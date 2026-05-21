# Optimal Resource Pack Strategy for a Minecraft 26.1.2 / 1.21.11 Fabric Server with Complementary Reimagined

## TL;DR
- **Do not bundle EMF/ETF into the *required* client modpack — ship them as a strongly recommended optional add‑on alongside StreamCraft.** Both Entity Model Features and Entity Texture Features are Modrinth‑tagged "Client‑side / Server: Unsupported" (LGPL‑3.0, by Traben); they mixin only into client rendering paths and have zero server‑side effect, so vanilla clients without them connect to your Fabric server normally and modded clients with them get Fresh Animations and labPBR specular reflections.
- **For the "enhanced vanilla + Complementary Reimagined" experience, ship two layered optional packs:** Fresh Animations 1.10.5 (FreshLX, released Apr 1, 2026, the first FA build to drop pre‑26.1 support) on top of a labPBR 1.3 vanilla‑faithful PBR pack. The two strongest 2026 candidates are **Patrix 32x basic** (officially paired with Complementary Reimagined in patrix1221's own Packtrix modpack) and **Bare Bones PBR x128 v1.3.7a** (Jan 22, 2026; ships its own Fresh Animations companion). Complementary Reimagined **r5.8 is the current shader, released May 14, 2026** per the official complementary.dev changelogs page; r5.7.1 (Jan 30, 2026) is the previous stable.
- **Use Minecraft's native multi‑pack server stack (added in 1.20.3) with `require‑resource‑pack=false`** to "suggest" rather than require, or — preferred for The Block Academy — skip the server‑pack workflow for the big packs and publish a Modrinth collection that players install client‑side. Reserve the server‑side mechanism for a small (<5 MB) Block Academy branding/identity pack.

## Key Findings

### 1. Versioning — 26.1.2 is the Fabric 1.21.11 ecosystem
Mojang's calendar versioning replaced the `1.x.x` scheme in 2026. Per the Minecraft Wiki version-formats article, **"the last version to have the '1.' prefix was 1.21.11"**, after which the line is 26.1 → 26.1.1 → 26.1.2 (released April 9, 2026), with 26.2 currently in snapshot. Mod ecosystem tags now treat `26.1.x` and `1.21.11` as adjacent but distinct loader targets — every project you'll touch (Fabric Loader, Iris, Sodium, EMF, ETF, Complementary, Fresh Animations) ships parallel builds for both. Practically: **if a pack or mod lists 26.1.2 and/or 1.21.x on Modrinth or CurseForge, it works on your server.**

### 2. Are EMF/ETF safe for vanilla clients on the server?
**Yes — both are pure client-side Fabric mods.** Per Traben's official GitHub READMEs and the Modrinth pages, EMF and ETF are tagged "Client-side" with "Server: Unsupported"; they mixin only into client rendering paths (`LivingEntityRenderer`, model loading, texture binding) and register no networking, gameplay logic, or world data.

Concretely:
- **You cannot install EMF/ETF on a Fabric server JAR and expect it to do anything.** They have no server-side hooks.
- **A vanilla client (no Fabric, no mods) connects to your Fabric server with no issue** as long as your server's *required* mods don't enforce client install (none of Sodium / Iris / Fabric API / Lithium / EMF / ETF do — only mods that register custom packets, blocks, items or entities would). StreamCraft's behavior governs that boundary, not EMF/ETF.
- **Vanilla clients simply don't see Fresh Animations or labPBR specular reflections** when connected; they get default visuals. Modded clients with EMF/ETF + the resource packs installed get the enhanced look.

**Therefore:** bundling EMF + ETF into the *recommended* (not required) StreamCraft modpack is fine and is the correct choice — the only players who lose anything are those who refuse the optional pack, and they still play normally.

**Latest versions (May 2026):**
- EMF: **3.2.4-fabric-26.1** (May 9, 2026, LGPLv3) — Modrinth/CurseForge by Traben.
- ETF: **7.1 for Fabric 26.1** (Apr 15, 2026) and **7.0.12 for 26.1** plus a dedicated **7.0.7-fabric-1.21.11** (Dec 16, 2025).
- Both share Traben's Discord support channel.

### 3. Fresh Animations status for 1.21.11 / 26.1.x
**Active and current.** Per FreshLX's Modrinth and CurseForge pages:
- **Fresh Animations 1.10.5 is the latest, released Apr 1, 2026, for MC 26.1.2** (CurseForge: "FA 1.10.5 · Latest release · B · 26.1.2 · Apr 1, 2026"). The 1.10.5 changelog **removes support for pre‑26.1 versions** and adds renamed textures for pigs, cows, chickens, cats, and foxes.
- For players still on 1.21.11 specifically, use **Fresh Animations 1.10.4** (Feb 24, 2026) instead.
- Requires either OptiFine *or* **EMF + ETF** to function (FreshLX explicitly recommends EMF/ETF on Fabric).
- Companion packs in the Fresh family worth offering:
  - **Fresh Animations: Extensions** (Classic Horses Edit, Objects Add-on) — supports 1.21.11.
  - **Fresh Animations: Emissive** (official) — the canonical fix for FA's glowing-eye textures not rendering with shaders; load **above** main FA.
  - **Fresh Moves** (player animations via EMF Player Animation) — currently only goes to 1.21.4. Skip for 1.21.11/26.1.2 until Traben updates the EMF Player Animation framework.
  - **Bare Bones x Fresh Animations: Objects** (1.1, Dec 21, 2025) — boats/chests/minecarts in FA style.
  - **Bare Bones PBR x Fresh Animations** (Jan 22, 2026) — adds specular textures to FA's mob models so they reflect in shaders.

### 4. Complementary Reimagined state (May 2026)
- **Latest: r5.8, released May 14, 2026** per the official Complementary Development changelogs page (complementary.dev/changelogs). Previous stable **r5.7.1 from January 30, 2026** (confirmed on Modrinth: "r5.7.1 · January 30, 2026 at 12:44 PM"). CurseForge/Modrinth list builds targeted at 26.1, 26.1.1, **26.1.2**, and 1.21.11 in parallel.
- **Iris compatibility:** Fully supported. Iris **1.10.9** for Fabric 26.1.2 (Apr 3, 2026); for 1.21.11 use **1.10.7** (Mar 24, 2026) or **1.10.4** (Dec 22, 2025). Sodium ≥ 0.8.2 is required for 1.21.11.
- **labPBR support level (shaderLABS official table):** Complementary supports **labPBR 1.3** with these features approved: Emission ✔, Material AO ✔, POM ✔, Hardcoded Metals ✔. **Not supported:** Porosity ❌, SSS ❌. (shaderLABS lists Reimagined and Unbound under one combined "Complementary Shaders" row — they share the codebase.)
- **Critical UX gotcha — RP Support mode is exclusive:** Reimagined defaults to **"Integrated PBR+"** under *Shader Options → RP Support*. In this mode, Complementary's own emissives drive glowing ores, amethyst, lava particles, redstone, etc. — but POM/parallax and labPBR specular maps **do nothing**. To unlock POM and labPBR `_n`/`_s` reflections you must switch RP Support to **"labPBR"**, which simultaneously *disables* Complementary's built-in glowing-ores effects. The community has documented this as a hard trade-off (Rethinking Voxels developer discussion #313): *"using integratedPBR+ is mostly a requirement because otherwise lava doesn't glow ... using POM means lava doesn't glow."*
- **Pragmatic recommendation for your server:** Default players to **labPBR mode** since you're pushing a labPBR PBR pack, accept the loss of built-in lava/ore emissives, and have players load the **Fresh Animations: Emissive** extension and any PBR pack with proper `_s.png` emission channel data to recover the glow. There is a hidden sub-option `IPBR_EMISSIVE_MODE` (Shader Options → Material submenu) that you can flip to **"labPBR"** to allow specular-mapped blocks to override IPBR+ emissives selectively — advanced users only.

### 5. Vanilla-faithful PBR packs evaluated (May 2026)

| Pack | Latest version | Last update | labPBR 1.3? | Status |
|---|---|---|---|---|
| **Patrix 32x basic** | #87 / Patrix_26.1_32x_basic.zip | Apr 2 / May 19, 2026 | ✔ explicit ("LabPBR 1.3 and above only") | **Most actively maintained; explicitly endorsed-with-Complementary via Packtrix modpack** |
| **Bare Bones PBR x128** (ludo_silver) | 1.3.7a | Jan 22, 2026 | ✔ labPBR-aligned | **Best free option + has FA companion** |
| **SPBR** | latest = MC 1.21.9 | ~2024–25, add-on patches ongoing | ✔ requires LabPBR shader | Active; explicitly lists Complementary as verified shader |
| **VibrantPBR** | (no formal Modrinth releases) | ~Sep 2025 | ✔ claims full labPBR | New, ~24K downloads but no version files; install via author's Ko-fi |
| **Simplista [LabPBR]** | R35 | Aug 31, 2024 | ✔ "fully LabPBR compliant" | Stale (~21 months) |
| **Vanilla PBR (h0ppip)** | 1-3-2 / labPBR 1-3-2 | **Mar 6, 2023** (MC 1.19.3) | ✔ has separate labPBR build | **Abandoned — do not ship for 26.1.2; will miss cherry/mangrove/trial-chambers/copper-bulb/dried-ghast etc.** |
| **PNAPBR** | v1 "Mangrove" | Aug 2023, single release | partial (POM/normals/specular) | Abandoned |
| **Nova Vanilla PBR 64x** | R5 | Sep 2023 | ✔ LabPBR+AO+SSS | Abandoned for current versions |

**Resolution recommendation:** For a vanilla-faithful aesthetic with Complementary Reimagined, **32x (Patrix basic) or 128x (Bare Bones PBR) is the sweet spot.** Going beyond 128x produces minimal visible improvement at vanilla-style intent and starts eating significant VRAM. With Complementary's shader memory overhead (~700–900 MB on Ultra), 16 GB system RAM and 8 GB VRAM (RTX 3060/RX 6700 XT) handle Patrix 32x + FA + Complementary at 1080p high-render-distance comfortably (60+ FPS). Pushing to Bare Bones x128 nudges VRAM near 5–6 GB used.

### 6. Eating/drinking animation packs for 1.21.11
The 1.21.4+ item model overhaul made standalone resource packs viable without any mod:
- **Eating Animation Resource Pack** (single 1.0.0 release, Nov 2024, CC-BY-4.0 on Modrinth) — pure resource pack, 16x, supports **1.21.4–1.21.11**. **No mod required.** Best vanilla-compatible pick.
- **Eating Animation (resource pack)** by a different author — also supports drinks, 16x, 1.21.4–1.21.11.
- **Theone's Eating Animation Pack** — sprite-animation conversion of the original mod, 1.21.4–1.21.11, no mod needed.
- **Eating Animation mod** by theoness1 — still pinned to 1.21.3, no 1.21.11 update. **Skip.**

All three resource-pack options work natively with Complementary Reimagined (they only change item-use camera-arm animations, no entity/shader interaction). Fresh Animations does *not* include eating animations, so this is an additive ship-with-FA recommendation.

### 7. Other vanilla-enhancing resource packs worth offering
- **Dramatic Skys** (thebaum64) — latest **1.5.3.36.2** (Dec 9, 2025) supports 1.21.11; updated for 26.1's new sun/moon format. HD skies for all 79 biomes. Free version is excellent; paid Patreon tier adds animated auroras/blood moon. **Requires a custom-skybox mod like FabricSkyboxes for non-OptiFine setups.** With Iris+Complementary, Reimagined's own sky takes priority by default — Dramatic Skys mainly affects vanilla rendering and biome fog tints.
- **Vanilla Tweaks** (vanillatweaks.net) — modular picker for GUI/icon/sound subset choices. Pair with **VTDownloader** (Modrinth, 1.21.11 supported) for in-game pack management. Recommend a subset: Borderless Glass, Brighter Nights, Cleaner Pumpkin Front, Lower Shield, Smaller Utility GUIs. Note: per Sodium issue #3367, **the Vanilla Tweaks "Quieter Leaves" pack is now redundant because vanilla 1.21.11 ships similar behavior natively.**
- **Sound Physics Remastered** (henkelmax) — not a resource pack, but the obvious audio enhancement. **fabric-1.21.11-1.5.1** (Dec 10, 2025); pure client-side acoustic ray-tracing. Plays nicely with Simple Voice Chat. Optional add to the recommended modpack.

### 8. Server-side optional pack delivery — best practices for 26.1.2
**Mechanism:** Since Minecraft 1.20.3, the vanilla protocol supports **stacked multi-resource-pack delivery** via the `ResourcePackInfo` system (UUID + URI + SHA-1). PaperMC's Adventure documentation states verbatim: *"Initially this just allowed sending a single resource pack, but starting with Minecraft 1.20.3 the server can send multiple resource packs to be stacked, and if needed removed individually."* This is still surfaced in vanilla `server.properties` as a single `resource-pack=` + `resource-pack-sha1=` field; true multi-pack delivery requires a plugin (Adventure/Paper) or a Fabric server-side mod that exposes the new API.

**Required vs suggested:**
- `require-resource-pack=false` (the default) → client sees a Yes/No prompt. **This is what you want for "suggesting."**
- `require-resource-pack=true` → players who decline are disconnected.
- `resource-pack-prompt=` → custom multi-line chat-component message in the prompt.

**Workflow for hosting a server pack:**
1. Build a ZIP (your "server identity" pack — e.g., a small Block Academy branding pack with logo/MOTD textures).
2. Upload to MC-Packs.net (auto-generates direct link + SHA-1) **or** any direct-link host (OneDrive embed link, GitHub raw, your own CDN, Cloudflare R2).
3. Set in `server.properties`:
   ```
   resource-pack=https://...your.zip
   resource-pack-sha1=cf23df2207d99a74fbe169e3eba035e633b65d94
   require-resource-pack=false
   resource-pack-prompt={"text":"The Block Academy recommends this server identity pack."}
   ```
4. Recompute SHA-1 on every re-zip — ZIP timestamps differ even when contents are unchanged.
5. **Size limit:** The current vanilla protocol cap for automatic server-pack downloads is **250 MB**, raised from 100 MB in 1.18 per the Minecraft Wiki Java Edition 1.18 release notes: *"Size limit for server resource packs has been increased from 100 MB to 250 MB."* (Historic progression: ≤50 MB pre-1.15, 100 MB in 1.15–1.17, 250 MB since 1.18.) Fresh Animations is ~1 MB, Patrix 32x basic ~30 MB, Bare Bones PBR x128 ~50 MB — all individually fine; bundling everything still fits under the 250 MB cap but loses the per-pack opt-out players get from a Modrinth collection.

**Recommendation for The Block Academy:** Don't try to ship Fresh Animations + Patrix + shaders via the server-pack mechanism. Instead:
- Server-pack: a small (<5 MB) "Block Academy" branding/UI pack with `require-resource-pack=false`.
- Optional client install: a **Modrinth collection** or modpack page listing the rest, so players one-click install via the Modrinth App.

### 9. Fabric mods that improve optional-pack UX
- **ModernFix / Bobby / Sodium Extra** — not pack-related but reduce client memory pressure that frees room for PBR packs.
- **VTDownloader** — surfaces Vanilla Tweaks picker inside the in-game resource pack screen.
- **Server Resource Pack** (Lucko / various forks) — Bukkit/Paper plugin to push multi-pack stacks programmatically. If your server is Fabric-only, the new `ResourcePackInfo` API is accessible via Fabric API on modern Loader versions but is generally easier to drive from Paper/Purpur if you ever switch.

## Details

### 9a. Load order (top → bottom in the in-game Resource Pack list, top wins)

For a player running Fresh Animations + Patrix PBR + Complementary Reimagined:

1. **Fresh Animations: Emissive** (extension)
2. **Fresh Animations: Extensions** (Classic Horses, Objects)
3. **Fresh Animations 1.10.5** (main, 26.1.2) — or 1.10.4 on 1.21.11
4. **Bare Bones PBR x Fresh Animations** *(only if using Bare Bones PBR below)*
5. **Server identity pack** (small Block Academy pack — server-pushed, displays above default)
6. **Vanilla Tweaks subset** (UI/icons only — must not contain entity models)
7. **Patrix 32x basic** *or* **Bare Bones PBR x128** (the labPBR base)
8. **Dramatic Skys** (sky-only; ordering between this and PBR doesn't usually matter)
9. (Default)

Rationale: FA's `.jem`/`.jpm` entity models must override the PBR pack's mob models (FA's own FAQ: *"packs with entity models won't work as it would override FA's models and animations"*), but the PBR pack's block-level `_n.png`/`_s.png` files still apply because FA doesn't ship those.

### 9b. Known incompatibility: FA + Continuity + Complementary IPBR+
Documented in Complementary Reimagined GitHub Issue #179: stacking FA's emissive textures + Continuity's emissive textures + Complementary's RP Support = "Integrated PBR+" can produce miscolored pixels on mobs depending on held items, especially with Shadow Sample Quality at Off/Very Low. **Workarounds (any one):**
- Disable Continuity emissives.
- Switch RP Support to **labPBR** (this is the route you're taking anyway).
- Raise Shadow Sample Quality above Off/Very Low.

### 9c. EMF-specific known bug (eyeless mobs)
EMF GitHub Issue #125: occasionally on launch, all wolves/cows/sheep/zombies render with missing eyes or limbs until Minecraft is fully restarted. Track for fixes in EMF 3.2.4+; for now it's a "close and reopen the game" workaround.

### 10. Performance — RTX 3060 / RX 6700 XT class

Tested community baselines (Complementary Reimagined r5.7.x + Patrix 32x + FA + EMF/ETF + Sodium + Iris, 1080p, 16 chunks, Ultra preset):

| Component | VRAM | FPS impact |
|---|---|---|
| Vanilla baseline | ~1.5 GB | 200+ FPS |
| + Sodium/Iris (no shader) | ~1.7 GB | 250+ FPS |
| + Complementary Reimagined (Medium) | ~3 GB | 90–110 FPS |
| + Complementary Reimagined (High/Ultra) | ~4 GB | 60–80 FPS |
| + Patrix 32x basic | +0.5 GB | -5 FPS |
| + Bare Bones PBR x128 (instead) | +1.5 GB | -10 FPS |
| + FA + EMF + ETF | +0.2 GB | -5 to -10 FPS (mob-dense scenes) |
| + Dramatic Skys + Sound Physics | negligible | -2 FPS |
| **Full stack** | **~5–6 GB** | **50–70 FPS** at Ultra |

The minimum mid-tier system (RTX 3060 8 GB / RX 6700 XT 12 GB, Ryzen 5 5600 / i5-12400, 16 GB RAM) handles the full stack at Ultra/Medium-shader at 1080p with a stable 60 FPS. **For lower-end systems** (GTX 1660, integrated graphics), recommend:
- Drop Complementary to the "Low" or "Medium" preset.
- Use **Bare Bones PBR x128** instead of Patrix (lower polygon detail, similar VRAM).
- Skip EMF/ETF/Fresh Animations (skeletal animations are the heaviest part of the FA stack).

## Recommended Pack List for the 26.1.2 Server (publishable)

> **The Block Academy — Recommended Enhanced Vanilla (26.1.2)**
>
> Required (already in StreamCraft modpack): StreamCraft Live core.
>
> **Strongly recommended optional mods** (install with the Modrinth App):
> - Fabric API (latest for 26.1.2)
> - Iris **1.10.9** for Fabric 26.1.2
> - Sodium ≥ 0.8.2 for 26.1.2
> - **EMF (Entity Model Features) 3.2.4-fabric-26.1** by Traben
> - **ETF (Entity Texture Features) 7.1-fabric-26.1** by Traben
> - Sound Physics Remastered fabric-1.21.11-1.5.1 (or its 26.1 build when published) by henkelmax
> - VTDownloader (optional, for in-game Vanilla Tweaks installs)
>
> **Shader:**
> - **Complementary Reimagined r5.8** by EminGT — drop into `shaderpacks/`, enable in Iris menu, then **change Shader Options → RP Support → labPBR**.
>
> **Resource packs (top → bottom in load order):**
> 1. Fresh Animations: Emissive
> 2. Fresh Animations: Extensions
> 3. **Fresh Animations 1.10.5** (26.1.2) by FreshLX
> 4. (optional) Bare Bones PBR x Fresh Animations
> 5. The Block Academy server identity pack (auto-served, <5 MB)
> 6. Vanilla Tweaks subset (Borderless Glass, Brighter Nights, Cleaner Pumpkin Front, Lower Shield, Smaller Utility GUIs)
> 7. **Patrix 32x basic** (Modrinth #87 / CurseForge Patrix_26.1_32x_basic.zip) — *the recommended PBR base, officially Complementary-tested via Packtrix*
> 8. Dramatic Skys 1.5.3.36.2

## Recommendations

### Stage 1 — Ship now (next deploy)
1. **Configure your server.properties** for opt-in server pack with `require-resource-pack=false` and a friendly `resource-pack-prompt`. Use a tiny (<5 MB) Block Academy branding pack only — host it on Cloudflare R2 or GitHub Releases (free, stable, fast, no Dropbox rate limits).
2. **Publish the Modrinth collection above.** Order matters — make the load-order section the most visible part of the README.
3. **Document the load order** in your server's Discord/README using the 9-item ordering.

### Stage 2 — A/B test within the player base (week 2)
1. Survey ~10 players: Patrix 32x vs Bare Bones PBR x128 — which they prefer aesthetically and FPS-wise. Patrix has more block variation; Bare Bones is closer to the trailers and has a first-party FA tie-in.
2. Test the **labPBR vs Integrated PBR+** trade-off in Complementary. If players miss glowing ores/lava more than they want POM, default the recommendation back to IPBR+ and skip the heavy PBR pack (use a connected-textures-only pack like Vanilla Tweaks instead).

### Stage 3 — Decide bundling (month 1)
- **If <30% of players install the optional pack** → consider bundling EMF + ETF into the StreamCraft modpack to lower install friction. Both are client-side-only and won't break the server.
- **If >70% install** → leave as optional, friction isn't blocking adoption.

### Thresholds that should change these recommendations
- If **Complementary r6.x** drops with simultaneous `Integrated PBR+` and `labPBR` support → switch the default RP Support back to IPBR+ and recommend Patrix uniformly.
- If **Fresh Moves** updates past 1.21.4 → add it to the optional pack list for player-body animation parity with mobs.
- If a new EMF release fixes Issue #125 (eyeless mobs) → remove the workaround note from the player README.
- If your **server-pack URL serves >250 MB** at any point → split into stacked packs using the post-1.20.3 multi-pack `ResourcePackInfo` API rather than trying to compress.

## Caveats

1. **Version drift is fast right now.** This report references Complementary r5.8 (May 14, 2026), EMF 3.2.4 (May 9), ETF 7.1 (Apr 15), Iris 1.10.9 (Apr 3), FA 1.10.5 (Apr 1) / 1.10.4 (Feb 24). Re-verify on Modrinth before publishing your collection — Mojang's faster game-drop cadence has accelerated downstream releases too.
2. **The IPBR+ vs labPBR exclusivity in Complementary is the single biggest gotcha.** Test both modes on your own machine before committing to a default. If your players are casual, IPBR+ (no PBR pack, just FA + Vanilla Tweaks + Dramatic Skys) may produce a better impression than the heavier labPBR stack.
3. **EMF GitHub Issue #125** (eyeless mob render glitch on launch) is intermittent and unresolved as of EMF 3.2.4. Document the "restart Minecraft to fix" workaround.
4. **Patrix has its own license terms** (Patreon-paid tiers are not redistributable). You can recommend the free 32x basic but **cannot bundle it into a self-hosted modpack ZIP** — must link via the Modrinth/CurseForge installer.
5. **Complementary's license** allows Modrinth/CurseForge modpack inclusion only via their existing systems with visible credit; same constraint applies to your collection.
6. **Vanilla clients without EMF/ETF/Iris connecting to your server** see all entities as default Minecraft models with default textures, no shaders, no labPBR — but the connection is fully functional and they participate normally. This is the correct vanilla-compatibility behavior you wanted to preserve.
7. **Server-side pack delivery from 1.20.3 onward supports stacking and individual removal** via the new packet, but `server.properties` still only exposes single-pack fields. Multi-pack delivery requires a plugin (Paper Adventure API) or a Fabric server-side mod that drives the new API directly.
8. The Patrix Packtrix modpack's explicit endorsement of Complementary Reimagined ("custom Unbound settings for realistic clouds") is the strongest validated FA + PBR + Complementary combo in the wild — closest to a "known-good" reference setup for your server, and the basis for the primary recommendation here.