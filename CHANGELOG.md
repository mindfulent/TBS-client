# Changelog — TheBlockSurvival

All notable changes to the TheBlockSurvival client modpack (formerly TBS-Client).

## [1.1.3] — 2026-05-22

Multi-platform release. v1.1.2 shipped only the Windows StreamCraft variant, so
macOS and Linux players got broken native libraries on import. v1.1.3 ships **one
pack file per OS**, each pointing at the matching StreamCraft Live 0.8.25 build.

### Added
- **`scripts/platform-sources/<variant>/`** — per-OS `streamcraft-live.pw.toml`
  files for `linux`, `linux-aarch64`, `macos-arm64`, `macos-x86_64`. The
  canonical pack still references the Windows StreamCraft jar; for the other
  variants, `publish.py` overlays the matching `streamcraft-live.pw.toml`.
- `publish.py --variant <name|all>` flag and per-variant output filenames
  (e.g. `TheBlockSurvival-1.1.3-linux.mrpack`). The Windows variant has no
  classifier suffix and is the primary download, matching the StreamCraft
  convention.
- Multi-file uploads in `publish.py` — one Modrinth version with all 5
  `.mrpack` files attached, and one CurseForge release with the Windows zip
  as primary + 4 additional files via `parentFileID`.

### Fixed
- Removed a stray `plugins/simple-voice-chat.pw.toml` that a `cf install` in an
  earlier session had quietly created (CurseForge classifies Simple Voice Chat
  as a Bukkit Plugin, so packwiz routed the metafile to `plugins/` instead of
  `mods/`). It poisoned the CurseForge `manifest.json` with a reference to a
  Bukkit project — which CurseForge's modpack moderation rejects — and bloated
  the Modrinth `.mrpack` with a useless `overrides/plugins/voicechat-bukkit-*.jar`.
  Added `plugins/` to `.packwizignore` so a future stray can't slip through.

### Notes
- Players on macOS/Linux who imported v1.1.2 should re-import the matching
  v1.1.3 variant; the manual StreamCraft jar swap recommended in v1.1.2's notes
  is no longer required.
- Adding more platform-specific overlays later (per-OS configs etc.) only needs
  another file under `scripts/platform-sources/<variant>/` at the matching pack
  path — `publish.py` already overlays everything in there.

50 packwiz metadata entries (canonical, Windows-variant).

## [1.1.2] — 2026-05-22

Prepares the pack for public release as **TheBlockSurvival** on Modrinth.

### Changed
- **StreamCraft Live** — re-pinned from the bundled work-in-progress
  `streamcraft-0.8.22+mc26.1.2.jar` loose override to the published Modrinth
  release `streamcraft-0.8.25+mc26.1.2.jar`. The pack source tree no longer
  contains any loose jar files; every entry is packwiz metadata, which keeps the
  public `.mrpack` clean.
- Pack renamed `TBS-Client` → `TheBlockSurvival` (`pack.toml` `name`). Exported
  artifacts are now `TheBlockSurvival-X.Y.Z.{mrpack,zip}`.
- **Camera Utils, Crash Assistant, WTHIT** re-sourced from CurseForge to Modrinth
  *(Modrinth)*. Their licenses (All-Rights-Reserved / custom / CC-BY-NC-SA) do not
  permit redistribution as bundled jars; as Modrinth metadata they ride in the
  public `.mrpack` as URL references, which redistributes nothing.

### Added
- `scripts/publish.py` — automated export + publish to Modrinth and CurseForge,
  modelled on StreamCraft's publish scripts. Auth via a gitignored `.env`
  (see `.env.example`); dependencies in `scripts/requirements.txt`.
- `scripts/cf-sources/` — CurseForge-sourced `.pw.toml` files for the CurseForge
  build's per-platform swap. `publish.py` keeps the canonical pack
  Modrinth-sourced (so the Modrinth build stays clean) and copies these CF
  metafiles over the canonical paths only for the CurseForge export, then
  restores. 18 swap entries (17 mods + Patrix 32x).

### Notes
- StreamCraft Live 0.8.25 ships per-platform variants (native libraries); the pack
  references the Windows default. macOS/Linux players should swap in the matching
  StreamCraft variant from its Modrinth page after importing.
- **CurseForge build differences from Modrinth.** The CurseForge package excludes
  five entries that can't ride along: **Voxy** (CurseForge policy prohibits it),
  **Complementary Shaders – Reimagined** and the **Fresh Animations** pack family
  (main + Emissive + Extensions — custom/ARR licenses don't allow redistribution
  inside a modpack). `publish.py` drops them automatically and appends a note to
  the CurseForge release changelog telling players to install each separately.
  Patrix 32x stays in the CurseForge build via the CF reference swap.

50 packwiz metadata entries (the StreamCraft jar is now a Modrinth reference, not
a bundled file).

## [1.1.1] — 2026-05-20

Fixes the launch crash in v1.1.0, and bundles the work-in-progress StreamCraft build.

### Fixed — v1.1.0 would not launch
- **AmbientSounds** was missing its **CreativeCore** dependency (CurseForge metadata never
  declared it) — added CreativeCore `2.14.14`.
- **Sodium** downgraded `0.8.12` → `0.8.11` *(Modrinth)* — Voxy `0.2.15-beta`, the latest
  Voxy, requires Sodium `0.8.9`–`0.8.11`.
- **VTDownloader** removed — its only build targets Minecraft `1.21.11`, which the Fabric
  loader treats as distinct from `26.1.2`, so it was rejected at load. Re-add when a
  26.1.2 build appears.

### Changed
- **StreamCraft Live** — switched from the Modrinth `0.8.8` reference to a bundled local
  build, `streamcraft-0.8.22+mc26.1.2.jar`, carried as a loose override in `mods/`. 0.8.22
  is a work-in-progress build not yet on Modrinth; re-pin to the Modrinth version once it
  is published. TBS-Server bundles the identical jar.

50 entries (49 packwiz metadata + the bundled StreamCraft jar).

## [1.1.0] — 2026-05-20

Adds an **optional visual layer** — the Complementary Reimagined shader, the Fresh
Animations entity-animation family, and a labPBR resource pack — plus the VTDownloader
utility mod and **Simple Voice Chat** proximity voice chat. **50** metadata entries total
(was 43).

The shader and resource packs are packwiz **optional** entries (`[option] optional = true`):
they ride in the exported `.mrpack` as Modrinth URL references and appear as per-player
toggles in Prism / the CurseForge App. Nothing is bundled — the All-Rights-Reserved
Patrix pack and the custom-licensed Complementary shader are only ever linked.

### Tier 4 — HUD, UI, utility
- VTDownloader — in-game Vanilla Tweaks resource-pack picker

### Tier 5 — Cross-side
- **Simple Voice Chat** `2.6.17` *(Modrinth)* — proximity voice chat; shipped in both packs
  at the same jar version as TBS-Server. Optional per player — a vanilla client without it
  still connects and plays, it just has no voice.

### Resource packs & shader (optional)
- **Complementary Shaders - Reimagined** `r5.8` *(Modrinth)* — Iris shader; default off
- **Patrix 32x** *(Modrinth)* — 32x labPBR resource pack; default off
- **Fresh Animations** `v1.10.5` *(Modrinth)* — smooth entity animations (uses the
  bundled EMF + ETF); default on
- **Fresh Animations: Emissive** *(Modrinth)* — glowing-eye textures under shaders; default on
- **Fresh Animations: Extensions** *(Modrinth)* — Classic Horses / Objects models; default on

### Changed
- Re-sourced **First-person Model**, **Not Enough Animations**, **Subtle Effects**, and
  **Skin Layers 3D** from CurseForge to Modrinth. Their CurseForge files forbid
  third-party API distribution, which aborted `packwiz modrinth export` entirely — the
  v1.0.0 `.mrpack` was never produced. With Modrinth metadata the pack now exports.
- Added `1.21.11` to the pack's `acceptable-game-versions` — 26.1.2 is the Fabric
  1.21.11 ecosystem, and VTDownloader's current build is tagged `1.21.11`.

### Notes
- See `README.md` for the recommended in-game resource-pack load order and the
  Complementary "RP Support → labPBR" setup step; `docs/resource-packs.md` has the full
  rationale.
- All five visual packs are Modrinth-sourced: the Fresh Animations family blocks
  CurseForge third-party distribution, and Patrix / Complementary carry restrictive
  licenses — all must be linked (not embedded), which is exactly what Modrinth metadata
  produces in the `.mrpack`.

## [1.0.0] — 2026-05-20

Initial pack. Minecraft **26.1.2**, Fabric loader **0.19.2**, packwiz format `packwiz:1.1.0`.

43 metadata entries (mods + auto-resolved dependencies). Source = CurseForge unless marked
`(Modrinth)`; Modrinth is used only where no 26.1.2 CurseForge build exists.

### Tier 1 — Foundation
- Fabric API
- Sodium
- Iris Shaders
- Lithium
- FerriteCore *(Modrinth)*
- ImmediatelyFast
- BadOptimizations
- EntityCulling *(Modrinth)*
- Krypton

### Tier 2 — Visual range & quality
- Voxy *(Modrinth)*
- Continuity
- Entity Texture Features (ETF) — pulled as an EMF dependency
- Entity Model Features (EMF)
- Falling Leaves *(Modrinth)*
- Visuality
- Subtle Effects
- Sound Physics Remastered
- AmbientSounds 6

### Tier 3 — Camera, controls, animations
- Camera Utils
- Zoomify *(Modrinth)*
- Not Enough Animations
- First-person Model
- Skin Layers 3D
- Smooth Swapping

### Tier 4 — HUD, UI, utility
- BetterF3
- Mod Menu
- Cloth Config API
- YetAnotherConfigLib (YACL)
- AppleSkin
- WTHIT
- JEI
- Paginated Advancements
- Mouse Wheelie
- Controlling
- Status Effect Bars
- Crash Assistant
- Blur+ *(Modrinth)*

### Tier 5 — Cross-side
- StreamCraft Live `0.8.8+mc26.1.2` *(Modrinth)*

### Auto-resolved dependencies
- bad packets, Fabric Language Kotlin, Fzzy Config, Searchables, Text Placeholder API

### Not yet included — no 26.1.2 build available
- **ModernFix** — load-time / memory fixes
- **Drip Sounds** — cave drip audio
- **Better Third Person** — third-person camera angles
- **Eating Animation** — visual eating
- **InvMove** — walk while inventory is open
- **Auto HUD** — hide HUD on demand

### Notes
- `Voxy World Gen V2` is not a separate mod — Voxy's V2 world generation is a config option
  inside Voxy itself.
- Iris Shaders resolved to a file tagged `mc26.1.1`; CurseForge marks it compatible with
  26.1.2.
