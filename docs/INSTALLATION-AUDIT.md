# V0.1.2 installation and launcher audit

Audit date: 2026-10-16 (America/Los_Angeles). Audited repository baseline:
`6628330557541f1e59fabe4f41db780b4d455398`. Published prototype tag v0.1.2:
`a04ce38494241d69b268b1f12cb04eae724a15ec`.

**Development hold. V0.1.2 is an experimental prototype. The current interface is
not approved and is not the final Plate Studio design.** Successful packaging and
update tests did not establish a professional 3D editor or True Engine integration.

## Evidence and scope

The complete tracked-file inventory, entry scripts, Python launch/build/updater
implementations, package/compatibility manifests, browser code, workflow, existing
test reports and local Build inventory were inspected. No installer, updater,
repair, dependency installation or build was executed for this audit. No existing
scripts, source assets, binaries, projects or settings were deleted or moved.

The user's screenshot shows `.github`, Build, docs, src, tests and tools, plus the
source/developer batch files and native batch files together. It shows no app
folder. This matches the source distribution layout, not the complete native
installation layout. The screenshot's address bar is not visible: the full Windows
folder path and the contents of its Build directory are not established. It does
not distinguish Git clone from extracted source archive or a manual file copy.

In this cloud checkout, `app/`, `app/PlateStudio.exe`, `app/PlateUpdater.exe`,
`.plate-studio/recovery-updater.exe` and `Installed/current.json` are all absent.
Those are direct filesystem observations, not assumptions about the user's disk.
The screenshot independently confirms the missing app folder in the folder shown.

## Why the three launch paths behave differently

All batch files use `%~dp0`: the directory of THAT batch file. They do not search
B:, other release folders, Build subdirectories or the current GitHub source tree
for a compatible installation.

| Script | Exact code path | Required layout and result |
| --- | --- | --- |
| START APPLICATION.bat | Line 4 calls tools/run-python.bat with tools/launch.py | Source/developer route. Python 3.12+ executes the local host; no native EXE is required. |
| Start Plate.bat | Lines 4–9 test and execute `%~dp0app\PlateStudio.exe` | Native route. The screenshot's missing app folder makes this guard fail before any application code executes. |
| Update Plate.bat | Lines 4–11 select `%~dp0app\PlateUpdater.exe`, then `%~dp0.plate-studio\recovery-updater.exe` | If neither path exists, it prints the reported missing-updater message and exits BEFORE GitHub is contacted. A source checkout cannot bootstrap this native updater. |
| UPDATE APPLICATION.bat | Line 5 runs tools/updater.py against local Build and Installed, then START APPLICATION.bat | Legacy Python updater, not the native GitHub updater. |
| ROLLBACK APPLICATION.bat | Line 4 uses the same legacy updater with --rollback | Requires Installed/current.json and a prior Installed/versions slot. Not the native backup journal. |
| Rollback Plate.bat | Lines 4–11 use the native updater/recovery EXE with --rollback | Requires a native updater and a retained .plate-studio backup. Not a legacy Installed rollback. |
| INSTALL DEPENDENCIES.bat | Calls run-python; if missing, uses WinGet Python.Python.3.12 --scope user | Installs/checks Python for the source/developer route. It does NOT install PlateStudio.exe, PlateUpdater.exe or True Engine. |
| BUILD WINDOWS.bat | Line 4 calls tools/build_windows.py via run-python | Builds a ZIP; does NOT install its app folder beside Start Plate.bat. |
| VERIFY RELEASE.bat | Calls tools/verify_release.py | Checks root release.json's FOUR browser asset hashes; this does not prove a complete native installation. |

The source host's `application_root()` in tools/launch.py first checks the legacy
Installed/current.json pointer, otherwise serves source root assets. In this
checkout there is no pointer, so it serves index.html and src/*.js/css. On a
machine with that legacy pointer, it may instead serve the pointed legacy version;
package.json alone would not prove which legacy project was launched.

This is a distribution/entry-point mismatch. In the pictured directory, the EXEs
required by the native launchers were not supplied at their expected paths. It is
not evidence of a GPU, antivirus, GitHub credential, True Engine or checksum
failure. We have not established how that Windows folder was populated or whether
there is a separate complete installation elsewhere. A double-nested app folder
would also fail the same guard, but none is inferred from the screenshot.

The native Start error's suggestion to run Update is incomplete for this case:
without both a native updater and a recovery copy, Update cannot start either.
There is no unified source/installed-layout preflight or dedicated repair utility.
This confusing launcher coexistence is a packaging/UX defect, not user error.

## Verified contents of the actual native release ZIP

`Build/License-Plate-Studio-v0.1.2-windows-x64.zip` contains exactly:

```
app/PlateStudio.exe
app/PlateUpdater.exe
app/manifest.json
app/CHANGELOG.md
app/KNOWN_ISSUES.md
app/true-engine.compatibility.json
Start Plate.bat
Update Plate.bat
Rollback Plate.bat
README - FIRST TIME SETUP.txt
```

It does NOT include START APPLICATION.bat, BUILD WINDOWS.bat, INSTALL
DEPENDENCIES.bat, tools/, src/ or tests/. Those are source/developer files. The UI
and Python runtime are embedded inside the native EXEs; packaging them does not
change the UI into an engine-powered editor.

Read-only verification performed now:

- Full ZIP SHA-256 matched its published sidecar:
  `3fa3cbf5c4f9e3569ab424f00a128a2ac4deb6b24234de98cf6ba5d50faa9938`.
- Every managed file matched app/manifest.json's hash.
- Both executables have MZ/PE headers and machine type `0x8664` (Windows x64).
- Manifest source commit matches the preserved v0.1.2 tag.
- The archive contains the needed files; merely keeping the ZIP inside Build does
  not unpack or activate them. No extraction into a real installation was done.

## Build directory and manifest distinctions

This CLOUD Build directory contains the legacy 0.1.0 ZIP, the 0.1.1 portable-r2 ZIP
and sidecars/report, the 0.1.2 native ZIP/checksum, Windows/live reports, legacy
Build/release.json and SHA256SUMS.txt, and a retained validation-failed candidate.
The user's Build contents were not shown and must not be assumed identical.

Only `Build/.gitkeep` is tracked in Git. `.gitignore` excludes Build contents, so a clone/source archive does not obtain compiled ZIPs or EXEs from that directory. Release assets are distributed separately.

Generic `Build/release.json` / `Build/SHA256SUMS.txt` belong to the OLD 0.1.0 package.
They must not be used to validate a different ZIP. Use the exact filename-matched
0.1.2 `.zip.sha256` and the app manifest inside that ZIP.

Root package.json says 0.1.2 and invokes Python-based source tooling through npm.
It is not a native installation manifest. Root release.json explicitly covers
only four UI assets. Native app/manifest.json covers installed code and runtime.
RELEASE_MANIFEST.json describes historical release provenance; it does not prove
files were installed on the user's computer.

The actual compatibility filename is `true-engine.compatibility.json` (hyphen).
`true_engine.compatibility.json` (underscore) does not exist in this repository.
No current launcher uses the underscore filename, so this spelling difference is
not the cause of the launcher errors. The real manifest has SDK/package null,
no tested engine versions and status blocked-sdk-not-supplied.

## Precisely what BUILD WINDOWS.bat does

1. tools/run-python.bat selects `py -3`, falling back to `python`, checking >=3.12.
2. tools/build_windows.py refuses a non-Windows host. On Windows it creates a
   temporary venv using that interpreter.
3. It invokes the venv's pip to install tools/requirements-windows-build.txt:
   `PyInstaller==6.16.0`. This occurs BEFORE the packaging clean-tree/output checks.
4. Official PyPI metadata for that version lists the following applicable normal
   Windows/Python 3.12 dependencies: altgraph, packaging>=22.0,
   pefile>=2022.5.30 except 2024.8.26, pyinstaller-hooks-contrib>=2025.8,
   pywin32-ctypes>=0.2.1 and setuptools>=42.0.0. No test/completion extras are
   requested. Transitive resolved versions are not fully locked; a byte-identical
   reproducible build is not currently guaranteed. Metadata was read, not installed.
5. It runs tools/windows_release.py using the venv interpreter. That code checks
   Windows/x64 platform, a stable package version, Git HEAD and a clean TRACKED
   worktree. Git is required. Node 24 is needed by separate automated tests, not
   by the local compilation wrapper itself.
6. The builder rejects an already-existing same-name ZIP OR checksum. In this
   cloud Build, both 0.1.2 outputs already exist. A Windows source folder with the
   same files would refuse replacement after the wrapper's dependency step.
7. In temporary staging, PyInstaller freezes tools/launch.py as PlateStudio.exe
   and tools/github_updater.py as PlateUpdater.exe. Only the four explicit UI
   assets and generated runtime manifest are embedded in the studio host.
8. It adds manifests/docs/root native launchers, verifies hashes, executes the two
   native --check commands and validates a temporary extraction. The local wrapper
   does NOT itself run all unit/browser/installation tests; GitHub Actions does.
9. It writes the versioned windows-x64 ZIP and matching `.zip.sha256` into the
   source checkout's Build by default (`--output` can change the builder output).
   Temporary venv/build/extraction directories are cleaned by their contexts;
   normal pip/PyInstaller caches may persist under the Windows user profile.

There is no installation/repair call in this build path. It does not populate
`<script-folder>\app`, change Installed/current.json, migrate user data, replace
an installed app, fetch/compile True Engine or make the viewport GPU-engine-based.
It writes build outputs and temporary/cache files; it is not a substitute for a
confirmed installation repair. It was not run during this audit.

## Prototype reality and verification limits

src/style.css uses CSS perspective/rotateX/rotateY on an HTML plate. src/app.js's
Orbit input changes that CSS transform. There is no SDK package dependency, engine
adapter, GPU render-surface integration, scene graph or engine camera navigation.
The compiler wraps that same prototype in a browser-host EXE. The landing-page
intro is present in index.html. No visual or editor changes were made now.

Earlier Windows/Linux/native/browser/update tests remain historical evidence
for packaging and prototype behavior, not approval of the design or proof of an
engine integration. No Windows launcher was executed on the user's PC during this
audit. The full B: path, actual local versions and any separate native installation
remain to be confirmed before repair. See INSTALLATION-REPAIR-PLAN.md.
