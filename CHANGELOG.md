# Changelog — TheBlockSurvival

All notable changes to the TheBlockSurvival client modpack (formerly TBS-Client).

## [1.2.0] — 2026-06-09

**StreamCraft Live 0.9.9 → 0.12.1.** The first big cross-side update since voice moved out of
Simple Voice Chat — in-world voice now lives in StreamCraft, alongside native Linux capture,
Display Block upgrades, and a new Terms/age gate. Lockstep release with TBS-Server 1.2.0.

- Repinned **StreamCraft Live → 0.12.1+mc26.1.2** (Modrinth `DEgY8AQ8`) across the base pack
  and all four platform-source variants (linux, linux-aarch64, macos-arm64, macos-x86_64);
  the CurseForge swap repinned to CF file `8224184`.
- StreamCraft highlights since 0.9.9: in-world **voice chat** (open-mic / push-to-talk /
  voice-activated, per-player volume, echo cancellation & noise suppression); **native Linux**
  webcam, screen, and audio capture (manually tested on Fedora GNOME + Arch KDE Plasma);
  Display Block **auto-crop black bars / pixel-precise placement / opaque backdrops**; macOS
  capture-stall fixes; and a first-run **Terms of Use & age gate** before camera/screen/voice.
- No other mod added, removed, or changed. Run the **same StreamCraft version on client and
  server** — both packs ship 0.12.1.

### Default-options seeding hotfix (2026-06-09)

The initial 1.2.0 build shipped with two seeded defaults failing to apply on a fresh
install: the **direct-connect TheBlockSurvival server entry** and the **Open Parties and
Claims menu keybind** (`;`). Corrected in-place — assets re-uploaded, no version bump. The
**minimap default was unaffected** and continued to apply.

- The seeded `config/defaultoptions/extra/servers.dat` was being stripped from the export:
  an unanchored `servers.dat` rule in `.packwizignore`/`.gitignore` matched at any depth
  (packwiz uses gitignore semantics) and deleted it. Anchored both rules to `/servers.dat`
  so they only match the maintainer's local list at the pack root.
- Keybind defaults lived in `config/defaultoptions/options.txt`, which the Default Options
  mod does not apply to keymappings (it has a dedicated handler). Moved them to
  `config/defaultoptions/keybindings.txt` and removed the dead `options.txt`.
- Resolved keybind conflicts in the seeded defaults: Xaero **Open Map** `M → N` (M was
  colliding with StreamCraft's mute, which defaults to M); Xaero **Toggle Minimap** `→ K`;
  Iris **Toggle Shaders** and **Reload Shaders** unbound (K is now the minimap toggle, and
  stray shader reloads are off). OPAC menu stays on `;`.

## [1.1.13] — 2026-05-31

**Removed Simple Voice Chat** (`2.6.17`) from the pack. Proximity voice is consolidating
into **StreamCraft Live** — use StreamCraft for in-game voice going forward.

- Removed `mods/simple-voice-chat.pw.toml` (canonical Modrinth entry) and its CurseForge
  reference swap (`scripts/cf-sources/mods/simple-voice-chat.pw.toml`).
- **StreamCraft Live is once again the only cross-side (`both`) mod** — reverts the
  second-cross-side-mod exception that v1.0.1 introduced when SVC was added.
- Lockstep release with TBS-Server 1.1.13.

### CurseForge build hotfix (2026-05-31)

The CurseForge `.zip` (all platform variants) crashed at launch with
`Incompatible mods found! … Replace mod 'Zoomify' 2.15.2+1.21.11 with any version
compatible with minecraft 26.1.2`. The **Modrinth `.mrpack` was never affected** — this
was a CurseForge-packaging-only bug, so no pack-content change and no version bump.

Cause: two `scripts/cf-sources/` CurseForge swaps had gone stale. CurseForge still hosted
only the older `+1.21.11` build of each mod while the canonical Modrinth source had already
moved to the `+26.1` build, so the CF `.zip` shipped a jar whose `fabric.mod.json` requires
Minecraft `<1.22` — which the 26.1.2 runtime does not satisfy, aborting the whole pack.

- Dropped `scripts/cf-sources/mods/zoomify.pw.toml` and `scripts/cf-sources/mods/blur-plus.pw.toml`.
  Both mods now ride in the CurseForge `.zip` as bundled `+26.1` overrides (same jars the
  Modrinth build uses) instead of stale CurseForge manifest references. Re-add each swap once
  CurseForge publishes a 26.1.2 build.
- Added a **stale-swap guard** to `scripts/publish.py`: the CurseForge export now fails fast
  (offline, no CF API) when a swapped CurseForge jar's filename lacks the pack's MC version
  token that the canonical Modrinth jar carries — preventing this class of silent breakage.

## [1.1.12] — 2026-05-31

**Adds Xaero's maps** so the Open Parties and Claims overlay works — claims drawn
on the minimap + fullscreen map, with right-click-to-claim on the world map.

**Client mod changes:**
- **Added Xaero's Minimap** `25.3.14` *(Modrinth — ARR, URL-referenced)*,
  `side = "client"`.
- **Added Xaero's World Map** `1.40.18` *(Modrinth — ARR, URL-referenced)*,
  `side = "client"`. Both are client-side-only and safe on any vanilla server.

**Survival-friendly defaults (entity radar + cave maps OFF):** the Fair-play
edition is discontinued (no 26.1.2 build), so we use the regular Minimap with a
shipped default that disables **entity radar** and **cave maps** —
`config/xaerominimap.txt` (`entityRadar:false`, `caveMaps:0`), delivered via Default
Options' `extra/` folder so it applies **only on a fresh install** and never
overwrites an existing config.

> **Not enforced + verify on first launch.** Without a Xaero server companion these
> are *defaults*, not server-enforced — a player can re-enable radar/cave in the
> Y → settings menu. And because the keys can't be runtime-verified here, confirm on
> a fresh install: if radar/cave are still on, toggle them off in-game (Y menu) and
> let us know so we can correct the shipped default.

**CurseForge build note:** Xaero's Minimap + World Map (and Default Options + Balm)
are excluded from the CurseForge `.zip` (ARR). CF-app users install Xaero's Minimap
+ World Map directly from CurseForge (one click). The Modrinth `.mrpack` includes
everything.

## [1.1.11] — 2026-05-31

**Lockstep sync with TBS-Server 1.1.11.** Brings the **Open Parties and Claims**
client to TheBlockSurvival so residents get the in-game claim UI + Xaero map
overlay (the server has run OPAC server-side since 1.1.10 — vanilla clients still
manage claims via chat commands).

**Client mod changes:**
- **Added Open Parties and Claims** `0.26.3` *(CurseForge project `636608`, file
  `8091537`)* — native 26.1.2 build, `side = "client"`. Opens the claim/party UI
  and draws claims on Xaero's maps. Dependency **Forge Config API Port** added
  *(CurseForge project `547434`)*, also `side = "client"`.
- **Added Default Options** `26.1.0.1` *(Modrinth — ARR, URL-referenced for
  redistribution compliance)* + its dependency **Balm** `26.1.2.6` *(Modrinth)*.
  Sole purpose: ship a non-destructive keybind default.

**Default keybind:** OPAC's menu key defaults to **semicolon (`;`)** instead of its
built-in apostrophe (`'`), via `config/defaultoptions/options.txt`
(`key_gui.xaero_pac_key_open_menu:key.keyboard.semicolon`). Default Options applies
this only on a fresh install / when the key is unset — it never overrides a binding
you've already chosen, so existing installs keep whatever they have set (rebind in
Controls → "Open Parties and Claims Menu" if you want semicolon).

**CurseForge build note:** Default Options + Balm are excluded from the CurseForge
`.zip` (ARR license) — CF-app users get the OPAC client but keep the apostrophe
default unless they install Default Options + Balm themselves, or rebind manually.
The Modrinth `.mrpack` includes everything.

## [1.1.10] — 2026-05-31

**No client mod changes.** Version aligned with TBS-Server 1.1.10 per the lockstep
policy. The server gained **Open Parties and Claims** (Tier S5) for anti-theft chunk
claims — protection is server-enforced and driven entirely by chat commands
(`/openpac-claims`, `/openpac-parties`, `/opm`), so vanilla and modded clients alike
need nothing installed. (The OPAC client mod — claim UI + Xaero map overlay — is a
possible future addition here, not shipped in this release.)

## [1.1.9] — 2026-05-30

**Lockstep sync with TBS-Server 1.1.9.** The server gained **Sit Anywhere!**
(Tier S5 gameplay augment) — a server-side, vanilla-client-safe sitting mod
(datapack logic in a Fabric wrapper, no new client-visible content). Nothing to
install client-side for sitting: vanilla and modded players alike can right-click
stairs/slabs to sit once running the 1.1.9 server.

**Client mod changes:**
- **Removed Cubes Without Borders** (`cwb-4.0.3+26.1.jar`) — was Tier 4
  (HUD/UI/utility).
- **Added Bridging Mod** `2.6.6+26.1` *(CurseForge project `533942`, file
  `7915819`)* — bridging assist / placement helper, Tier 3 (camera, controls,
  animations). Client-side QoL.

**Dependency re-sourcing (CurseForge-first compliance):**
- **Fabric API** and **YACL (YetAnotherConfigLib)** re-sourced from Modrinth to
  CurseForge (now `mode = "metadata:curseforge"`), matching the pack's
  CurseForge-first policy. Same mods, same function — distribution source only.

## [1.1.8] — 2026-05-30

**No client mod changes.** Version aligned with TBS-Server 1.1.8 per the lockstep
policy. The real fix lands server-side: JEI is now installed on TBS-Server so it
can sync recipes to the JEI already in this client pack. Since MC 1.21.2 recipes
are held server-side, JEI on the client alone reported "missing recipes" until the
server gained a matching JEI build (`26.1.2-fabric-29.6.2.31`, identical to this
pack's copy). No action needed by players beyond running the 1.1.8 server.

## [1.1.7] — 2026-05-28

**Updated:**
- **StreamCraft Live** `0.8.25+mc26.1.2` → `0.9.9+mc26.1.2`. Brings in "the Adi branch"
  — a rollup release covering everything between v0.8.25 and v0.9.9. Headline changes
  most visible on TBS:
  - New custom Windows capture DLL (`libstreamcraft_windows.dll`) — Media Foundation
    webcam + Windows Graphics Capture screen, replacing the legacy Video for Windows +
    GDI BitBlt path. Real failure messages ("Camera failed: device busy /
    permission denied") instead of silent fails.
  - Borderless-fullscreen mod compat — Cubes Without Borders, Optifine borderless, etc.
    desktop streaming now works under those window modes.
  - Late-joining viewers reliably hear desktop audio without the publisher having to
    toggle Desktop Audio off/on.
  - 1.21.6+ audio receiver fix — Mac (or any) viewer hears PC publishers correctly.
  - Display Block crafting recipe — iron in corners, glass panes on edges, redstone in
    center. Survival players no longer need `/give` or Creative.
  - Display Block source-selector fix — the "block won't switch to me even though I'm
    sharing" trap is resolved.
  - Screen-share click-before-connect race fix — clicking Share Screen before LiveKit
    finishes connecting now works.
  - New in-mod Support + Backers screen — coral ♥ icon in the main menu footer
    between How it works and Settings.

  `PROTOCOL_VERSION` unchanged — v0.9.9 clients connect cleanly to any v0.8.x or v0.9.x
  server. TBS-Server is upgraded synchronously in TBS-server v1.0.7.

No other mod added, removed, or updated. Mod count unchanged.

## [1.1.6] — 2026-05-23

**Added:**
- **Pre-configured server list entry** — `TheBlockSurvival → theblocksurvival.com`
  ships in `servers.dat` at the pack root, so players see the official server in
  their multiplayer list on first launch. Mirrors the pattern used by the TBA pack
  (`join.theblock.academy`).

No mod added, removed, or updated. Mod count is 51.

## [1.1.5] — 2026-05-23

## Addressing the v1.1.4 rejection

Thanks for the moderation review on v1.1.4 — you flagged three CurseForge-hosted
mods that were shipping as override jars instead of `manifest.json` references:

- `overrides/mods/blur-fabric-6.2.0+26.1.jar`
- `overrides/mods/entityculling-fabric-1.10.2-mc26.1.jar`
- `overrides/mods/voicechat-fabric-2.6.17+26.1.2.jar`

All three are now properly referenced in `manifest.json` by their CurseForge
project + file IDs (Blur+ 393563/7655028, Entity Culling 448233/8053788, Simple
Voice Chat 416089/8037825). The exported `.zip` ships zero CurseForge-hosted
jars in `overrides/mods/`. Appreciate the catch — happy to make any further
adjustments if anything else looks off.

## Changes since the last CurseForge release (v1.1.3)

**Added (was v1.1.4):**
- **Cubes Without Borders** `4.0.3` — borderless-fullscreen window mode for
  players running Minecraft alongside OBS / Discord / a browser without the
  window minimizing on focus change.

**Fixed (v1.1.5):**
- CurseForge `.zip` now references Blur+, Entity Culling, and Simple Voice
  Chat through `manifest.json` instead of bundling them as override jars.

No mod removed; no gameplay change. Mod count is 51.

## [1.1.4] — 2026-05-22

Adds a borderless-fullscreen quality-of-life mod recommended by a community
playtester. Useful for streamers running a second monitor — Minecraft stays
"fullscreen" while you switch focus to OBS / Discord / a browser without the
window minimizing and interrupting the stream.

### Added — Tier 4 (HUD, UI, utility)
- **Cubes Without Borders** `4.0.3` — borderless-fullscreen window mode. Pure
  client-side window behaviour, side `client`. CurseForge project `975120`,
  also published on Modrinth (`ETlrkaYF`) as a fallback if the CF metafile ever
  needs to be re-sourced.

### Changed — side-field sweep
- Standardised `side = "client"` across all 32 mods that had inherited
  `side = "both"` from CurseForge metadata at install time. The CLAUDE.md rule
  is explicit ("`side` must be `client` for every mod except the cross-side
  ones"), but packwiz copies whatever the upstream registry reports — most
  client-only QoL mods are tagged "Both" on CurseForge, so the project
  silently drifted. Functionally a no-op for the Modrinth manifest (both
  resolve to client-required), but a doc-honesty + future-reuse fix.
- **StreamCraft Live** and **Simple Voice Chat** kept at `side = "both"` —
  they really are cross-side (shipped at the same version on TBS-Server).

### Notes
- No change to StreamCraft Live, Simple Voice Chat, or any cross-side mod —
  v1.1.4 is a pure client-only addition, no TBS-Server bump needed.

51 packwiz metadata entries (canonical, Windows-variant).

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
