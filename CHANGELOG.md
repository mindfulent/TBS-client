# Changelog — TBS-Client

All notable changes to the TBS-Client modpack.

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
