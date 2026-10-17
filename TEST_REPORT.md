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

The GitHub Actions workflow is configured to run tests on Windows and Linux,
build real self-contained x64 EXEs, validate full ZIP/checksum/manifest structure,
execute both EXE self-checks and Start Plate.bat, install and recover a real native
package, serve its UI, and run Chromium editing/save/browser-reopen/export/import
checks against the frozen host. These Windows/Actions checks are **not yet confirmed
in this local report**; consult actual workflow results and the generated
windows-test-report.txt artifact. Local Linux tests do not establish Windows readiness.

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
