# Experimental V0.1.2 — development hold and known issues

**The current interface is not approved. Feature/visual development and feature
version advancement are frozen until explicit user approval and a tested True
Engine foundation.** Published artifact history remains intact; this classification
does not alter, delete or retag a release.

- The source root mixes START APPLICATION.bat (Python/developer), UPDATE/ROLLBACK
  APPLICATION.bat (legacy Installed slots) and Start/Update/Rollback Plate.bat
  (native app layout). These are not interchangeable installations.
- The user's screenshot shows the source layout and no visible app folder. Native
  Start requires app/PlateStudio.exe. Native Update requires app/PlateUpdater.exe
  or .plate-studio/recovery-updater.exe. Both are absent in this cloud checkout;
  Update cannot contact GitHub or self-repair a source-only folder without a native
  bootstrap. Start's suggestion to use Update is misleading in this condition.
- The complete published native ZIP DOES contain both x64 EXEs. Having a ZIP in
  Build does not install it. The user's full B: path and Build contents were not
  visible in the screenshot; no separate Windows installation was inspected here.
- BUILD WINDOWS.bat installs PyInstaller in a temporary Python venv and creates a
  ZIP/checksum. It does not install app beside the launcher or integrate True Engine.
  Transitive build requirements are not fully locked for byte-identical rebuilds.
- Root release.json and VERIFY RELEASE validate four browser assets, not a complete
  native app. Generic Build/release.json/SHA256SUMS.txt are historical 0.1.0 sidecars;
  use the matching package-specific checksums, not generic files for other versions.
- The compatibility filename is true-engine.compatibility.json (hyphen), not the
  underscore spelling. SDK package/version remain null. No engine adapter/render
  integration exists; CSS perspective/rotation is an HTML prototype only.
- No professional engine viewport, real mouse camera, pan/zoom, object editing,
  compact approved editor shell or dark theme exists. Do not continue the current
  landing-page UI as the final product or implement a substitute renderer.
- No dedicated repair utility exists. Legacy and native updaters accept full
  packages only. Versioned patches, exact-base patch verification and simplified
  maintenance launchers are proposals, not implemented capabilities. Existing
  scripts must stay until approved replacements work and pass tests.
- Native updates refuse same-version reinstall/downgrade and unknown/modified app
  contents. Therefore the current update command is not a generic repair utility.
  Root launchers are not overwritten automatically. Earlier layouts are not
  silently migrated. Keep recovery/backups; do not run updates as a diagnostic.
- User state is one browser save slot plus separate research notes. Project JSON
  excludes notes and view angle. Clearing site data, changing origin/profile or
  overwriting the save slot can lose access to prior state. Repair must preserve
  data and export/copy it before any specifically approved mutation.
- There is no official style/eligibility dataset, reviewed legal determination,
  authorized availability provider, membership or vehicle-model integration. Legal
  remains Unverified; risk is unassessed. External media tools/data remain untouched.
- Historical Windows native/browser/install/recovery/live-update tests passed for
  the prototype's packaging. They do not prove professional-editor readiness,
  design approval or a working True Engine SDK. This audit did not execute native
  code, installers, dependency scripts, repairs or destructive tests.
- Packages are unsigned; network/rate-limit/locked-file/storage failures remain
  possible. Logs/backups/runners/downloads accumulate until explicitly maintained.
  No original data/media, unknown files, legacy releases or scripts were removed.

See docs/INSTALLATION-AUDIT.md for exact evidence and script line references,
docs/INSTALLATION-REPAIR-PLAN.md for proposed structure/confirmation gates, and
docs/TRUE-ENGINE-UI-ARCHITECTURE.md for engine/UI plans. No repair is approved or
performed by these documents.
