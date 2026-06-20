# Building a Custom Android Launcher for Minecraft 26.1.2 + Fabric + StreamCraft (XREAL Beam Pro)

**Scope (locked 2026-06-18):** A sideloaded Android APK that boots a desktop JVM, launches **Minecraft 26.1.2 + Fabric + the StreamCraft client mod**, and connects to the existing **TBS dedicated server** as a *client*. StreamCraft must work with **full capture** — webcam + screen-share + voice broadcast *from the device*. Target device: **XREAL Beam Pro 5G** (Android 14, Snapdragon 6 Gen 1 / Adreno 710, 8 GB).

**Out of scope:** Sodium / Iris / Voxy / Continuity / shaders (the whole TBS-Client visual layer); SoulCraft (server-side mod, runs on the TBS server, not the client); on-device server hosting.

**Status:** Build-ready synthesis from three research passes (broad lineage/packaging sweep + targeted device-specs pass + targeted Java-25/capture pass). Primary sources cited inline. Items requiring on-hardware validation are flagged ⚠ and collected in the Risk Register and Open Questions.

---

## 0. Executive summary — the strategic picture

Two facts reshape this project versus a naïve "port PojavLauncher" plan:

1. **The launcher itself is mostly a solved problem — adopt it, don't rebuild it.** Minecraft 26.1.2 requires **Java 25**, and **ZalithLauncher2 (ZL2)** — an active, GPLv3, PojavLauncher-core fork — *already ships an aarch64 Java 25 runtime and launches MC 26.1+/26.2+ on Android today*. Classic PojavLauncher caps at Java 21 and is discontinued; it cannot launch 26.x. So the JVM-bootstrap / renderer / GLFW work we'd otherwise research from scratch is done, in the open, by a trustworthy project. **Recommendation: fork/build on ZL2** (with FoldCraftLauncher as the fallback base — it bundles Java 8/17/21/25). This is also the clean answer to "I don't trust MojoLauncher": **ZL2 is the trustworthy open-source alternative.**

2. **Because we dropped shaders, graphics is no longer a risk — but StreamCraft full-capture becomes the entire reason to ship a custom launcher.** Without Sodium/Iris/Voxy, vanilla MC + StreamCraft run on the plain **gl4es** path that has worked for years; the Adreno 710's weak Vulkan/Turnip story stops mattering. What *doesn't* come for free is StreamCraft's webcam/screen/voice capture: its native libs have no Android build, and a desktop JVM on Android **cannot call Android's camera/screen/mic framework APIs**. Getting capture working — especially screen-share via `MediaProjection`, which is reachable *only* from the host Android app — is the novel engineering. **The custom-launcher's product is the capture bridge between the Android host app and the embedded JVM.**

**One-line architecture:** *Fork ZL2 → it boots Java 25 + MC 26.1.2 + Fabric + StreamCraft on gl4es → add an Android-side capture service (camera/screen/mic) that pipes frames over local IPC to the StreamCraft mod inside the JVM, which publishes them through the (Android-rebuilt) LiveKit FFI.*

---

## 1. Prior art / lineage, and the trust question

Minecraft Java runs on Android by **bundling a desktop-class OpenJDK inside the APK and translating desktop OpenGL → GLES/Vulkan**. There is one clean open-source lineage; build on it.

```
Boardwalk (zhuowei, root)               native JVM + glShim (ancestor of gl4es); dead on Android 7+
   └─ PojavLauncher (PojavLauncherTeam) canonical; bundled OpenJDK 8/17/21; gl4es/Mesa/virgl
        │                               ── repo ARCHIVED ~Sept 2025, caps at Java 21 ──
        ├─ Amethyst-Android (AngelAuraMC)   active successor; Java 8/17/21  → CANNOT do 26.x (no Java 25)
        ├─ FoldCraftLauncher (FCL-Team)     HMCL UI + Pojav backend; Java 8/17/21/25 → can do 26.x
        ├─ ZalithLauncher2 (ZalithLauncher) active; ships aarch64 JRE 25; launches 26.1+/26.2+ ← RECOMMENDED BASE
        └─ MojoLauncher                     forks Pojav v3_openjdk; LGPLv3 source — but distributed APK is AV-flagged
```

- **Boardwalk** (zhuowei) — root project. Solved desktop-GL-on-mobile with **glShim** (lunixbochs/ptitSeb → ancestor of **gl4es**). JVM strategy evolved Android-native → Oracle JDK → **OpenJDK Android port** (the bundled-desktop-JVM approach Pojav refined). Dead on Android 7+. *Historical reference only.*
- **PojavLauncher** — the de-facto standard for a decade; gl4es (MIT) + Mesa/libepoxy/virglrenderer; multi-arch OpenJDK 8/17/21. **Archived ~Sept 2025, tops out at Java 21** → *cannot launch 26.x.*
- **Amethyst-Android** (AngelAuraMC) — the "successor from Pojav's ruined reputation"; active, Forge+Fabric. **But Java 8/17/21 only** → *not viable for our Java-25 target.*
- **FoldCraftLauncher (FCL)** — HMCL's launcher UI over Pojav's runtime backend; **bundles Java 8/17/21/25**; GL stack gl4es/NG-gl4es/ANGLE/Mesa/virgl. *Viable Java-25 base / fallback.*
- **ZalithLauncher2 (ZL2)** — active Pojav-core fork. Changelog explicitly: *"Java Runtime: Added JRE 25"*, multi-arch Jre25 fixes, *"NeoForge: fixed … versions 26.1+"*, *"…load Java environment on 26.2+"*, plus a Vulkan-1.2 device check for the 26.2 renderer switch. **This is the only launcher independently confirmed to ship Java 25 and target 26.x.** *Recommended base.*

### MojoLauncher — the trust verdict

MojoLauncher is **"a Minecraft: Java Edition launcher, based on PojavLauncher"**, forking Pojav's `v3_openjdk` branch. The nuance that matters:

- **The GitHub source is *not* closed.** `github.com/mojolauncher/mojolauncher` is a public, buildable **LGPLv3** tree (`app_pojavlauncher`, `dnbglfw`, `forge_installer`, …). MojoLauncher also maintains the **LTW** renderer.
- **The distrust is about the *binary*, not the repo.** The APK served from `mojolauncher.com/.org/.lol` is a *different artifact* from the GitHub source; **AV engines have flagged that APK**, and there's a sprawl of **SEO mirror domains**. So: license/source clean (LGPLv3); binary distribution channel is the untrustworthy part.

**Clean-room guidance:** You may legitimately learn from and reuse the (L)GPL/MIT source across the Pojav lineage, subject to copyleft (§9). What to avoid is **shipping or copying MojoLauncher's distributed APK or any non-source binaries** from the mojolauncher.* domains. Base your work on **ZL2 source** (active, Java-25-capable, GPLv3). You can still read MojoLauncher's *source* (e.g. LTW) for technique, but pull nothing from its binaries.

---

## 2. Pillar 1 — Getting MC 26.1.2 + Fabric to launch (mostly solved by ZL2)

### 2.1 Version & Java runtime — the corrected facts

Mojang adopted a **`YY.D.H` (year.drop.hotfix)** calendar scheme (announced Dec 2025). The version names in play are **not interchangeable**:

| Version | Released | Java | Notes |
|---|---|---|---|
| **1.21.11** ("Mounts of Mayhem") | Dec 9 2025 | **Java 21** | *Last* "1." version, *last* obfuscated, *last* Java-21 line |
| **26.1** ("Tiny Takeover") | Mar 24 2026 | **Java 25** | *First* calendar version, *first* fully unobfuscated, *first* Java-25 line; successor to 1.21.11 |
| **26.1.2** (hotfix) | Apr 9 2026 | **Java 25** | Our target. Bundled runtime = Microsoft OpenJDK 25 |
| **26.2+** | later 2026 | Java 25 | **Renderer switched to Vulkan** (ZL2 enforces a Vulkan-1.2 device check) |

**Critical reconciliation:** your `TBS-client/pack.toml` lists `minecraft = "26.1.2"` with `acceptable-game-versions = ["1.21.11"]`. **Those are two different runtimes** (Java 25 vs Java 21). The packwiz metadata treats them as loosely compatible, but the *actual* 26.1.2 client needs **Java 25**. Likewise, **the StreamCraft jar must be the 26.1 band build** (StreamCraft's quarantined "Band I" — JDK 25 / Loom 1.15.5), **not** the 1.21.11 "Band H" jar. Installing the wrong band will fail to load.

**26.1.2 is still OpenGL** (the Vulkan switch is 26.2+), so the gl4es path applies. Good — and if you ever move to 26.2, the Adreno 710 does expose Vulkan 1.3, so the Vulkan-1.2 gate passes.

### 2.2 JVM on Android — how it works (ZL2 already does this)

- A desktop OpenJDK won't run on Android unmodified: Android uses **bionic libc** (not glibc; not binary-compatible), so the JDK must be **source-patched and NDK-built** — exactly what the OpenJDK **`openjdk/mobile`** project and Pojav's `android-openjdk-build-multiarch` do. **Temurin/Adoptium desktop aarch64 builds will not drop in.**
- The runtime must be a **`pojav`-patched build** (e.g. `jreXX-pojav`), supplying the AWT stub for the headless/AWT problem. ZL2's JRE 25 is such a bionic build.
- The APK `dlopen`s the bundled JDK's launcher libs (the `libjli`/launcher path), invokes the JVM via JNI, and hands off to the Fabric/Minecraft main class.
- **You do not need to build OpenJDK 25 yourself** — ZL2 ships it. (Fallback if you ever must: the `openjdk/mobile` patch set + NDK build for `aarch64-linux-android`. High effort; avoid.)

### 2.3 Renderer — trivial at this scope

With **no shaders and no Sodium/Iris**, vanilla MC + StreamCraft only need basic desktop GL, which **Holy GL4ES / gl4es** provides out of the box (it's Pojav's default). The hard Zink+Turnip path — and the Adreno 710's *experimental* Turnip support that worried us earlier — is **not needed**. Keep it in reserve only if some StreamCraft in-world rendering (the webcam billboards / display-block GL textures) misbehaves under gl4es; ZL2 lets you switch renderers in settings.

| Renderer | Needed here? | Why |
|---|---|---|
| **Holy GL4ES / gl4es** (default) | **Yes — use this** | GL 2.x/partial-3.x is plenty for vanilla + StreamCraft's texture quads; no shaders to satisfy |
| Zink + Turnip | No (reserve) | Only needed for GL 3.3+/4.x mods (Sodium/Iris) — out of scope. Adreno 710 Turnip is experimental anyway |
| ANGLE / VirGL | No | Compatibility/virtualized paths, not needed |

### 2.4 GLFW / windowing / input

ZL2 inherits Pojav's **custom GLFW stub + LWJGL fork** (GPL-3.0): an **EGL context** is created against the Android `Surface` and handed to the JVM-side GL/gl4es layer; **touch + on-screen keyboard + virtual gamepad** map to Minecraft input through the stubbed GLFW callbacks. You inherit all of this from the base. **Beam-Pro input nuance** is in §4.

### 2.5 Fabric + StreamCraft install

- ZL2/FCL already install **Fabric** (resolve the Fabric version JSON, fetch loader libraries, invoke `fabric-loader` under the bundled Java 25 — same flow as desktop).
- **You only need two mods**, not a `.mrpack`: **Fabric API** + **StreamCraft (26.1 band jar)**. Drop them into the instance `mods/` dir. (If you prefer, the launcher can fetch them from Modrinth — StreamCraft is published as `streamcraft-live` — but at this scope manual placement is simpler and avoids the `.mrpack` plumbing entirely.)
- **Native dependency caveat:** StreamCraft's jar bundles per-OS native `.so`/`.dll`/`.dylib` for capture + LiveKit FFI. **None are Android/bionic builds**, so the stock jar will *load as a mod* but its capture/voice natives **will not load** on Android. That's Pillar 2.

---

## 3. Pillar 2 — StreamCraft full capture on Android (the actual build)

This is where the custom launcher earns its existence. StreamCraft on desktop loads the **LiveKit Rust FFI** via JNA and captures webcam/screen/audio via per-OS native libs (Windows GDI/VfW/WASAPI, macOS ScreenCaptureKit, Linux V4L2/PipeWire). It bundles natives for Windows, macOS, and **glibc** linux-aarch64 — **no Android build**. And the embedded JVM is *desktop* OpenJDK with **no access to Android's Java framework** (Camera2, MediaProjection, AudioRecord). So capture must be re-architected around one seam: **native code reachable from the bionic JVM (via JNA/JNI), plus a host-app bridge for anything framework-only.**

### 3.1 The non-negotiable: rebuild every native for bionic/NDK

The bundled **glibc** `linux-aarch64` `.so` files **will not load** in the ZL2 JVM (bionic ≠ glibc; different linker, libc, C++ runtime). Everything native must be rebuilt for the **`aarch64-linux-android`** target with the NDK:
- LiveKit FFI (`liblivekit_ffi.so`)
- JNA's own dispatch lib (`libjnidispatch.so`) — must be the Android build
- any capture helper libs you write (below)

The established packaging pattern (used by the "Android Audio Shim" mod) is to **self-extract the bionic `.so` from the mod jar at runtime** and `System.load()` it.

### 3.2 Capture pipeline by modality (risk-ranked)

```
   ANDROID HOST APP (ART, holds permissions)              EMBEDDED DESKTOP JVM (ZL2)
   ┌───────────────────────────────────────┐             ┌──────────────────────────────────┐
   │ MediaProjection service (screen)       │  frames     │ StreamCraft (Fabric mod)         │
   │ Camera2 / AImageReader (webcam)*       │ ───IPC────▶ │  → LiveKit FFI (bionic .so)      │
   │ AudioRecord (mic)*                     │  socket/    │  → publishes WebRTC tracks       │
   │ CAMERA / RECORD_AUDIO / PROJECTION     │  shmem      │  → in-world billboards/display   │
   └───────────────────────────────────────┘             └──────────────────────────────────┘
   * camera & mic can alternatively be done natively inside the JVM via NDK libs (see below)
```

| Modality | Recommended path | Risk | Notes |
|---|---|---|---|
| **LiveKit transport** | Reuse StreamCraft's **JNA→FFI** path with the **Android aarch64 `liblivekit_ffi.so`** | **LOW** | `livekit/rust-sdks` CI (`ffi-builds.yml`) already builds & publishes `aarch64-linux-android` artifacts. C ABI is identical to desktop; only the `.so` changes. Don't switch to the Kotlin `livekit-android` SDK. |
| **Voice (mic + playback)** | Native **AAudio (mic) + OpenSL ES (playback)** bionic lib, self-extracted from the jar — the **Android Audio Shim** pattern | **LOW–MED** | This is the *proven* trick that makes Simple Voice Chat work under Pojav. Direct template for StreamCraft audio. Needs `RECORD_AUDIO` granted to the host APK. |
| **Webcam** | **NDK Camera2** (`libcamera2ndk` / `AImageReader`) in a bionic `.so` → frames to the JVM-side mod | **MED** | Camera2 NDK is callable from native code without the Java framework (API 24+). *No known precedent for a camera mod under Pojav* — novel plumbing. Needs `CAMERA` granted to the host APK. Alternative: host-app captures and pipes frames (below). |
| **Screen-share** | **`MediaProjection` runs in the HOST APK** (consent Activity + foreground Service) → frames piped over local IPC to the mod → LiveKit | **HIGH** | `MediaProjection` is framework/ART-only and **unreachable from the desktop JVM**. No NDK equivalent. This *forces* host-APK involvement and is the single biggest architectural piece. |

**Why owning the launcher APK is the unlock:** a stock-ZL2 user could never screen-share a Fabric mod — there's no way to reach `MediaProjection` from the JVM. But because we **fork ZL2**, we control the host APK: we add the projection consent flow, a foreground capture service, the camera/mic permission declarations, and a local IPC channel (Unix-domain socket or `ashmem`/shared buffer) that streams encoded or raw frames to the StreamCraft mod, which hands them to LiveKit as video tracks. **That bridge is the product.**

**Recommended simplification:** put **camera and mic in the host app too**, alongside screen capture (not just screen). Reasons: (a) one permission/consent surface, (b) one IPC frame-transport to build and debug, (c) avoids the unproven in-JVM NDK-Camera2 path. The JVM-side mod then becomes a thin consumer: receive frames over IPC → push into LiveKit FFI. This trades a bit more host-app code for far less risk.

### 3.3 What StreamCraft code has to change

- Replace the platform `CaptureFactory` selection so that, on Android, capture sources read from the **IPC bridge** instead of GDI/V4L2/ScreenCaptureKit.
- Swap the bundled native loader to extract/load the **`aarch64-linux-android`** `liblivekit_ffi.so` (+ Android `libjnidispatch.so`).
- Verify the in-world rendering path (`StreamTextureManager` GL texture uploads, `WebcamBillboardFeature`, `DisplayBlockRenderer`) works under **gl4es** — these use plain GL texture quads, which gl4es handles, but ⚠ validate on hardware.
- StreamCraft's licensing/networking/proximity logic is pure JVM and needs no change.

---

## 4. Target device — XREAL Beam Pro 5G

| Property | Value | Implication |
|---|---|---|
| SoC | **Snapdragon 6 Gen 1 (SM6450)**, 4 nm | Mid-range; third-party-confirmed (XREAL markets it as "Snapdragon Spatial Companion Platform") |
| GPU | **Adreno 710**, Vulkan 1.3 / GLES 3.2 | Fine for gl4es vanilla. (Turnip support is experimental for A710 — irrelevant now that we don't need Zink) |
| CPU | 4×A78 ≤2.2 GHz + 4×A55 1.8 GHz | OK for vanilla + WebRTC; expect some throttling |
| RAM | **8 GB** (target) / 6 GB variant | JVM heap budget after Android 14 + NebulaOS + AR compositor: **~3.5–4 GB on 8 GB**, ~2–2.5 GB on 6 GB. **Get the 8 GB model.** |
| OS | **Android 14**, NebulaOS skin | Full Google Play **and** sideloading (unknown-sources) officially supported; not a kiosk lockdown |
| Root | none needed | AdrenoTools driver-swap works without root — but we don't need it anyway |
| Own display | 6.5" 1080×2400 90 Hz touchscreen | This is the touch surface for input |
| Glasses output | 1920×1080@90 Hz (or 3840×1080@72 Hz 3D), 3DoF | Render target; 6DoF only with Air 2 Ultra |
| Thermals | mid-range chip also driving glasses | ⚠ throttling on long sessions — validate |

**Input model (important and unusual):** the glasses provide *display + head-tracking*, **not buttons**. Minecraft input must come from the **Beam Pro's own touchscreen** (Pojav/ZL2 on-screen controls) and/or a **paired Bluetooth controller or keyboard+mouse** (BT 5.2). Head-tracking 3DoF is not native Minecraft input and would need custom mapping — treat as out of scope. For a *video-conferencing-in-Minecraft* use case, a paired BT keyboard+mouse is the realistic comfortable setup; design the launcher to assume external input is likely.

**Sideloading is confirmed feasible** — standard Android 14, no root, no kiosk restriction.

---

## 5. Microsoft authentication

- Implement **Microsoft / Xbox Live OAuth** in the host app. The **device-code flow** is most robust for a sideloaded app (no custom redirect URI handling): show a code, user authorizes on `microsoft.com/link`, poll for the token.
- Token exchange chain: **MS OAuth → Xbox Live (XBL) → XSTS → Minecraft services token → Minecraft profile/entitlements.**
- Store tokens in the **Android Keystore / EncryptedSharedPreferences**; refresh on expiry.
- **Ownership is mandatory** — the account must own Minecraft Java Edition; do not bypass entitlement checks (§9). ZL2 already implements an MS-auth flow you can inherit/adapt.

---

## 6. Asset / version bootstrap (never redistribute Mojang's jar)

- Pull Mojang's **version manifest**, resolve the **26.1.2** entry, and download the **client jar + asset index + assets + libraries directly from Mojang's servers at runtime.** Never ship Mojang's client jar in the APK.
- 26.x is **unobfuscated**, which simplifies nothing for launching but is worth noting.
- Handle the asset index (hash-keyed objects) and lay out a **`.minecraft`-style instance dir under Android scoped storage** (app-specific external dir). ZL2 already structures this — inherit it.

---

## 7. APK / build / packaging

- **Project:** standard Android Gradle project — you're forking ZL2's, not greenfielding.
- **Large native payload:** bundled **JRE 25 + gl4es/Mesa/LWJGL `.so` + LiveKit FFI + capture libs**. **Split by ABI; ship `arm64-v8a` (`aarch64-linux-android`) only** — that's the Beam Pro and every modern phone. Dropping the other ABIs cuts size substantially.
- **Scoped storage:** keep the game dir in app-scoped external storage; modern target-SDK forbids broad filesystem access.
- **Long sessions + capture:** you already need a **foreground service** for `MediaProjection`; reuse it (with a wakelock) to keep the session alive. Declare `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_MEDIA_PROJECTION`, `CAMERA`, `RECORD_AUDIO`, `POST_NOTIFICATIONS`.
- **Signing/sideload:** self-sign; distribute the APK directly. **Publish your source** (copyleft, §9). Never redistribute the AV-flagged MojoLauncher binaries.

---

## 8. Legal / licensing

- **Mojang EULA / brand guidelines:** don't use "Minecraft"/"Mojang" branding in the app name/logo; don't redistribute the client jar (download from Mojang at runtime, §6); require account ownership (§5). Commercial/Patreon aspects of StreamCraft are unaffected on the client side.
- **Copyleft you inherit by forking ZL2:**
  - **ZalithLauncher2 / PojavLauncher / the Pojav LWJGL fork (`Vera-Firefly/lwjgl3-build`):** **GPL-3.0** — strong copyleft. A derivative **must release source under GPL-compatible terms.** (Upstream LWJGL3 is BSD-3; the copyleft enters via Pojav's modifications.)
  - **gl4es, Mesa 3D, libepoxy, virglrenderer:** **MIT** (permissive).
  - **MojoLauncher source:** LGPLv3 (don't ship its binaries regardless).
  - **LiveKit Rust SDK / FFI:** Apache-2.0 (permissive) — fine to bundle the Android `.so`.
- **StreamCraft itself:** your own mod; ensure its bundled third-party natives (FFmpeg/OpenCV/etc., per its `THIRD-PARTY-NATIVES.md`) keep their LGPL/license compliance when you rebuild them for Android — *or drop the ones the Android capture path no longer uses.*
- **Net:** forking ZL2 means **your launcher must be open-source (GPL-3.0)**. That's compatible with a clean, trustworthy release and is the opposite of the MojoLauncher binary problem.

---

## 9. Recommended stack + phased build plan

### Recommended stack
- **Launcher base:** **ZalithLauncher2** (active, ships aarch64 **Java 25**, launches 26.1+; GPL-3.0). Fallback: **FoldCraftLauncher** (Java 8/17/21/25).
- **JVM:** ZL2's bundled **pojav-patched OpenJDK 25** for `aarch64-linux-android`. (Do **not** build your own; do **not** use Temurin desktop.)
- **Renderer:** **Holy GL4ES / gl4es** (default). Zink+Turnip kept only as a fallback toggle.
- **Loader + mods:** Fabric loader (current 26.1 build) + **Fabric API** + **StreamCraft 26.1-band jar**.
- **Capture:** host-APK **MediaProjection (screen) + Camera2 (webcam) + AudioRecord/AAudio (mic)** → local IPC → StreamCraft mod → **LiveKit FFI (`aarch64-linux-android` build)**.
- **Auth:** Microsoft device-code OAuth (inherited from ZL2), ownership required.
- **Device:** XREAL Beam Pro **8 GB**, gl4es, BT keyboard+mouse for comfortable input.

### Phased milestones (⚠ = highest-risk; validate on real Beam Pro hardware ASAP)

**Phase 0 — De-risk on real hardware before writing launcher code (do this first).**
- Install **stock ZalithLauncher2** from its official release on the Beam Pro, log in, and **launch vanilla 26.1.2 on gl4es**. ⚠ This single test confirms Java 25 + renderer + the device all work before you invest in anything custom. If this fails, everything downstream changes.

**Phase 1 — Vanilla + Fabric + StreamCraft loads (no capture).**
- Fork ZL2; build/sign your APK; launch **26.1.2 + Fabric API + StreamCraft 26.1-band**; connect to the TBS server. ⚠ Confirm StreamCraft's in-world GL rendering (billboards/display blocks) works under gl4es even with capture disabled.

**Phase 2 — LiveKit transport on Android.**
- Rebuild/obtain **`liblivekit_ffi.so` (aarch64-linux-android)** + Android `libjnidispatch.so`; get StreamCraft to **connect to LiveKit and receive** a remote track (display someone else's webcam in-world). ⚠ FFI ABI match between mod and `.so`.

**Phase 3 — Voice (mic + playback).**
- Add the **AAudio/OpenSL ES** bionic audio lib (Audio-Shim pattern); host APK grants `RECORD_AUDIO`. Achieve two-way voice. (Proven pattern → should be smooth.)

**Phase 4 — Webcam broadcast.**
- Host-app **Camera2** capture → IPC → StreamCraft → LiveKit video track. ⚠ Frame format/perf of the IPC bridge; ⚠ camera permission/consent UX.

**Phase 5 — Screen-share broadcast (hardest).**
- Host-app **MediaProjection** consent + foreground service → IPC → StreamCraft → LiveKit. ⚠⚠ Largest architectural piece; ⚠ projection consent + foreground-service-media-projection target-SDK rules; ⚠ encode/transport perf and thermals.

**Phase 6 — Hardening.**
- Thermal/throttle soak test on the Beam Pro; reconnection logic; token refresh; battery; input ergonomics with BT peripherals; APK size trim (arm64-v8a only).

### Risk register
| Risk | Severity | Mitigation |
|---|---|---|
| Phase 0 fails (26.1.2 won't launch on Beam Pro under ZL2) | **High** | Test first, before any custom work. Fall back to FCL; or pin to 1.21.11/Java-21 + StreamCraft Band H if 26.x is blocked on device |
| `MediaProjection` unreachable from JVM (screen-share) | **High** | Host-APK capture service + IPC bridge (the core design); defer screen-share to last |
| Webcam via NDK/host-app, no Pojav precedent | Med–High | Do camera in the host app (not in-JVM NDK); reuse the screen IPC transport |
| All natives need bionic rebuild | Med | Mechanical; LiveKit FFI Android artifact already exists; script the NDK builds |
| StreamCraft GL rendering under gl4es | Med | Validate Phase 1; fall back to Zink+Turnip toggle if billboards/textures break |
| 8 GB shared RAM / heap pressure | Med | Buy 8 GB variant; cap JVM heap ~3–3.5 GB; vanilla (no Voxy) keeps footprint low |
| Thermal throttling on long sessions | Med | Soak test; encode efficiently; possibly cap resolution/FPS of captured streams |
| GPL-3.0 obligations from forking ZL2 | Low | Publish source; it's compatible with a clean release |
| Wrong StreamCraft band installed (H vs I) | Low | Pin the **26.1** band jar; document it |
| Beam Pro input ergonomics | Low–Med | Assume BT keyboard+mouse/controller; tune on-screen controls as fallback |

---

## 10. Open questions to resolve on hardware / with the StreamCraft codebase
1. **Does stock ZL2 launch 26.1.2 on the Beam Pro?** (Phase 0 — the gating unknown.)
2. **Exact ZL2 version** that first shipped JRE 25 (changelog confirms it exists; pin a known-good release).
3. **gl4es vs StreamCraft's GL texture path** — do `StreamTextureManager` uploads and billboard/display-block rendering work without artifacts under gl4es?
4. **IPC frame transport** — raw frames vs on-device hardware-encoded (MediaCodec) frames into LiveKit; latency/throughput on the SM6450.
5. **LiveKit FFI version** matching StreamCraft's desktop FFI ABI for the 26.1 band.
6. **Foreground-service-media-projection** target-SDK requirements on Android 14 (consent re-prompts, service type declaration).
7. **Thermal envelope** for simultaneous game render + camera + screen + WebRTC encode on a mid-range chip also driving AR glasses.
8. **Beam Pro audio routing** — does mic/playback go through the glasses, the Beam Pro, or a BT headset, and does AAudio see the right device?

---

## Appendix: primary sources

**Lineage / launchers / MojoLauncher**
- `github.com/zhuowei/Boardwalk` · `github.com/PojavLauncherTeam/PojavLauncher` (archived) · `github.com/AngelAuraMC/Amethyst-Android` (Java 8/17/21) · `github.com/FCL-Team/FoldCraftLauncher` (Java 8/17/21/25)
- `github.com/ZalithLauncher/ZalithLauncher2` + releases (ships **JRE 25**, 26.1+/26.2+ support, Vulkan-1.2 check) — *recommended base*
- `github.com/mojolauncher/mojolauncher` (LGPLv3 source) · `github.com/MojoLauncher/LTW` (renderer) — *source readable, binaries AV-flagged*

**JVM on Android**
- `github.com/PojavLauncherTeam/android-openjdk-build-multiarch` (+ `/releases`) — multi-arch OpenJDK, branch-per-version (caps at 21)
- `openjdk.org/projects/mobile/android.html` — bionic patch set for building OpenJDK on Android
- `pojavlauncher.app/wiki/faq/android/JAVARUNTIMES.html` — pojav-patched-runtime requirement

**Versioning / Java 25**
- `minecraft.wiki/w/Java_Edition_26.1`, `…/Java_Edition_26.1.2`, `…/Java_Edition_1.21.11`, `…/Version_formats`
- `minecraft.net/en-us/article/minecraft-new-version-numbering-system`
- `hosting.swelis.com` 26.1.2 admin guide (Java 25 / MS OpenJDK 25) · `modready.gg` Java-version table · `github.com/Infinidoge/nix-minecraft/issues/211` (independent jdk25 confirmation)

**Renderers**
- `pojavlauncher.app/wiki/faq/android/RENDERERS.html` · `github.com/eternights/PojavLauncherDocs/blob/main/RENDERERS.md`

**StreamCraft capture / natives**
- `github.com/livekit/rust-sdks/blob/main/.github/workflows/ffi-builds.yml` (builds **aarch64-linux-android** FFI) · `github.com/livekit/rust-sdks/releases`
- `modrinth.com/mod/android-audio-shim` (AAudio mic + OpenSL ES playback for mods under Pojav) · `github.com/henkelmax/simple-voice-chat/issues/773` · `github.com/PojavLauncherTeam/PojavLauncher/issues/4810`
- `developer.android.com/media/camera/camera2` (NDK Camera2) · `github.com/Cloudef/android2gnulinux` (bionic≠glibc) · `android.googlesource.com/platform/bionic/+/master/android-changes-for-ndk-developers.md`

**Device**
- `gsmarena.com` Beam Pro · `benchmarks.ul.com/hardware/phone/XREAL+Beam+Pro+review` · `cputronic.com/soc/qualcomm-snapdragon-6-gen-1` · `notebookcheck.net` Adreno 710 · `xreal.com/us/beampro` · `xreal.sensofinity.com/pages/beam-pro-support` (sideloading)

**Licensing**
- `github.com/Vera-Firefly/lwjgl3-build` (GPL-3.0 Pojav LWJGL)

---

*Document reframed to the locked scope (client-only; MC 26.1.2 + Fabric + StreamCraft full-capture; no shaders; no SoulCraft) on 2026-06-18, consolidating a broad lineage/packaging research sweep with two targeted passes (XREAL Beam Pro hardware; Java-25-on-Android + WebRTC/capture feasibility).*
