# Current source iteration — SDK assessment and launcher repair

The owner authorized integration restart and selected published True Engine
v0.1.2/SDK0.1, commit8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0. No new application
version or integrated release has been produced. Historical release results below
remain associated with their original tagged source and binaries.

## Actual local execution

- Linux; Python3.12.14, Node24.19.0, Rust1.85.1.
- `npm test`: **5 Node passed**; Python **38 discovered, 37 passed, 1 skipped**.
  The skip is the explicit Windows-only cmd.exe primary/alias batch test. It was
  not simulated or claimed passed here.
- The 10 passing new launcher tests cover source/native selection, exact app hash/
  inventory verification in Python dispatch, damaged-app refusal without source
  fallback, legacy pointer/argv/exit-code preservation, recovery selection,
  journal-only refusal, explicit source-install confirmation/cancellation,
  read-only diagnostics, root override rejection and fixture-file preservation.
- Existing updater tests exercised checksum/download fixtures, staging/activation
  failure rollback, journal recovery, unknown-file refusal and preservation of
  projects/settings/history/original and processed media/output/template markers
  in temporary test roots. Fixture EXEs are not native-executable validation.
- `python3 tools/windows_entry.py --root . start -- --check` and the corresponding
  `update -- --check`: passed. No browser, network download or installation.
- Source dispatcher was started with `--no-browser` on a temporary test port;
  actual HTML and JavaScript requests succeeded. Only our own host process group
  was stopped. The production default remains localhost:4173; no user browser or
  browser data was opened or changed.
- External Rust SDK consumer: **4 CPU +1 GPU tests passed**, 0 failed/ignored.
  Exact command: `cargo +1.85.1 test --locked -- --nocapture`.
  CPU: plate dimensions/rotation/color, scene/project save-reopen, picking, camera
  orbit/pan/zoom and changed viewport aspect. GPU: real public Engine Renderer
  pixel readback, visible scaled cube plate, red-to-blue material update, changed
  camera image, and64x64-to96x48 resize. Adapter: **Mesa llvmpipe LLVM19.1.7,
  GL software rendering**. Full output: docs/true-engine-sdk-test-results.txt.
- `cargo fmt --all -- --check` and `git diff --check`: passed.
- Reusable environment install_script was executed end-to-end after saving;
  app/domain, Python and locked SDK checks passed again. It installs/activates
  Rust1.85.1 under /workspace/.tools, preserves dependency lockfiles and keeps
  generated outputs outside tracked source. start_skill was updated with the
  exact prerequisites, tests and present SDK blockers. Saving does not publish
  a cloud environment or verify another restored instance.

## Unrun and blocked checks

No Windows execution occurred in this Linux cloud. The remote consumer and cmd.exe tests below ran on Windows. No real mouse/window events, user hardware qualification, updater download on the user's PC, existing-installation repair, data migration, or production application/engine integration test is claimed.
No app UI asset changed; no new browser visual test is claimed.

The reusable SDK workflow now runs CPU/GPU checks on both Ubuntu and Windows and
is a dependency of Windows packaging/publication. A missing adapter fails, never
silently skips. The remote jobs were observed through public GitHub HTML/annotations, independently of API access.
The cloud's api.github.com tunnel returned403; successful Git access is separate.
A stable-tag guard additionally refuses publication while the compatibility
manifest says the app does not render through True Engine or SDK capabilities
remain blocked. Future actual editor acceptance must supplement the probe; a
standalone rendering test is not production integration.

## Actual remote CPU/GPU and Windows launcher verification

[GitHub run38996217608](https://github.com/BirthrightPublication/License-Plate-Obfuscation/actions/runs/38996217608) tested
implementation commit `9d278f846a2def5eb7751a72918b31b62042a559`.
Public annotations confirm Windows38Python tests passed with0skips, including
actual cmd.exe primary/alias execution; Ubuntu37passed/1Windows-onlyskip.
SDK consumer tests passed4CPU+1rendered-pixel test on each platform. Ubuntu used
Mesa llvmpipe LLVM20.1.2/Vulkan; Windows used Microsoft Basic Render Driver/DX12.
These are software adapters, not consumer hardware or interactive-window tests.
Full exact scope and initial failure history: docs/true-engine-sdk-test-results.txt.

Initial run38995978921 failed six Windows fixture comparisons because TEMP used
an8.3path alias while dispatch canonicalized to the long name; the fixture now
uses the same actual directory, keeping assertions intact. Initial Linux GPU
runs failed with no adapter, never skipped. Explicit Mesa driver setup fixed that
runner prerequisite. No render assertion or SDK requirement was relaxed. The complete run then finished **Success**. Its windows-package job built the
existing prototype into native EXEs and passed the actual packaged Start batch,
checksum/manifest verification, native installation, interrupted-rename recovery,
personal-marker preservation, HTTP/ES-module startup and Chromium
editing/save/reopen/export/import checks. It uploaded a development candidate
artifact. Tag-only publish/live-update jobs were skipped; no stable release or
live public update is claimed for this branch. This package still contains the
unintegrated CSS prototype, not the requested engine editor.

## Result and limitations

Local development/testing is available. SDK0.1 lacks orthographic and suitable
plate-text/custom-mesh submission, so the complete requested editor is blocked.
The production app stays the rejected experimental CSS prototype0.1.2. No new
version/tag/package/checksum or integrated Windows release is claimed. Existing
release files, projects/settings/browser data, scripts and source are preserved.

---

# 0.1.2 release/update validation

Current local environment: Linux, Python 3.12.14, Node 24.19.0. Local `npm test`
passed **5 Node tests and 27 Python tests**, 0 failed/0 skipped. The Python total
includes 18 new GitHub updater tests plus 9 existing launcher/legacy updater tests.

New tests cover stable asset selection and exact repository URLs, numeric versions,
HTTP transport/download orchestration using injected fixture responses, checksum
rejection, archive traversal/reserved/case-collision rejection, manifest tampering,
full install/update/rollback, post-activation and staging failures, interrupted
rename/activation recovery, rollback failure, exclusive update locks, offline
failure and preservation of marker files for projects, original/processed media,
outputs, presets, preferences/history, templates, custom tools, Build source and
unknown personal files. Unknown/modified files in app refuse updates. Fixture
EXEs are fake bytes and are not claimed as native executable validation.

Actual GitHub Actions run [38992808983](https://github.com/BirthrightPublication/License-Plate-Obfuscation/actions/runs/38992808983) passed on source commit cdde601 (full SHA recorded in Git). Both Windows and Linux unit jobs passed. The Windows-package job passed its real native build, complete ZIP/checksum/manifest checks, both EXE self-checks, Start Plate.bat, native installation and interrupted recovery with personal marker files intact, loopback HTTP/JS delivery, Chromium editing/save/reopen/export/import and artifact upload. This is actual Windows runner validation, not simulated Linux execution. A prior initial Windows job failed; exclusive Windows socket binding was corrected and subsequent Windows runs passed. Superseded branch runs were cancelled intentionally.

This validates the implementation before release. The final tag workflow rebuilds its exact source and must pass the same checks before publication. The live public download/update job runs only after publication; its actual result and permanent release report must be verified separately.
Stable tag publication uploads a draft full ZIP/checksum and native report,
re-downloads them with gh and verifies SHA-256, then publishes. A development build
or successful Git push does not prove this publication/download step succeeded.
Live latest-release updates cannot be asserted until a compatible stable release
actually exists and the operation succeeds. API access from this cloud has returned
HTTP 403; no GitHub asset-upload success is claimed here.

No current True Engine compatibility tests exist: SDK/version/commit absent.
No production legal/data-provider claims, code signing, performance benchmarks,
new editor controls or media-processing features are included. Prior 0.1.0/0.1.1
source, ZIPs and test records remain preserved in tags and release history.

## Completed v0.1.2 publication and live update

Run [38992985878](https://github.com/BirthrightPublication/License-Plate-Obfuscation/actions/runs/38992985878) validated exact tagged source a04ce38494241d69b268b1f12cb04eae724a15ec, published the complete Windows ZIP/checksum and native report, and passed its real public updater acceptance on Windows. The final job attached live-update-test-report.txt successfully; the withdraw-to-draft failure step was skipped. The public ZIP was independently downloaded here and its outer checksum, app manifest and exact source commit verified. No source archive was substituted for an executable installation package.

SHA-256: 3fa3cbf5c4f9e3569ab424f00a128a2ac4deb6b24234de98cf6ba5d50faa9938. Permanent native/live reports, package manifest and changed-source-file inventory are under docs/releases/v0.1.2-*. Earlier pre-publication statements are chronological evidence; this completed run establishes publication and live-update success. Consumer Windows 11 hardware, default-browser auto-opening and unsigned-download prompts still require the user's manual first-use checklist; hosted Windows validation does not cover every PC configuration.

## Development-hold installation audit — 2026-10-16

This iteration changed documentation/classification only. Inspected the full tracked inventory, launcher/helper/build/updater source, UI code, workflow, manifests and Build files; incorporated the user's screenshot as evidence of a source-layout folder with no visible app. The screenshot's full Windows path and Build contents were not visible.

Read-only checks now verified the published 0.1.2 archive SHA-256, all five managed file hashes against its app manifest, exact tagged source commit, complete ten-file ZIP inventory and both EXEs' PE x64 machine type 0x8664. Source checkout app/EXEs, recovery updater and legacy Installed/current.json are absent. Read authoritative PyInstaller 6.16.0 dependency metadata without installing it. The real compatibility file is true-engine.compatibility.json (hyphen).

No new tests of application behavior or Windows execution are claimed. Unit/browser/native tests were not rerun for this documentation-only audit. No build/dependency installation, extraction into an installation, updater, repair, rollback, migration or destructive test was run. Earlier successful Windows/native/browser/live-update records remain historical packaging/prototype evidence, not a working SDK or approved professional editor. No new version/release/tag/patch was created. Documentation commits intentionally skip CI to avoid generating new candidate packages during the hold.
