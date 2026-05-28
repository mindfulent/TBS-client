#!/usr/bin/env python3
"""
Publish the TheBlockSurvival client modpack to Modrinth and/or CurseForge.

TheBlockSurvival is the public release of the TBS-Client packwiz modpack. Unlike
StreamCraft (a multi-band, multi-platform *mod*), a modpack is a single artifact
per platform: one `.mrpack` for Modrinth, one `.zip` for CurseForge. This script
exports the pack with packwiz, then uploads it.

Modelled on StreamCraft's scripts/publish-modrinth.py + publish-curseforge.py —
same `.env` auth, the same idempotent-Modrinth and CurseForge-catalog-resolution
patterns — collapsed into one script because a modpack has no band/platform/loader
matrix to fan out over.

Usage:
    # Dry-run: export the artifact(s) and print upload metadata, upload nothing
    python scripts/publish.py --platform both --dry-run

    # Publish to Modrinth only (the v1 launch target)
    python scripts/publish.py --platform modrinth

    # Publish to both platforms
    python scripts/publish.py --platform both

    # Re-use an artifact already in dist/ instead of re-exporting
    python scripts/publish.py --platform modrinth --no-export

The version is read from pack.toml; the changelog is the matching `## [X.Y.Z]`
section of CHANGELOG.md. Auth comes from a gitignored `.env` in the pack root
(TBS-client/.env) — see .env.example:

    MODRINTH_TOKEN          PAT with "Create version" scope — modrinth.com/settings/pats
    MODRINTH_PROJECT        project slug or ID (default: theblocksurvival)
    CURSEFORGE_TOKEN        token from authors-old.curseforge.com/account/api-tokens
    CURSEFORGE_PROJECT_ID   numeric project ID of the CurseForge modpack project

The Modrinth and CurseForge projects must be created manually on each site first —
this script uploads a version to an *existing* project, it does not create one.

Idempotent on Modrinth: an existing version with the same version_number is
skipped, so re-running after a partial failure won't double-upload. CurseForge has
no equivalent lookup — if a CF upload half-fails, delete the partial file via the
CF dashboard before retrying.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERR: requests not installed. Install with: pip install -r scripts/requirements.txt")
    sys.exit(1)

try:
    import markdown as _markdown
except ImportError:
    _markdown = None  # CurseForge changelog falls back to plain text if absent


MODRINTH_API = "https://api.modrinth.com/v2"
CURSEFORGE_API = "https://minecraft.curseforge.com/api"
USER_AGENT = "mindfulent/TheBlockSurvival publish.py (jon@papp.as)"

DEFAULT_MODRINTH_PROJECT = "theblocksurvival"
# Loader the .mrpack manifest declares. TheBlockSurvival is a Fabric pack.
PACK_LOADERS = ["fabric"]

# Per-platform variants. StreamCraft Live ships per-OS native libraries (one
# jar per platform), so a single modpack can't serve every OS — we produce one
# pack file per variant, each pointing at the matching StreamCraft jar. The
# canonical pack already references the Windows StreamCraft jar; for the other
# variants, publish.py overlays scripts/platform-sources/<variant>/ on top of
# the pack at export time, then restores.
PLATFORM_VARIANTS = ["windows", "linux", "linux-aarch64", "macos-arm64", "macos-x86_64"]
DEFAULT_VARIANT = "windows"  # canonical pack ≡ Windows; no swap needed for this one
PLATFORM_SOURCES_DIR = "scripts/platform-sources"


def variant_suffix(variant: str) -> str:
    """Filename suffix for a variant. Windows is the primary download and ships
    without a classifier suffix (matching the StreamCraft convention)."""
    return "" if variant == DEFAULT_VARIANT else f"-{variant}"

# The CurseForge build is produced from the canonical Modrinth-sourced pack by
# applying two per-platform transformations at export time, then restoring the
# canonical state. The Modrinth build is exported untouched.
#
# 1. EXCLUDE: pack entries that cannot ship in the CurseForge package at all.
#    Paths relative to the pack root.
CURSEFORGE_EXCLUDED = [
    "mods/voxy.pw.toml",                                 # CurseForge prohibits Voxy in modpacks
    "shaderpacks/complementary-reimagined.pw.toml",      # custom license; install separately
    "resourcepacks/fresh-animations.pw.toml",            # "see terms" license; install separately
    "resourcepacks/fresh-animations-emissive.pw.toml",   # ARR; rides with main FA
    "resourcepacks/fresh-animations-extensions.pw.toml", # ARR; rides with main FA
]

# 2. SWAP: pack entries whose canonical Modrinth-sourced .pw.toml is replaced
#    with a CurseForge-sourced equivalent so the CF zip carries a proper
#    manifest reference (not a bundled override). Files live in
#    scripts/cf-sources/, mirroring the pack's directory layout — every
#    .pw.toml in there is swapped into the pack for the CurseForge export,
#    then removed in the cleanup so the canonical pack stays Modrinth-sourced.
#
# To add a swap: cd into the pack, snapshot mods/resourcepacks/shaderpacks,
# `./packwiz.exe cf install <slug> -y`, copy the resulting CF metafile to
# scripts/cf-sources/<same-relative-path>, then restore the snapshot.
CF_SOURCES_DIR = "scripts/cf-sources"

# Appended to the CurseForge release changelog so the CF page always tells
# players what's missing relative to the Modrinth build, and why.
CURSEFORGE_EXCLUSION_NOTE = (
    "\n\n---\n"
    "### Not in the CurseForge build\n"
    "A few things can't ride along inside the CurseForge package because of "
    "licensing or CurseForge policy. The **Modrinth** build of this pack "
    "includes them; on CurseForge, install them yourself:\n\n"
    "- **Voxy** — CurseForge does not permit redistributing it in modpacks. "
    "Install from its Modrinth page.\n"
    "- **Complementary Shaders – Reimagined** — install from its CurseForge "
    "page. The bundled **Patrix 32x** resource pack pairs with it for labPBR.\n"
    "- **Fresh Animations** (main pack + Emissive + Extensions) — install the "
    "FA family from CurseForge."
)


# --------------------------------------------------------------------------
# .env + pack metadata
# --------------------------------------------------------------------------

def load_dotenv(path: Path) -> None:
    """Minimal .env loader: KEY=VALUE per line, no quoting/expansion. Existing
    environment variables win over .env entries."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and value and key not in os.environ:
            os.environ[key] = value


def read_pack_field(pack_toml: Path, key: str, section: str | None = None) -> str:
    """Pull a `key = "value"` string out of pack.toml without a TOML lib
    (tomllib is 3.11+; the pack targets Python 3.10+). When `section` is given,
    only the lines under that `[section]` header are searched."""
    text = pack_toml.read_text(encoding="utf-8")
    if section:
        m = re.search(rf"^\[{re.escape(section)}\]\s*$(.*?)(?=^\[|\Z)", text,
                      re.MULTILINE | re.DOTALL)
        text = m.group(1) if m else ""
    m = re.search(rf'^\s*{re.escape(key)}\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not m:
        raise SystemExit(f"ERR: could not find `{key}` in {pack_toml}"
                         + (f" under [{section}]" if section else ""))
    return m.group(1)


def extract_changelog(changelog_path: Path, version: str) -> str:
    """Return the `## [X.Y.Z]` section of CHANGELOG.md (TBS-client uses the
    Keep-a-Changelog `## [version] — date` heading style)."""
    if not changelog_path.exists():
        return ""
    text = changelog_path.read_text(encoding="utf-8")
    pattern = rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def render_changelog(markdown_text: str, fmt: str) -> tuple[str, str]:
    """Returns (rendered, changelogType) for a CurseForge upload. CF's own
    "markdown" type renders raw markup unreliably, so by default we convert to
    HTML client-side and send changelogType="html"."""
    if fmt == "html":
        if _markdown is None:
            print("  WARN python-markdown not installed; sending changelogType=text. "
                  "Install with: pip install -r scripts/requirements.txt")
            return markdown_text, "text"
        return _markdown.markdown(markdown_text), "html"
    return markdown_text, fmt  # "markdown" / "text" sent verbatim


# --------------------------------------------------------------------------
# packwiz export
# --------------------------------------------------------------------------

def packwiz_export(pack_dir: Path, packwiz_exe: Path, platform: str, out_path: Path,
                   variant: str = DEFAULT_VARIANT) -> None:
    """Run `packwiz refresh` then `packwiz <platform> export` into out_path.

    Two per-platform transformations are applied to the pack in-place before
    export, then reverted in a finally block so the canonical Modrinth-sourced
    state is always restored — even on a failed export:

    - **CurseForge swap** (only when platform=="curseforge"): excludes
      CURSEFORGE_EXCLUDED entries and overlays the files in CF_SOURCES_DIR so
      the .zip carries proper CurseForge manifest references.
    - **Platform overlay** (when variant != DEFAULT_VARIANT): overlays the
      files in PLATFORM_SOURCES_DIR/<variant>/ — currently a per-OS
      StreamCraft Live .pw.toml so each platform's .mrpack / .zip points at
      the matching StreamCraft jar. Layered on top of the CurseForge swap so
      the per-OS StreamCraft wins over the Windows CF reference for
      non-Windows CF builds."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cf_excluded: list[Path] = []
    swaps: dict[Path, Path] = {}  # canonical-path-in-pack -> source-file-to-copy-in
    excluded_set: set[Path] = set()

    if platform == "curseforge":
        excluded_set = {pack_dir / rel for rel in CURSEFORGE_EXCLUDED}
        for pw in excluded_set:
            if pw.exists():
                cf_excluded.append(pw)
        cf_src_root = pack_dir / CF_SOURCES_DIR
        if cf_src_root.is_dir():
            for cf_src in sorted(cf_src_root.rglob("*.pw.toml")):
                canon = pack_dir / cf_src.relative_to(cf_src_root)
                # Exclusion wins over swap — a stray cf-source for an
                # excluded entry would otherwise sneak it back into the build.
                if canon in excluded_set:
                    continue
                swaps[canon] = cf_src

    if variant != DEFAULT_VARIANT:
        plat_root = pack_dir / PLATFORM_SOURCES_DIR / variant
        if plat_root.is_dir():
            for plat_src in sorted(plat_root.rglob("*.pw.toml")):
                canon = pack_dir / plat_src.relative_to(plat_root)
                if canon in excluded_set:
                    continue
                # Platform overlay overrides any CF swap at the same path —
                # per-OS StreamCraft jar wins over the Windows CF reference.
                swaps[canon] = plat_src

    # Files we'll move/replace and must restore afterward.
    affected = list(cf_excluded) + list(swaps.keys())

    stash_dir: Path | None = None
    try:
        if affected:
            # Stash canonical state OUTSIDE pack_dir so packwiz can't re-index it.
            # Index-prefix to avoid name collisions across mods/ rp/ sp/.
            stash_dir = Path(tempfile.mkdtemp(prefix="tbs-export-stash-"))
            for i, p in enumerate(affected):
                if p.exists():
                    shutil.move(str(p), str(stash_dir / f"{i}_{p.name}"))
            # Apply swaps: copy each source over its canonical pack path.
            for canon, src in swaps.items():
                canon.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(canon))
            for p in cf_excluded:
                print(f"  excluded from CurseForge build: {p.relative_to(pack_dir).as_posix()}")
            if variant != DEFAULT_VARIANT:
                print(f"  platform overlay applied:       {variant}")

        for args in (["refresh"], [platform, "export", "-o", str(out_path)]):
            print(f"  $ packwiz {' '.join(args)}")
            r = subprocess.run([str(packwiz_exe), *args], cwd=pack_dir)
            if r.returncode != 0:
                raise SystemExit(
                    f"ERR: `packwiz {' '.join(args)}` exited {r.returncode}. "
                    "A non-zero curseforge export usually means a mod's CurseForge "
                    "file blocks third-party distribution — re-source it from Modrinth."
                )
    finally:
        if stash_dir is not None:
            # Remove swap-applied files first so the canonical restore is clean.
            for canon in swaps:
                if canon.exists():
                    canon.unlink()
            # Restore canonical files from the stash.
            for i, p in enumerate(affected):
                stashed = stash_dir / f"{i}_{p.name}"
                if stashed.exists():
                    p.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(stashed), str(p))
            stash_dir.rmdir()
            # Rebuild the index to match the restored canonical state.
            subprocess.run([str(packwiz_exe), "refresh"], cwd=pack_dir)

    if not out_path.exists():
        raise SystemExit(f"ERR: packwiz reported success but {out_path} is missing")
    size_mb = out_path.stat().st_size / 1_000_000
    print(f"  exported {out_path.name} ({size_mb:.2f} MB)")


# --------------------------------------------------------------------------
# Modrinth
# --------------------------------------------------------------------------

def modrinth_resolve_project(slug_or_id: str, token: str) -> str:
    """Modrinth's POST /version wants the project's base62 ID in the JSON body —
    a slug there fails with 'Base62 decoding overflowed'. URL paths take either."""
    r = requests.get(f"{MODRINTH_API}/project/{slug_or_id}",
                      headers={"Authorization": token, "User-Agent": USER_AGENT},
                      timeout=30)
    if r.status_code == 404:
        raise SystemExit(
            f"ERR: Modrinth project '{slug_or_id}' not found. Create the modpack "
            f"project at https://modrinth.com/ first, then set MODRINTH_PROJECT "
            f"(slug or ID) in .env or pass --modrinth-project."
        )
    r.raise_for_status()
    data = r.json()
    if data.get("project_type") != "modpack":
        print(f"  WARN Modrinth project '{slug_or_id}' has project_type="
              f"{data.get('project_type')!r}, expected 'modpack'")
    return data["id"]


def modrinth_find_version(project: str, version_number: str, token: str) -> str | None:
    r = requests.get(f"{MODRINTH_API}/project/{project}/version",
                      headers={"Authorization": token, "User-Agent": USER_AGENT},
                      timeout=30)
    r.raise_for_status()
    for v in r.json():
        if v["version_number"] == version_number:
            return v["id"]
    return None


def publish_modrinth(
    mrpacks: list[Path],
    project: str,
    version: str,
    game_versions: list[str],
    version_type: str,
    changelog: str,
    token: str,
    dry_run: bool,
) -> bool:
    """Upload one Modrinth version with all platform-variant .mrpack files
    attached. `mrpacks[0]` is marked primary. Returns True on a successful
    upload."""
    if not mrpacks:
        raise ValueError("publish_modrinth: empty mrpacks list")
    primary = mrpacks[0]
    print(f"\n=== Modrinth: {project} v{version} ===")
    print(f"  game_versions: {game_versions}  loaders: {PACK_LOADERS}  type: {version_type}")
    print(f"  files: {len(mrpacks)} (primary: {primary.name})")
    for p in mrpacks[1:]:
        print(f"         {p.name}")

    metadata = {
        "name": f"v{version}",
        "version_number": version,
        "changelog": changelog,
        "dependencies": [],          # modpack deps are carried inside the .mrpack manifest
        "game_versions": game_versions,
        "version_type": version_type,
        "loaders": PACK_LOADERS,
        "featured": False,
        "file_parts": [p.name for p in mrpacks],
        "primary_file": primary.name,
    }

    if dry_run:
        print(f"  DRY-RUN — would POST {MODRINTH_API}/version:\n"
              f"{json.dumps(metadata, indent=2)}")
        return False

    project_id = modrinth_resolve_project(project, token)
    metadata["project_id"] = project_id  # base62 ID — strict in the JSON body
    existing = modrinth_find_version(project, version, token)
    if existing:
        print(f"  SKIP — version {version} already published (id={existing})")
        return False

    total_mb = sum(p.stat().st_size for p in mrpacks) / 1_000_000
    primary_mb = primary.stat().st_size / 1_000_000
    print(f"  POST {MODRINTH_API}/version  (primary only: {primary_mb:.2f} MB; "
          f"+{len(mrpacks) - 1} additional files staged separately, "
          f"{total_mb:.2f} MB total) ...")
    # Staged upload: a single multipart POST with all 5 .mrpacks exceeds Cloudflare's
    # ~100 MB API-gateway cap (HTTP 413). Modrinth's create-version endpoint accepts
    # one file at a time fine, so we POST /version with just the primary, then add
    # each additional file via POST /version/{id}/file. Same end state — one Modrinth
    # version with N files attached, primary first.
    primary_metadata = dict(metadata)
    primary_metadata["file_parts"] = [primary.name]
    with primary.open("rb") as fh:
        files = [
            ("data", (None, json.dumps(primary_metadata), "application/json")),
            (primary.name, (primary.name, fh, "application/x-modrinth-modpack+zip")),
        ]
        r = requests.post(f"{MODRINTH_API}/version",
                          headers={"Authorization": token, "User-Agent": USER_AGENT},
                          files=files, timeout=600)
    if r.status_code >= 400:
        raise RuntimeError(f"Modrinth (primary) {r.status_code}: {r.text}")
    data = r.json()
    version_id = data["id"]
    print(f"  OK primary uploaded id={version_id} ({primary.name})")

    for extra in mrpacks[1:]:
        size_mb = extra.stat().st_size / 1_000_000
        print(f"  POST {MODRINTH_API}/version/{version_id}/file  ({size_mb:.2f} MB, {extra.name}) ...")
        extra_meta = {"file_parts": [extra.name]}
        with extra.open("rb") as fh:
            files = [
                ("data", (None, json.dumps(extra_meta), "application/json")),
                (extra.name, (extra.name, fh, "application/x-modrinth-modpack+zip")),
            ]
            r = requests.post(f"{MODRINTH_API}/version/{version_id}/file",
                              headers={"Authorization": token, "User-Agent": USER_AGENT},
                              files=files, timeout=600)
        if r.status_code >= 400:
            raise RuntimeError(f"Modrinth (additional {extra.name}) {r.status_code}: {r.text}")
        print(f"    OK additional uploaded ({extra.name})")
    print(f"  OK id={version_id}  files={len(mrpacks)}  "
          f"https://modrinth.com/modpack/{project}/version/{version}")
    return True


# --------------------------------------------------------------------------
# CurseForge
# --------------------------------------------------------------------------

def cf_fetch_catalog(token: str) -> tuple[dict[tuple[int, str], int], dict[str, int]]:
    """Return ((typeId, name)->id catalog, version-type slug->id map). CurseForge
    lists each version name under several type buckets; uploads must reference the
    Minecraft-type ID for MC versions and the Modloader-type ID for "Fabric"."""
    hdr = {"X-Api-Token": token, "User-Agent": USER_AGENT}
    r = requests.get(f"{CURSEFORGE_API}/game/versions", headers=hdr, timeout=30)
    r.raise_for_status()
    catalog = {(v["gameVersionTypeID"], v["name"]): v["id"] for v in r.json()}
    r = requests.get(f"{CURSEFORGE_API}/game/version-types", headers=hdr, timeout=30)
    r.raise_for_status()
    type_ids = {t["slug"]: t["id"] for t in r.json()}
    return catalog, type_ids


def cf_type_slug(name: str) -> str | None:
    """Version-type slug a name lives under: "26.1.2" -> "minecraft-26-1",
    "1.21.11" -> "minecraft-1-21", "Fabric" -> "modloader"."""
    if name in ("Fabric", "NeoForge", "Quilt"):
        return "modloader"
    m = re.match(r"^(\d+)\.(\d+)(?:\.\d+)?$", name)
    return f"minecraft-{m.group(1)}-{m.group(2)}" if m else None


def cf_resolve_game_versions(
    catalog: dict[tuple[int, str], int],
    type_ids: dict[str, int],
    names: list[str],
) -> list[int]:
    ids, missing = [], []
    for name in names:
        slug = cf_type_slug(name)
        type_id = type_ids.get(slug) if slug else None
        cf_id = catalog.get((type_id, name)) if type_id else None
        if cf_id is None:
            missing.append(f"{name} (slug={slug})")
        else:
            ids.append(cf_id)
    if missing:
        print(f"  WARN CurseForge catalog missing {missing}; those entries "
              f"won't appear on the file's version list")
    return ids


def publish_curseforge(
    zips: list[Path],
    project_id: int,
    version: str,
    game_version_names: list[str],
    release_type: str,
    changelog: str,
    changelog_type: str,
    token: str,
    dry_run: bool,
) -> bool:
    """Upload `zips[0]` as the primary CurseForge file; upload each subsequent
    entry as an additional file with `parentFileID` set to the primary's file
    id — matching StreamCraft's per-platform CurseForge convention. CurseForge
    rejects gameVersions on additional files (children inherit from parent),
    so only the primary carries the versions list."""
    if not zips:
        raise ValueError("publish_curseforge: empty zips list")
    primary = zips[0]
    print(f"\n=== CurseForge: project {project_id} v{version} ===")
    print(f"  files: {len(zips)} (primary: {primary.name})")
    for p in zips[1:]:
        print(f"         {p.name}")

    catalog, type_ids, game_version_ids = {}, {}, []
    if token:
        try:
            catalog, type_ids = cf_fetch_catalog(token)
            game_version_ids = cf_resolve_game_versions(catalog, type_ids, game_version_names)
            print(f"  game versions {game_version_names} -> ids {game_version_ids}")
        except Exception as e:
            print(f"  ERR could not fetch CurseForge catalog: {e}")
            if not dry_run:
                raise

    primary_meta = {
        "changelog": changelog,
        "changelogType": changelog_type,
        "displayName": primary.name,
        "gameVersions": game_version_ids,
        "releaseType": release_type,
    }

    if dry_run:
        print(f"  DRY-RUN — would POST primary:\n{json.dumps(primary_meta, indent=2)}")
        for p in zips[1:]:
            extra_preview = {
                "changelog": "<same>", "changelogType": changelog_type,
                "displayName": p.name, "releaseType": release_type,
                "parentFileID": "<resolved from primary upload>",
            }
            print(f"  DRY-RUN — would POST additional ({p.name}):\n"
                  f"{json.dumps(extra_preview, indent=2)}")
        return False

    if not game_version_ids:
        raise SystemExit("ERR: CurseForge upload needs at least one resolved gameVersion id")

    url = f"{CURSEFORGE_API}/projects/{project_id}/upload-file"

    def _upload(z: Path, meta: dict) -> int:
        size_mb = z.stat().st_size / 1_000_000
        print(f"  POST {url} ({size_mb:.2f} MB, {z.name}) ...")
        with z.open("rb") as fh:
            files = {
                "metadata": (None, json.dumps(meta), "application/json"),
                "file": (z.name, fh, "application/zip"),
            }
            r = requests.post(url, headers={"X-Api-Token": token, "User-Agent": USER_AGENT},
                              files=files, timeout=600)
        if r.status_code >= 400:
            raise RuntimeError(f"CurseForge {r.status_code}: {r.text}")
        fid = r.json().get("id")
        if not isinstance(fid, int):
            raise RuntimeError(f"CurseForge returned no file id: {r.json()}")
        return fid

    primary_id = _upload(primary, primary_meta)
    print(f"    OK primary fileID={primary_id}")
    for p in zips[1:]:
        extra_meta = {
            "changelog": changelog,
            "changelogType": changelog_type,
            "displayName": p.name,
            "releaseType": release_type,
            "parentFileID": primary_id,
        }
        extra_id = _upload(p, extra_meta)
        print(f"    OK additional fileID={extra_id}")
    return True


# --------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--platform", choices=["modrinth", "curseforge", "both"],
                   default="both", help="Where to publish (default: both)")
    p.add_argument("--variant", default="all",
                   help=f"Platform variant(s) to build: {'/'.join(PLATFORM_VARIANTS)} or "
                        f"'all' (default — builds every variant and uploads them as one "
                        f"multi-file Modrinth version / CurseForge primary+additionals).")
    p.add_argument("--type", default="release", choices=["release", "beta", "alpha"],
                   help="Release channel (default: release)")
    p.add_argument("--modrinth-project", help="Modrinth slug or ID "
                   "(default: $MODRINTH_PROJECT or 'theblocksurvival')")
    p.add_argument("--cf-project-id", type=int,
                   help="CurseForge numeric project ID (default: $CURSEFORGE_PROJECT_ID)")
    p.add_argument("--game-versions", help="Comma-separated MC versions to advertise "
                   "(default: the pack.toml [versions] minecraft value)")
    p.add_argument("--changelog-format", default="html",
                   choices=["html", "markdown", "text"],
                   help="CurseForge changelogType (default: html, converted client-side)")
    p.add_argument("--no-export", action="store_true",
                   help="Skip packwiz export; use the artifact already in dist/")
    p.add_argument("--dry-run", action="store_true",
                   help="Export and print upload metadata, but upload nothing")
    args = p.parse_args()

    # Windows consoles default to cp1252 — force UTF-8 so em-dashes in our own
    # output and in the echoed changelog don't turn into mojibake.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    pack_dir = Path(__file__).resolve().parent.parent
    load_dotenv(pack_dir / ".env")

    packwiz_exe = pack_dir / ("packwiz.exe" if os.name == "nt" else "packwiz")
    if not packwiz_exe.exists():
        # fall back to whichever name is present
        packwiz_exe = next(pack_dir.glob("packwiz*"), packwiz_exe)
    version = read_pack_field(pack_dir / "pack.toml", "version")
    mc_version = read_pack_field(pack_dir / "pack.toml", "minecraft", section="versions")
    game_versions = ([v.strip() for v in args.game_versions.split(",")]
                     if args.game_versions else [mc_version])

    changelog_md = extract_changelog(pack_dir / "CHANGELOG.md", version)
    if changelog_md:
        print(f"Version {version} — changelog: "
              f"{changelog_md.splitlines()[0]} ({len(changelog_md)} chars)")
    else:
        print(f"WARN no `## [{version}]` section found in CHANGELOG.md")

    do_modrinth = args.platform in ("modrinth", "both")
    do_curseforge = args.platform in ("curseforge", "both")

    # Determine variants to build.
    if args.variant == "all":
        variants = list(PLATFORM_VARIANTS)
    elif args.variant in PLATFORM_VARIANTS:
        variants = [args.variant]
    else:
        print(f"ERR: unknown --variant {args.variant!r}; valid: {PLATFORM_VARIANTS} or 'all'")
        return 1
    print(f"Variants: {', '.join(variants)}")

    dist = pack_dir / "dist"
    mrpacks: list[Path] = []
    cf_zips: list[Path] = []
    for v in variants:
        suf = variant_suffix(v)
        if do_modrinth:
            mrpacks.append(dist / f"TheBlockSurvival-{version}{suf}.mrpack")
        if do_curseforge:
            cf_zips.append(dist / f"TheBlockSurvival-{version}{suf}.zip")

    # ---- export -----------------------------------------------------------
    if not args.no_export:
        for idx, v in enumerate(variants):
            if do_modrinth:
                print(f"\n--- exporting .mrpack ({v}) ---")
                packwiz_export(pack_dir, packwiz_exe, "modrinth", mrpacks[idx], variant=v)
            if do_curseforge:
                print(f"\n--- exporting CurseForge .zip ({v}) ---")
                packwiz_export(pack_dir, packwiz_exe, "curseforge", cf_zips[idx], variant=v)

    failures = 0

    # ---- Modrinth (one version, all variants attached) --------------------
    if do_modrinth:
        for p in mrpacks:
            if not p.exists():
                raise SystemExit(f"ERR: {p} not found (run without --no-export)")
        token = os.environ.get("MODRINTH_TOKEN", "")
        if not token and not args.dry_run:
            print("ERR: MODRINTH_TOKEN not set (.env or env var)")
            return 1
        project = (args.modrinth_project or os.environ.get("MODRINTH_PROJECT")
                   or DEFAULT_MODRINTH_PROJECT)
        try:
            publish_modrinth(mrpacks, project, version, game_versions,
                             args.type, changelog_md, token, args.dry_run)
        except Exception as e:
            print(f"  FAILED: {e}")
            failures += 1

    # ---- CurseForge (primary + additionals via parentFileID) --------------
    if do_curseforge:
        for p in cf_zips:
            if not p.exists():
                raise SystemExit(f"ERR: {p} not found (run without --no-export)")
        token = os.environ.get("CURSEFORGE_TOKEN", "")
        if not token and not args.dry_run:
            print("ERR: CURSEFORGE_TOKEN not set (.env or env var)")
            return 1
        cf_pid = args.cf_project_id
        if cf_pid is None:
            env_pid = os.environ.get("CURSEFORGE_PROJECT_ID", "").strip()
            if not env_pid and not args.dry_run:
                print("ERR: --cf-project-id not given and CURSEFORGE_PROJECT_ID not set")
                return 1
            cf_pid = int(env_pid) if env_pid else 0
        # The CurseForge build ships without the CURSEFORGE_EXCLUDED entries —
        # append a note so the CF release page always explains what's missing.
        cf_changelog_md = changelog_md + CURSEFORGE_EXCLUSION_NOTE
        changelog_cf, changelog_type = render_changelog(cf_changelog_md, args.changelog_format)
        try:
            publish_curseforge(cf_zips, cf_pid, version, [*game_versions, "Fabric"],
                               args.type, changelog_cf, changelog_type, token, args.dry_run)
        except Exception as e:
            print(f"  FAILED: {e}")
            failures += 1

    print(f"\nDone — {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
