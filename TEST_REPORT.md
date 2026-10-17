# v0.1.1 validation report

Executed in Linux cloud on 2026-10-16 (America/Los_Angeles). Runtime: Python 3.12.14, Node v24.19.0, Playwright 1.62.1, system Chromium 154.0.8037.57. Windows 11 is the intended test target, not a platform tested here.

## Executed against working source

- `npm test`: **5 Node tests passed; 9 Python tests passed; 0 failed; 0 skipped.** Node tests cover all states, preview syntax, independent legal/risk unknowns, unavailable lookup, and project schema/import boundaries. Python tests cover update/rollback, data preservation, corrupt/unsafe ZIP refusal, failed-update pointer preservation, patch refusal, compatible Build discovery, asset tamper detection, localhost/allowlisted HTTP serving with module MIME types, and occupied-port refusal.
- `python3 tools/launch.py --check`: passed with the prepared per-file manifest.
- `STUDIO_URL=http://localhost:4183 CHROMIUM_PATH=/usr/bin/chromium node tools/smoke.cjs`: passed against the new Python launcher. Exercises 50 state options, initial rendering, real-time uppercase text, mouse drag on Orbit slider, reset, single-slot save, actual browser close/reopen/load using a persistent test profile, JSON download/export and import, malformed-import rejection without losing the current preview, persistent research notes, unavailable-provider message, Unverified legal status, 390px layout and no page script errors. Does not test free-camera pan/zoom because they do not exist.
- `python3 tools/build_windows.py`: correctly refused on Linux with a specific no-cross-compilation message. This is a checked platform guard, NOT a successful Windows build.

## Corrected failure during release validation

The first 0.1.1 candidate failed the real-package rollback test: the updater had not copied release.json into version slots. Fixed by retaining the verified manifest; the existing update/rollback test now explicitly asserts its presence. The first candidate ZIP is retained unchanged and is not the recommended download. Packaging revision r2 includes this correction and is the intended test package.

## Release packaging validation

`tools/test_package.py` is the reproducible post-packaging acceptance command. It extracts the actual ZIP into a fresh temporary path containing spaces, verifies all file hashes, exercises its own launcher, installs real 0.1.0 and 0.1.1 artifacts, rolls back in both directions, verifies personal project/settings marker files survive, refuses a repeated install, runs the Chromium UI smoke test, and rechecks packaged hashes after execution. Its actual run output and ZIP hash are saved separately in Build alongside the final artifact after packaging. No checksum is fabricated inside this report.

## Original release audit

The original Build/License-Plate-Obfuscation-Studio-0.1.0.zip remains unchanged with SHA-256 `8450f726b8a14c6186403ee751ebb00d22f5eeac02fe2b7ea0bfba2e85f6445c`. Its RELEASE-REPORT.md recorded five Node tests, three Python updater tests, one browser workflow and ZIP hash/installation checks. The earlier browser smoke used a test URL at 127.0.0.1 and did not prove persistence across an actual browser restart; the new test does that using localhost. Its .cmd launchers were unrun. The old package's updater expected a Build ZIP outside its own extracted contents, so it was not a self-contained first-time Windows distribution.

## Unrun / unavailable

- Windows 11 batch launchers, WinGet installation, native PyInstaller EXE build, unsigned-download prompts, Windows browser interactive checklist, B: paths and native EXE behavior. No Windows runtime, Wine or PowerShell is available here. The Windows build script is supplied, not claimed tested.
- Browser default-app auto-opening: headless checks use --no-browser; verify this manually on Windows.
- Current legal source contents, interpretation, official artwork/eligibility datasets, live authorized plate availability, True Engine SDK integration, membership, vehicle models and unsupported roadmap tools.
- Automated screenshot pixel comparison, accessibility audit, performance benchmarks and other browser engines. No speed improvement or complete render correctness is claimed.

No existing source was deleted, prior ZIPs were overwritten, or user data was migrated. Modified v0.1.0 source remains recoverable via its Git tag. Browser-only data remains subject to origin/profile and browser clearing; the manual checklist explicitly tests reopen and export/import on the user's Windows computer.
