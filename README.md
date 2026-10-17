# License Plate Obfuscation Studio

> **Integration restart:** the owner selected True Engine v0.1.2 / SDK 0.1. The published application remains an experimental browser prototype; it does not render through True Engine. The selected SDK lacks orthographic rendering and suitable text/custom-mesh submission. See the [SDK assessment](docs/TRUE-ENGINE-SDK-ASSESSMENT.md), [engine feature request](docs/TRUE-ENGINE-FEATURE-REQUEST.md), and [separate SDK compatibility probe](integration/true-engine-sdk-probe). No integrated release is published by this iteration.

`Start Plate.bat` is the primary launcher for source and complete native layouts; `START APPLICATION.bat` forwards to it. Source mode is explicitly labeled as the old prototype. `Update Plate.bat` is the primary updater; `UPDATE APPLICATION.bat` forwards to it. A source-only update requires confirmation before installing native app files; it does not silently use the incompatible legacy slot updater. Read-only `--check` diagnostics do not download or install. Existing projects, browser origin, settings, media, source, old scripts and packages remain preserved. These source changes do not update scripts already installed on your PC.

Authoritative source: [BirthrightPublication/License-Plate-Obfuscation](https://github.com/BirthrightPublication/License-Plate-Obfuscation), stable branch main. True Engine is a separate repository; no SDK is integrated. No open-source license has been selected.

The 0.1.2 release/update iteration adds a GitHub-based Windows distribution system to the existing V0.1 educational browser foundation. It does not add editor features or complete the V0.1 roadmap. A source checkout is not an installer. Actual Windows build/publication status must be read from Actions and the release's Windows test report.

## Install and update

Use the completed stable GitHub Release's `License-Plate-Studio-v[VERSION]-windows-x64.zip` and matching `.zip.sha256`, not GitHub source archives. Verify and extract once to a new empty installation, recommended `B:\License Plate Studio`. The ZIP includes complete `app/` runtime, code and launch components. Python/Node are not required to run it; a current browser is required. Start with `Start Plate.bat`. Close Studio and double-click `Update Plate.bat` for subsequent stable updates. `Rollback Plate.bat` restores a retained prior version. Never extract over older application/source/data files.

Keep source/builds under `B:\License Plate Studio\Build`. All user data lives outside replaceable app. The updater preserves every other root path, including projects, media, outputs, presets, templates, settings and unknown configurations. Browser localStorage remains profile/origin-specific; keep localhost:4173 and export project backups. Backups/logs/recovery live under .plate-studio. Unknown or changed files inside app cause update refusal.

See [first-time instructions](README%20-%20FIRST%20TIME%20SETUP.txt) and [transaction/never-overwrite contract](docs/WINDOWS-RELEASE-UPDATES.md).

## Develop and release

Read AGENTS.md, NEXT_ITERATION.md and docs/GITHUB-REPOSITORY-RULES.md. Fetch, inspect and work on a dedicated branch. `npm test` runs Node/Python tests. `python3 tools/release.py --prepare` refreshes development UI integrity metadata; `npm start` runs the local host. With Playwright 1.62.1 supplied outside source, run `CHROMIUM_PATH=/usr/bin/chromium node tools/smoke.cjs` against it. No user-facing cloud localhost preview is supported.

On Windows x64 with Python 3.12 and Node 24, BUILD WINDOWS.bat installs pinned build requirements in a temporary environment and creates the standardized package from a clean commit. GitHub Actions runs both OS test suites, builds and tests real Windows binaries/browser behavior, and publishes complete stable assets only on a version-matching tag after tests pass. Development branch runs produce candidate artifacts. Earlier tag/package associations remain in docs/releases/history.json; immutable source and binary histories must not be overwritten.

The UI still provides an illustrative CSS 3D plate, Orbit slider/reset, 50-state selector, preview text, one browser save slot, JSON import/export and research notes. It has no engine mesh viewport, pan/zoom, dark theme, current official style/eligibility dataset, authoritative availability, membership or vehicle models. Legal status remains Unverified and risk unassessed; no identification-evasion optimizer is provided.
