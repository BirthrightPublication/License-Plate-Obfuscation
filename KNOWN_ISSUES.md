# Experimental V0.1.2 — SDK integration restart and known issues

The owner authorized engine/interface integration restart and selected published
True Engine v0.1.2/SDK0.1. The current landing-page/CSS prototype is still rejected
as the final editor. No new integrated release exists.

- SDK contract lacks orthographic projection usable by Renderer.draw and suitable
  plate-text/custom-mesh submission. Material support is opaque color only. See
  docs/TRUE-ENGINE-SDK-ASSESSMENT.md and docs/TRUE-ENGINE-FEATURE-REQUEST.md.
- The standalone Git-pinned SDK probe tests actual supported engine behavior;
  passing it does not integrate the application's UI or qualify interactive
  Windows11 GPU/input behavior. Read TEST_REPORT.md for exact run/skip status.
- Source/native primary launchers now distinguish layouts and preserve uppercase
  aliases. Source starts remain explicitly labeled experimental and use the same
  browser profile/origin/pointer as before. A damaged app must not silently fall
  back to source. Repository fixes do not modify copies already on a user's PC.
- Source-only native updating needs Python3.12 and explicit confirmation of the
  target root. It preserves source/legacy files and does not migrate user data.
  Complete native packages retain their embedded runtime/updater route.
- Native updates refuse same-version reinstall/downgrade and unknown/modified app
  contents. Update is not a generic repair. Root launchers are not automatically
  overwritten; customized/older launcher migration needs a verified backup plan.
- Recovery-updater copies are retained, not automatically refreshed. Recovery is
  based on prior verified app backups; no backup exists before first installation.
- A ZIP in Build is not an installation. BUILD WINDOWS creates a package using a
  temporary Python/PyInstaller environment; it does not create an installed app
  beside source. Binary rebuilds are not guaranteed byte-identical.
- Only app is replaceable. Every other project/settings/history/media/output/
  preset/custom configuration path and browser data must remain preserved.
  No exact B: folder or existing installation has been inspected from this cloud.
- Current project schema stores name/state/text in one browser slot. Notes and
  view angle are not exported. Preserve same localhost:4173 browser origin/profile;
  export projects and copy important notes before any approved migration.
- No approved professional engine editor, official plate-artwork catalog,
  authoritative availability provider, reviewed legal assessment, membership or
  vehicle integration exists. Legal is Unverified; regulatory risk is unassessed.
- Packages are unsigned. Hosted/native/Linux tests cover their stated targets;
  they do not imply all user GPUs, Windows security prompts or interactive use
  passed. Network/rate-limit/file-lock/storage failures remain possible.
- Native Update BAT detached bootstrap/public-download end-to-end was not run in this branch; its --check path, dispatch and backend fixture tests do not establish a live update on the user machine.
- The cloud GitHub API tunnel currently returns403 even though native HTTPS Git
  reads/pushes work. PR/issue/Actions/release operations require separate confirmed
  access. No successful remote operation may be inferred from a local file.
- No project/media/settings, source script, prior package or release tag was
  deleted. Exact-base patch ZIP support and a dedicated repair utility remain
  future work; existing updater accepts verified full packages only.

Historical audit evidence is preserved in docs/INSTALLATION-AUDIT.md. The safe
repair plan and professional UI target remain in docs/INSTALLATION-REPAIR-PLAN.md
and docs/TRUE-ENGINE-UI-ARCHITECTURE.md, with latest SDK/restart facts superseding
their prior audit-only hold language.
