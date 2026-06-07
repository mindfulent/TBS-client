# Publishing TheBlockSurvival

How the TheBlockSurvival client modpack is published to Modrinth and CurseForge.
This file is maintainer-only — it is excluded from the distributed pack via
`.packwizignore`.

## Tooling

`scripts/publish.py` exports the pack with packwiz and uploads it. Each release
produces **five** artifacts per platform — one per OS, because StreamCraft Live
ships per-OS native libraries that can't ride together in a single pack file:

| Variant | Modrinth artifact | CurseForge artifact |
|---------|-------------------|---------------------|
| Windows *(primary)* | `TheBlockSurvival-X.Y.Z.mrpack` | `TheBlockSurvival-X.Y.Z.zip` |
| Linux | `…-linux.mrpack` | `…-linux.zip` |
| Linux ARM64 | `…-linux-aarch64.mrpack` | `…-linux-aarch64.zip` |
| macOS Apple Silicon | `…-macos-arm64.mrpack` | `…-macos-arm64.zip` |
| macOS Intel | `…-macos-x86_64.mrpack` | `…-macos-x86_64.zip` |

```bash
pip install -r scripts/requirements.txt        # requests + markdown
cp .env.example .env                           # then fill in tokens

python scripts/publish.py --platform both --variant all --dry-run    # export + print metadata
python scripts/publish.py --platform modrinth                        # all 5 variants → one Modrinth version
python scripts/publish.py --platform both                            # both stores, all variants
python scripts/publish.py --platform modrinth --variant linux        # one variant (testing)
```

The version is read from `pack.toml`; the changelog is the matching `## [X.Y.Z]`
section of `CHANGELOG.md`. Modrinth uploads are idempotent. **Modrinth** receives
one version with all five `.mrpack` files attached (Windows primary). **CurseForge**
receives the Windows zip as primary + four additional files linked via
`parentFileID`, matching the StreamCraft convention.

### Per-platform StreamCraft overlay

The canonical pack references the Windows StreamCraft jar. For non-Windows
variants, `publish.py` overlays the matching `streamcraft-live.pw.toml` from
`scripts/platform-sources/<variant>/mods/` at export time, then restores. When
StreamCraft publishes a new version, regenerate the four non-Windows files —
swap the `filename`, `url`, and SHA-512 to match the new variant jars. The
Modrinth API gives you the URLs and hashes:

```bash
curl "https://api.modrinth.com/v2/version/<new-version-id>" | \
  python -c "import sys,json; [print(f['filename'], f['hashes']['sha512']) for f in json.load(sys.stdin)['files']]"
```

## Release checklist

1. Add/update mods (CurseForge-first — see `CLAUDE.md`), `packwiz refresh`.
2. Re-run the license check below if any mod was added.
3. Bump `version` in `pack.toml`; add a `## [X.Y.Z]` entry to `CHANGELOG.md`.
4. `python scripts/publish.py --platform modrinth --dry-run` — sanity-check.
5. `python scripts/publish.py --platform modrinth`.
6. Commit the pack changes inside this repo.

---

## One-time: create the Modrinth project

`publish.py` uploads versions to an *existing* project — it does not create one.
Create it once at <https://modrinth.com/> → **Create a project** → type **Modpack**,
then fill in the fields below and upload the icon + gallery screenshots.

### Project fields

| Field | Value |
|-------|-------|
| Name | `TheBlockSurvival` |
| Slug / URL | `theblocksurvival` |
| Summary | *(see below)* |
| Categories | `optimization`, `vanilla-like`, `multiplayer` |
| Environments | Client: **required** · Server: **unsupported** |
| License | Decision — see "License" below |
| Source / Issues | Link `github.com/slashdaemon/TBS-client` only if that repo is public |

### Summary (one sentence, ≤256 chars)

> An optional client-side modpack for Minecraft 26.1.2 that improves performance,
> visuals, audio, and quality-of-life without adding any gameplay content — so it
> works on any vanilla server.

### Description (paste into the Modrinth body)

```markdown
# TheBlockSurvival

**An optional client-side polish pack for vanilla-friendly Minecraft 26.1.2.**

TheBlockSurvival sharpens performance, lighting, audio, and quality-of-life for
long survival sessions — without touching a single gameplay mechanic. Every mod
is client-side or vanilla-protocol-safe, so the pack works on **any** vanilla
26.1.2 server. It is the companion client pack for *The Block Survival*, but
needs no special server to be worth installing.

## What's inside

- **Performance** — Sodium, Lithium, Krypton, FerriteCore, ImmediatelyFast,
  BadOptimizations, EntityCulling. More frames, smoother, on the same hardware.
- **Render distance & detail** — Voxy extended render distance, connected
  textures, Entity Model & Texture Features, subtle particles and ambience.
- **Camera, controls & animation** — Zoomify, Camera Utils, smooth item
  swapping, first-person body, 3D skin layers, Not Enough Animations.
- **HUD & quality-of-life** — JEI recipe search, WTHIT block tooltips,
  AppleSkin, BetterF3, Mod Menu, Controlling, Mouse Wheelie, and more.
- **Multiplayer** — StreamCraft Live (in-world video) and Simple Voice Chat
  (proximity voice), both optional per player and active only on servers that
  support them.

## Optional visual layer

A shader and PBR resource-pack set ship as **optional toggles** chosen at
import — off by default for a light client, on for a fully dialed-in look:

- Complementary Shaders – Reimagined
- Patrix 32x — labPBR resource pack
- Fresh Animations (+ Emissive, + Extensions)

## Vanilla-safe by design

No new blocks, items, mobs, or world generation. You get the **same game** as a
stock vanilla client — rendered better and easier to play — and you can join any
vanilla 26.1.2 server with it.

## Install

Import the `.mrpack` with **Prism Launcher** or the **Modrinth App**.

> **macOS / Linux:** StreamCraft Live ships per-platform native libraries; this
> pack references the Windows build. On macOS or Linux, swap the StreamCraft jar
> for the matching variant from the
> [StreamCraft Live](https://modrinth.com/mod/streamcraft-live) page.

## Credits

Built with [packwiz](https://packwiz.infra.link/). Every mod, shader, and
resource pack is the work of its respective author — please support them.
```

### License

Modrinth requires a license on the project. The choice applies to **the pack's
own work** — the packwiz curation and metadata — not the bundled mods, which keep
their own licenses. Recommended: **All Rights Reserved**, the usual choice for a
modpack (it protects the curation without affecting how players use the pack).
Pick a permissive license instead only if re-packaging of the curation should be
allowed.

## One-time: credentials

Copy `.env.example` → `.env` (gitignored) and fill in:

- `MODRINTH_TOKEN` — PAT with the "Create version" scope, from
  <https://modrinth.com/settings/pats>
- `MODRINTH_PROJECT` — `theblocksurvival` (or the project ID)

---

## License compliance

**Audit — 2026-05-22, pack v1.1.2.** A Modrinth `.mrpack` URL-references mods
sourced from Modrinth and **bundles** mods sourced from CurseForge as override
jars. Bundling is redistribution, so every bundled mod must permit it.

- All ~23 currently-bundled (CurseForge-sourced) mods are permissively licensed
  (MIT / LGPL-3.0 / GPL-3.0 / Apache-2.0 / Unlicense) — redistribution allowed.
- Mods with restrictive licenses are **URL references**, not bundled, so their
  licenses do not gate the pack: Camera Utils (All-Rights-Reserved),
  Crash Assistant (custom), WTHIT (CC-BY-NC-SA) — all re-sourced from Modrinth
  in v1.1.2 for exactly this reason — plus the optional Patrix 32x (ARR) and
  Complementary (custom) visual packs.

**When adding a mod:** if it is CurseForge-sourced it will be bundled — confirm
its license permits modpack redistribution, or re-source it from Modrinth so it
becomes a URL reference instead.

---

## CurseForge

### The CurseForge build differs from Modrinth — by design

A packwiz pack has one source per mod. The **canonical pack is
Modrinth-sourced**, which keeps the Modrinth build clean. For the CurseForge
build, `publish.py` applies two per-platform transformations at export time
(and restores the canonical state afterward, even on failure):

1. **Exclude** — five pack entries cannot ride along in the CurseForge package:

   | Entry | Why |
   |-------|-----|
   | `mods/voxy.pw.toml` | CurseForge does not permit Voxy in modpacks |
   | `shaderpacks/complementary-reimagined.pw.toml` | custom license, install separately |
   | `resourcepacks/fresh-animations.pw.toml` | custom "see terms" license |
   | `resourcepacks/fresh-animations-emissive.pw.toml` | ARR; rides with main FA |
   | `resourcepacks/fresh-animations-extensions.pw.toml` | ARR; rides with main FA |

   The list lives in `CURSEFORGE_EXCLUDED` at the top of `scripts/publish.py`.
   `publish.py` also appends a note to the CurseForge release changelog telling
   players what's missing and to install each separately. The **Modrinth** build
   keeps everything.

2. **Swap** — Modrinth-sourced mods that ARE referenceable on CurseForge get
   their `.pw.toml` temporarily replaced with a CurseForge-sourced equivalent so
   the CF manifest carries a proper project reference (instead of a bundled
   override). The CF metafiles live in **`scripts/cf-sources/`**, mirroring the
   pack's directory layout. There are currently 18 swap entries (17 mods +
   Patrix 32x).

After both transforms the CF zip ends up with ~45 manifest references + ~3
legally-bundleable overrides (Apache/MIT/LGPL/GPL/tr7zw-Protective mods that
couldn't be cleanly `cf install`'d).

### Maintaining `scripts/cf-sources/` when mods update

If you update or add a mod and want it referenced (not bundled) on CurseForge:

```bash
cd TBS-client
mkdir -p scripts/_mr_backup && cp -r mods resourcepacks shaderpacks scripts/_mr_backup/
./packwiz.exe cf install <slug> -y          # may create a different filename
cp <the-new-or-overwritten-cf-pw.toml> scripts/cf-sources/<original-relative-path>
rm -rf mods resourcepacks shaderpacks       # restore the canonical Modrinth state
cp -r scripts/_mr_backup/mods scripts/_mr_backup/resourcepacks scripts/_mr_backup/shaderpacks ./
rm -rf scripts/_mr_backup
./packwiz.exe refresh
```

If `cf install` creates a different-named metafile (e.g. `ferritecore-fabric.pw.toml`
when the canonical is `ferrite-core.pw.toml`), **rename the saved cf-source file
to match the canonical name** — the swap is path-for-path.

### CurseForge project description note

In the CurseForge project description, omit Voxy and the visual layer (the
Modrinth description above lists them). Reuse the rest of the body.

### Credentials and submission

Set `CURSEFORGE_TOKEN` (from <https://authors-old.curseforge.com/account/api-tokens>)
and `CURSEFORGE_PROJECT_ID` (numeric ID from the CF project dashboard) in `.env`.
Then `python scripts/publish.py --platform curseforge` exports + uploads.

> **One-time before the first CurseForge release: re-test on LocalServer.** Your
> `CLAUDE.md` requires testing untested version sets. A handful of swapped mods
> may pick a CurseForge version that differs slightly from the Modrinth-pinned
> one — most won't drift, but validate before submitting.
