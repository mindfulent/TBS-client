# Changelog — TBS-Client

All notable changes to the TBS-Client modpack.

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
