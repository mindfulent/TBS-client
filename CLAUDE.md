# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Read the parent `TBS/CLAUDE.md` too — it covers the two-pack architecture, the
> vanilla-client contract, `server-config.py`, and the shared CurseForge-first policy.
> This file only covers what is specific to **TBS-Client**.

## What this repo is

TBS-Client is a **packwiz modpack** — there is no application code, no build system, no
tests. The repo is a tree of TOML metadata: `pack.toml` (pack manifest), `index.toml`
(file index with hashes), and one `mods/<slug>.pw.toml` per mod. Each `.pw.toml` names a
mod, its target `side`, and a `[download]` URL + hash plus an `[update]` block pointing at
the CurseForge or Modrinth project. `packwiz.exe` resolves these into a distributable
`.mrpack`. "Working on the codebase" here means editing pack metadata, not writing code.

This is its **own git repo**, versioned independently from `TBS-server/` and the TBS root.
Commit pack changes here, inside `TBS-client/`.

## The hard constraint: client-side-only

Every mod in this pack must be **client-side-only and safe against a vanilla server** — it
must run when the player connects to a stock vanilla 26.1.2 server (which TBS's base server
effectively is). Concretely:

- No content mods, no worldgen/structure/mob mods, no mod that needs a server companion.
- The `side` field in each `.pw.toml` should be `client` for every mod **except
  StreamCraft Live**, which is `side = "both"` — it is the one mod shared with TBS-Server.
- Before adding any mod, confirm it is client-only. See the exclusion lists in
  `docs/TBS-mod-strategy.md`.

StreamCraft Live's jar version must stay **identical** to the TBS-Server copy. Bumping it
is a synchronized release of both packs; do not bump it here alone. Every other mod's
version is independent of TBS-Server.

## Mod organization

Mods follow a five-tier scheme (Foundation → Visual range/quality → Camera/controls/
animations → HUD/UI/utility → Cross-side). The tiers are documentation only — they live in
`README.md` and `CHANGELOG.md`, not in the pack metadata. `mods/` is a flat directory.

Mods with no 26.1.2 build yet are tracked under "Pending mods" in `README.md` and
"Not yet included" in `CHANGELOG.md` — add them when builds appear, don't silently drop them.

## Commands

```bash
./packwiz.exe cf install <slug> -y    # add a mod — CurseForge first (compliance)
./packwiz.exe mr install <slug> -y    # Modrinth fallback ONLY when no CF 26.1.2 build
./packwiz.exe update --all            # update every mod
./packwiz.exe refresh                 # rebuild index.toml hashes after ANY manual edit
./packwiz.exe modrinth export         # produce TBS-Client-X.Y.Z.mrpack
```

`index.toml` tracks `README.md`, `CHANGELOG.md`, and `docs/` alongside the `.pw.toml`
files — so editing any of those by hand requires a `refresh` afterward to fix the index
and `pack.toml` hashes. 26.1.2 is the Fabric 1.21.11 ecosystem; a mod tagged `26.1.x`
*or* `1.21.11` generally works.

## Adding or changing a mod — full checklist

1. `./packwiz.exe cf install <slug> -y` (CurseForge first; Modrinth only if no 26.1.2 CF
   build, and then mark the mod `(Modrinth)` in `CHANGELOG.md`).
2. Verify the mod is client-side-only and the new `.pw.toml` has `side = "client"`.
3. If switching a mod Modrinth↔CurseForge, delete the old `.pw.toml` first — packwiz
   writes a fresh file and the stale one will linger.
4. Bump `version` in `pack.toml` (semver: patch for mod add/fix, minor for larger changes).
5. Update `CHANGELOG.md` (new version entry, dated) and `README.md` (tier list, mod count,
   pending-mods list).
6. `./packwiz.exe refresh`, then `./packwiz.exe modrinth export`.
7. Commit inside this repo.

`packwiz modrinth export` **aborts** if a mod's CurseForge file forbids third-party API
distribution (error mentions "manual download"). Fix: re-source that mod from Modrinth —
delete its `.pw.toml`, `mr install` it — so the `.mrpack` can embed it by URL.

## Distribution

TBS-Client is published as a `.mrpack` (and exported `.zip`) for players to import into
Prism Launcher or the CurseForge App. Unlike TBS-Server, it is **not** deployed by
`server-config.py` — that tool only touches the server pack.
