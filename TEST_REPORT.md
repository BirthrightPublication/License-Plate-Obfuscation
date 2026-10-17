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
