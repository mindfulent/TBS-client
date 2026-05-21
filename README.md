# TBS-Client

**The Block Survival — Client modpack**

Fabric 1.x modpack for **Minecraft 26.1.2**, built with [packwiz](https://packwiz.infra.link/).

TBS-Client is **purely optional polish** — it is never required to play on The Block Survival.
Any player on stock vanilla 26.1.2 (+ StreamCraft) gets the full gameplay experience: same
world, items, shops, mail, and progression. This pack exists for players who want to dial in
visual fidelity, performance, and quality-of-life for long survival sessions.

Every mod here is **client-side only** and safe against a vanilla server. The single exception
is **StreamCraft Live**, the one mod shared with TBS-Server (see the cross-side contract in
`docs/TBS-mod-strategy.md`).

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
- **Tier 5 — Cross-side:** StreamCraft Live

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

TBS-Client and TBS-Server versions are **decoupled** — the only mod whose version must match
across both packs is **StreamCraft Live**. Coordinate StreamCraft bumps as a synchronized
release of both packs.
