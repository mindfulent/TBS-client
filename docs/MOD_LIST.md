# TheBlockSurvival — mod list

Reference for every entry tracked by packwiz in this pack. Source of truth is the
`.pw.toml` files under `mods/`, `shaderpacks/`, and `resourcepacks/` — when those
change, this doc should be updated alongside `README.md` and `CHANGELOG.md`.

- Tier rationale: [`TBS-mod-strategy.md`](TBS-mod-strategy.md)
- Shader / resource-pack stack: [`resource-packs.md`](resource-packs.md)
- CurseForge build differences: see the v1.1.2 entry in [`../CHANGELOG.md`](../CHANGELOG.md)
- Target: **Minecraft 26.1.2 (Fabric 1.x)**
- Pack version: see [`pack.toml`](../pack.toml)

**Totals (canonical / Windows variant):** 46 mods · 1 shader · 4 resource packs
= **51 packwiz entries**.

All mods are `side = "client"` except **StreamCraft Live** and **Simple Voice
Chat**, which are `side = "both"` (cross-side with TBS-Server, must match
versions). Reference links resolve to the project page on the listed source;
CurseForge project-ID URLs redirect to the canonical slug.

## Tier 1 — Foundation (performance & API base)

| Mod | Source | Filename |
|---|---|---|
| [Fabric API](https://modrinth.com/mod/P7dR8mSH) | Modrinth | `fabric-api-0.149.1+26.1.2.jar` |
| [Sodium](https://modrinth.com/mod/AANobbMI) | Modrinth | `sodium-fabric-0.8.11+mc26.1.2.jar` |
| [Iris Shaders](https://www.curseforge.com/projects/455508) | CurseForge | `iris-fabric-1.10.9+mc26.1.1.jar` |
| [Lithium](https://www.curseforge.com/projects/360438) | CurseForge | `lithium-fabric-0.24.2+mc26.1.2.jar` |
| [FerriteCore](https://modrinth.com/mod/uXXizFIs) | Modrinth | `ferritecore-9.0.0-fabric.jar` |
| [ImmediatelyFast](https://www.curseforge.com/projects/686911) | CurseForge | `ImmediatelyFast-Fabric-1.15.2+26.1.2.jar` |
| [BadOptimizations](https://www.curseforge.com/projects/949555) | CurseForge | `BadOptimizations-2.4.1-26.1-fabric.jar` |
| [Entity Culling](https://modrinth.com/mod/NNAgCjsB) | Modrinth | `entityculling-fabric-1.10.2-mc26.1.jar` |
| [Krypton](https://www.curseforge.com/projects/428912) | CurseForge | `krypton-0.3.0.jar` |

## Tier 2 — Visual range & quality

| Mod | Source | Filename |
|---|---|---|
| [Voxy](https://modrinth.com/mod/fxxUqruK) | Modrinth | `voxy-0.2.15-beta+26.1.jar` |
| [Continuity](https://www.curseforge.com/projects/531351) | CurseForge | `continuity-3.0.1-beta.2+26.1.jar` |
| [ETF — Entity Texture Features](https://www.curseforge.com/projects/568563) | CurseForge | `entity_texture_features_26.1-fabric-7.1.jar` |
| [EMF — Entity Model Features](https://www.curseforge.com/projects/844662) | CurseForge | `entity_model_features-3.2.4-26.1-fabric.jar` |
| [Falling Leaves](https://modrinth.com/mod/WhbRG4iK) | Modrinth | `fallingleaves-2.0.6+26.1.jar` |
| [Visuality](https://www.curseforge.com/projects/521126) | CurseForge | `visuality-0.7.13+26.1.jar` |
| [Subtle Effects](https://modrinth.com/mod/4q8UOK1d) | Modrinth | `SubtleEffects-fabric-26.1-1.14.3.jar` |
| [Sound Physics Remastered](https://www.curseforge.com/projects/535489) | CurseForge | `sound-physics-remastered-fabric-1.5.1+26.1.2.jar` |
| [AmbientSounds 6](https://www.curseforge.com/projects/254284) | CurseForge | `AmbientSounds_FABRIC_v6.3.6_mc26.1.2.jar` |

## Tier 3 — Camera, controls, animations

| Mod | Source | Filename |
|---|---|---|
| [Camera Utils](https://modrinth.com/mod/rrwQMaWQ) | Modrinth | `camerautils-fabric-1.1.2+26.1.2.jar` |
| [Zoomify](https://modrinth.com/mod/w7ThoJFB) | Modrinth | `zoomify-2.16.0+26.1.jar` |
| [Not Enough Animations](https://modrinth.com/mod/MPCX6s5C) | Modrinth | `notenoughanimations-fabric-1.12.3-mc26.1.jar` |
| [First-person Model](https://modrinth.com/mod/H5XMjpHi) | Modrinth | `firstperson-fabric-2.7.1-mc26.1.jar` |
| [3D Skin Layers](https://modrinth.com/mod/zV5r3pPn) | Modrinth | `skinlayers3d-fabric-1.11.1-mc26.1.jar` |
| [Smooth Swapping](https://www.curseforge.com/projects/513689) | CurseForge | `smoothswapping-0.9.9-26.1-fabric.jar` |

## Tier 4 — HUD, UI, utility

| Mod | Source | Filename |
|---|---|---|
| [BetterF3](https://www.curseforge.com/projects/401648) | CurseForge | `BetterF3-18.0.2-Fabric-26.1.jar` |
| [Mod Menu](https://www.curseforge.com/projects/308702) | CurseForge | `modmenu-18.0.0-beta.1.jar` |
| [Cloth Config API](https://modrinth.com/mod/9s6osm5g) | Modrinth | `cloth-config-26.1.154.jar` |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/mod/1eAoo2KR) | Modrinth | `yet_another_config_lib_v3-3.9.3+26.1-fabric.jar` |
| [AppleSkin](https://www.curseforge.com/projects/248787) | CurseForge | `appleskin-fabric-mc26.1-3.0.9.jar` |
| [WTHIT](https://modrinth.com/mod/6AQIaxuO) | Modrinth | `wthit-26.1-fabric-19.0.1.jar` |
| [Just Enough Items (JEI)](https://www.curseforge.com/projects/238222) | CurseForge | `jei-26.1.2-fabric-29.6.2.31.jar` |
| [Paginated Advancements & Custom Frames](https://www.curseforge.com/projects/618770) | CurseForge | `paginatedadvancements-2.8.0+26.1.jar` |
| [Mouse Wheelie](https://www.curseforge.com/projects/317514) | CurseForge | `mouse-wheelie-1.16.2+mc26.1.jar` |
| [Controlling](https://www.curseforge.com/projects/250398) | CurseForge | `Controlling-fabric-26.1.2-26.1.2.3.jar` |
| [Status Effect Bars](https://www.curseforge.com/projects/615459) | CurseForge | `status-effect-bars-1.0.11.jar` |
| [Crash Assistant](https://modrinth.com/mod/ix1qq8Ux) | Modrinth | `CrashAssistant-fabric-26.1-1.11.9.jar` |
| [Blur+](https://modrinth.com/mod/NK39zBp2) | Modrinth | `blur-fabric-6.2.0+26.1.jar` |
| [Cubes Without Borders](https://www.curseforge.com/projects/975120) | CurseForge | `cwb-4.0.3+26.1.jar` |

> **Cubes Without Borders** (v1.1.4) keeps Minecraft in borderless fullscreen
> when focus shifts to another app — useful for streamers on a multi-monitor
> setup so OBS / Discord / a browser don't minimize the game and break the
> stream. Modrinth fallback: [`ETlrkaYF`](https://modrinth.com/mod/ETlrkaYF).

## Tier 5 — Cross-side (shared with TBS-Server, must match versions)

| Mod | Side | Source | Filename |
|---|---|---|---|
| [StreamCraft Live](https://modrinth.com/mod/UUUunIAe) | both | Modrinth | `streamcraft-0.12.9+mc26.1.2.jar` |
| [Simple Voice Chat](https://modrinth.com/mod/9eGKb6K1) | both | Modrinth | `voicechat-fabric-2.6.17+26.1.2.jar` |

Both are optional per player — a vanilla client without them still connects and
plays. StreamCraft Live ships per-OS native-libs variants; the canonical pack
references the Windows build and `scripts/publish.py` overlays the matching
`streamcraft-live.pw.toml` from `scripts/platform-sources/<variant>/` when
producing the macOS / Linux `.mrpack` files.

## Library dependencies (not in a named tier)

Required by mods above.

| Mod | Source | Filename |
|---|---|---|
| [Fabric Language Kotlin](https://modrinth.com/mod/Ha28R6CL) | Modrinth | `fabric-language-kotlin-1.13.11+kotlin.2.3.21.jar` |
| [bad packets](https://www.curseforge.com/projects/615134) | CurseForge | `badpackets-fabric-0.12.2.jar` |
| [CreativeCore](https://www.curseforge.com/projects/257814) | CurseForge | `CreativeCore_FABRIC_v2.14.14_mc26.1.2.jar` |
| [Searchables](https://www.curseforge.com/projects/858542) | CurseForge | `Searchables-fabric-26.1.2-1.0.1.jar` |
| [Fzzy Config](https://modrinth.com/mod/hYykXjDp) | Modrinth | `fzzy_config-0.7.6+26.1.jar` |
| [Text Placeholder API](https://www.curseforge.com/projects/1037459) | CurseForge | `placeholder-api-3.0.0+26.1.jar` |

## Shaders

Optional packwiz entries — toggleable per player at import time.

| Pack | Default | Source | Filename |
|---|---|---|---|
| [Complementary Shaders — Reimagined](https://modrinth.com/shader/HVnmMxH1) | off | Modrinth | `ComplementaryReimagined_r5.8.zip` |

## Resource packs

Optional packwiz entries. In-game load order (top wins) is
**Emissive → Extensions → Fresh Animations → Patrix** — see [`resource-packs.md`](resource-packs.md).

| Pack | Default | Source | Filename |
|---|---|---|---|
| [Fresh Animations](https://modrinth.com/resourcepack/50dA9Sha) | on | Modrinth | `FreshAnimations_v1.10.5.zip` |
| [Fresh Animations: Emissive](https://modrinth.com/resourcepack/VRS2YQn9) | on | Modrinth | `FA+Emissive-v1.6.zip` |
| [Fresh Animations: Extensions](https://modrinth.com/resourcepack/YAVTU8mK) | on | Modrinth | `FA+All_Extensions-v1.9.zip` |
| [Patrix 32x](https://modrinth.com/resourcepack/olO1TaXd) | off | Modrinth | `Patrix_26.1_32x_basic.zip` |

## CurseForge build exclusions

`scripts/publish.py` drops the following from the CurseForge `.zip` build (the
canonical Modrinth `.mrpack` keeps them all). Reasons in the v1.1.2 entry of
[`../CHANGELOG.md`](../CHANGELOG.md):

- **Voxy** — CurseForge policy prohibits redistribution
- **Complementary Shaders — Reimagined** — custom license, not redistributable
- **Fresh Animations** (main + Emissive + Extensions) — custom / ARR licenses

Patrix 32x stays in the CurseForge build via a CF-source overlay in
`scripts/cf-sources/resourcepacks/`.

## Pending — no 26.1.2 build yet

From [`TBS-mod-strategy.md`](TBS-mod-strategy.md). Will be added once builds
appear on CurseForge or Modrinth:

- **ModernFix** — load-time / memory fixes
- **Drip Sounds** — cave drip audio
- **Better Third Person** — third-person camera angles
- **Eating Animation** — visual eating
- **InvMove** — walk while inventory is open
- **Auto HUD** — hide HUD on demand

`Voxy World Gen V2` from the strategy doc is not a separate project — it is a
config flag inside Voxy itself, enabled in-game.
