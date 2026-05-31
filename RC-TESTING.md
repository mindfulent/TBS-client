# RC testing path (bundled pre-release → mrpack → GitHub)

Maintainer-only. Excluded from the distributed pack via `.packwizignore`.

Normally TheBlockSurvival references **published** mods (Modrinth/CurseForge) and ships via
`scripts/publish.py`. This is the **exception path** for handing a *release candidate* of a
not-yet-published mod (e.g. a StreamCraft pre-release) to testers, distributed **manually as
`.mrpack` via a GitHub pre-release** — skipping CurseForge and Modrinth entirely.

## Rules

- **`main` never carries a bundled RC.** It stays on the published Modrinth/CurseForge
  references. All RC work lives on a branch named **`rc/<thing>-<version>`**
  (e.g. `rc/streamcraft-0.10.2`).
- Use **plain `packwiz modrinth export`**, *not* `scripts/publish.py` (that drives the store
  upload + CurseForge transforms we're skipping).
- Ship as a **GitHub pre-release** (`--prerelease`) so it never becomes "Latest".
- When the mod is published to Modrinth, do a normal `main` release that reverts to the
  Modrinth reference, and delete/retire the RC branch.

## Procedure

1. `git switch -c rc/<thing>-<ver>` off `main`.
2. Bundle the RC as a **loose jar** in `mods/` (delete the published `.pw.toml`, copy the jar
   in). The canonical pack = the Windows/standard jar. `./packwiz.exe refresh`.
3. Set `pack.toml` version to an RC marker (e.g. `1.1.14-rc.1`).
4. Build one `.mrpack` per platform you're testing. For a non-Windows platform, **swap** the
   loose jar (`rm mods/streamcraft-*.jar`, copy the per-OS jar in, `refresh`), export with a
   suffixed `-o` name, then **swap back** to the canonical Windows jar + `refresh`:
   ```
   ./packwiz.exe modrinth export -o dist/TheBlockSurvival-<ver>.mrpack            # Windows/standard
   # swap to -macos-arm64 jar, refresh
   ./packwiz.exe modrinth export -o dist/TheBlockSurvival-<ver>-macos-arm64.mrpack
   # swap back to the Windows jar, refresh  (leave the branch on the canonical jar)
   ```
5. Commit the branch with the **canonical (Windows) jar** in `mods/`; push the branch.
6. `gh release create <tag> dist/*.mrpack --target rc/<thing>-<ver> --prerelease ...`.

## Server side

If testers need a matching server, do the same on a `rc/<thing>-<ver>` branch in
`TBS-server` (bundle the **standard** jar — the server doesn't use capture natives) and
deploy from that branch via `server-config.py deploy`. `main` server pack stays published.
