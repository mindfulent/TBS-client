# TBS-Client

**The Block Survival — Client modpack**

Fabric 1.x modpack for **Minecraft 26.1.2**, built with [packwiz](https://packwiz.infra.link/).

TBS-Client is **purely optional polish** — it is never required to play on The Block Survival.
Any player on stock vanilla 26.1.2 (+ StreamCraft) gets the full gameplay experience: same
world, items, shops, mail, and progression. This pack exists for players who want to dial in
visual fidelity, performance, and quality-of-life for long survival sessions.

Every mod here is safe against a vanilla server. Two mods — **StreamCraft Live** and
**Simple Voice Chat** — are shared with TBS-Server; both are optional per player, so a
vanilla client without them still connects and plays the full game (see the cross-side
contract in `docs/TBS-mod-strategy.md`).

## Install

| Launcher | How |
|----------|-----|
| Prism Launcher | Import the `TBS-Client-X.Y.Z.mrpack` release file |
| CurseForge App | Import the exported `.zip` |

## Build / maintenance

```bash
./packwiz.exe cf install <mod-slug> -y   # add a mod from CurseForge (preferred)
./packwiz.exe mr install <mod-slug> -y   # Modrinth fallback (no CF 26.1.2 build)
./packwiz.exe update --all               # update every mod
./packwiz.exe refresh                     # rebuild index.toml after manual edits
./packwiz.exe modrinth export             # produce TBS-Client-X.Y.Z.mrpack
```

CurseForge is always tried first to stay compliant with the CurseForge distribution policy;
Modrinth is used only when a mod has no CurseForge build for 26.1.2.

## Mod tiers

Mods follow the five-tier layout from the strategy doc. See `CHANGELOG.md` for the exact
resolved state of every mod, and `docs/TBS-mod-strategy.md` for the full design rationale.

- **Tier 1 — Foundation:** Fabric API, Sodium, Iris Shaders, Lithium, FerriteCore,
  ImmediatelyFast, BadOptimizations, EntityCulling, Krypton
- **Tier 2 — Visual range & quality:** Voxy, Continuity, ETF + EMF, Falling Leaves,
  Visuality, Subtle Effects, Sound Physics Remastered, AmbientSounds
- **Tier 3 — Camera, controls, animations:** Camera Utils, Zoomify, Not Enough Animations,
  First-person Model, Skin Layers 3D, Smooth Swapping
- **Tier 4 — HUD, UI, utility:** BetterF3, Mod Menu, Cloth Config + YACL, AppleSkin, WTHIT,
  JEI, Paginated Advancements, Mouse Wheelie, Controlling, Status Effect Bars,
  Crash Assistant, Blur+
- **Tier 5 — Cross-side:** StreamCraft Live, Simple Voice Chat

## Resource packs & shader

TBS-Client also ships an **optional visual layer** — a shader plus a set of resource
packs — as packwiz *optional* entries (`[option] optional = true`). They are embedded in
the exported `.mrpack` only as Modrinth URL references, and appear as per-player toggles
when you import the pack in Prism Launcher or the CurseForge App. None of it is required;
leave it all off for a lighter client. See `docs/resource-packs.md` for the full rationale.

| Pack | Default | Notes |
|------|---------|-------|
| Complementary Shaders - Reimagined `r5.8` | off | Iris shader. After enabling, open **Shader Options → RP Support → labPBR** to unlock POM and the PBR pack's reflections. |
| Patrix 32x | off | 32x labPBR resource pack — adds PBR depth under the shader. |
| Fresh Animations `v1.10.5` | on | Smooth entity animations. Driven by the bundled **EMF + ETF**. |
| Fresh Animations: Emissive | on | Restores Fresh Animations glowing-eye textures under shaders. |
| Fresh Animations: Extensions | on | Extra Fresh Animations models (Classic Horses, Objects). |

**In-game resource-pack load order** (top wins, top → bottom):

1. Fresh Animations: Emissive
2. Fresh Animations: Extensions
3. Fresh Animations
4. Patrix 32x

The Fresh Animations packs must sit above Patrix so FA's entity models take priority;
Patrix's block-level PBR textures still apply underneath. The shader is selected
separately in the Iris menu, not the resource-pack list.

**Performance:** the full stack (shader + Patrix + Fresh Animations) targets roughly an
RTX 3060 / 8 GB-VRAM-class machine at ~60 FPS / 1080p. On weaker hardware, drop
Complementary to a lower preset or leave the shader and PBR pack off.

## Pending mods

These mods from the strategy doc have **no 26.1.2 build** on CurseForge or Modrinth yet and
will be added once builds appear:

- **ModernFix** — load-time / memory fixes
- **Drip Sounds** — cave drip audio
- **Better Third Person** — third-person camera angles
- **Eating Animation** — visual eating
- **InvMove** — walk while inventory is open
- **Auto HUD** — hide HUD on demand

`Voxy World Gen V2` from the doc is not a separate project — Voxy's V2 world generation is a
setting inside Voxy's own config, enabled in-game.

## Version coupling

TBS-Client and TBS-Server versions are **decoupled** — the mods whose versions must match
across both packs are **StreamCraft Live** and **Simple Voice Chat**. Coordinate bumps of
either as a synchronized release of both packs.
