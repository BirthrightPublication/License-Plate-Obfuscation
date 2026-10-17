LICENSE PLATE OBFUSCATION STUDIO
V0.1.1 - WINDOWS TEST PACKAGE (V0.1 packaging fixes; no new editor features)

WHAT THIS IS
This is a runnable browser application with a Windows batch launcher and a small
Python local web host. It is NOT a compiled Windows .exe, a True Engine build,
or the completed V0.1 milestone in the master roadmap. The browser renders the
plate with CSS 3D transforms. You do not need Node, npm, a compiler, or True Engine
to run this portable package. Python is a separately documented prerequisite.

The cloud build machine is Linux. It has no Windows runtime/compiler environment
for producing and testing a native Windows executable. BUILD WINDOWS.bat can
produce an optional self-contained .exe ON YOUR WINDOWS COMPUTER. That .exe still
opens the same browser UI; it does not add an engine viewport or new features.

QUICK INSTALL - WINDOWS 11
1. Download License-Plate-Obfuscation-Studio-0.1.1-Windows-Portable-r2.zip.
   Put the ZIP in B:\License Plate Obfuscation Studio\Build.
   If that folder does not exist, create it. Do not remove earlier ZIPs.
2. Optional but recommended: verify the ZIP against the separately supplied
   SHA256SUMS file. In PowerShell run:
   Get-FileHash -Algorithm SHA256 -LiteralPath 'B:\License Plate Obfuscation Studio\Build\License-Plate-Obfuscation-Studio-0.1.1-Windows-Portable-r2.zip'
   Compare the entire hash with the release checksum file. A checksum detects
   corruption, not publisher authenticity. Only use trusted release files.
3. Right-click the ZIP > Extract All. Choose a NEW empty folder:
   B:\License Plate Obfuscation Studio\Releases\0.1.1
   The folder must contain START APPLICATION.bat directly (not inside a second
   nested folder). If the destination is nonempty, choose a different new folder.
   Never extract over an earlier installation, source files, or user projects.
4. Have Python 3.12+ installed and a current Edge, Chrome or Firefox browser.
   If Python is missing, double-click INSTALL DEPENDENCIES.bat. It uses Windows
   Package Manager to install Python 3.12 for your user. Internet is required.
   If automatic installation fails, install from:
   https://www.python.org/downloads/windows/
   Include the Python launcher. No application Python packages need installing.
5. Double-click START APPLICATION.bat in the extracted folder.
   A console stays open and your default browser should open automatically.
   If the browser does not open, type http://localhost:4173 into it manually.
   Do not double-click index.html: ES modules need the supplied local host.
6. Keep the console window open while using the app. To quit, export a backup,
   close the browser tab, then press Ctrl+C in the console or close the console.
   To reopen, double-click START APPLICATION.bat and use the same browser profile.

B:\True Engine is your intended separate engine directory. This package does not
install, write to, or require that directory. No SDK version has been supplied.

WHAT YOU SHOULD SEE
A light cream/green page headed B / BIRTHRIGHT and the title 'A space to design.
A place to understand.' The header reads v0.1.1 FOUNDATION. On a wide window:
- Left: state selector, preview text and official source-link area.
- Center: grid background, generic cream plate initially reading STUDIO and
  California, an Orbit slider and Reset view button.
- Right: Unverified legal status and an unassessed compliance-risk explanation.
- Below: local project controls and a research-notes text area.
The page rearranges into stacked panels on a narrow browser window.
There is no standalone 3D-engine window or membership sign-in screen.

BASIC MANUAL TEST CHECKLIST
[ ] Launch: the console prints READY and the UI loads with no missing assets.
[ ] Rendering: select Texas; the state label on the plate updates immediately.
[ ] Text: enter ABC123; the plate updates without reloading. Lowercase typed
    interactively becomes uppercase. Preview syntax is not registration approval.
[ ] Mouse/orbit: drag the Orbit SLIDER with the mouse. The plate tilts sideways.
    Click Reset view and it returns to its initial angle. Keyboard arrow keys
    work on the focused slider. Dragging the plate itself does NOT orbit it.
[ ] Viewport: resize the browser; panels remain readable. No pan, zoom, wheel
    zoom, 3D object picking, geometry editing, or free-camera control exists.
[ ] Save: give the project a recognizable name; click Save on this device and
    confirm the saved message. This stores ONE project slot, not a file on B:.
[ ] Reopen: close the tab and stop/restart the launcher. Use the SAME browser
    profile and http://localhost:4173. Click Load saved project; the text, state
    and project name should return. Projects do not automatically load at startup.
[ ] Export: click Export backup; save the JSON to a personal Projects folder,
    such as B:\License Plate Obfuscation Studio\Projects. Change the preview,
    then Import backup, select that JSON, and verify it restores the project.
    Click Save after importing if you want it retained in the local save slot.
[ ] Notes: type a research note, reload the page and confirm it persists.
    Notes are NOT included in exported project JSON; copy important notes to
    a separate file before clearing browser data.
[ ] Availability: click Check availability options; expect an explicit
    unavailable-provider message, not an invented available/unavailable plate.
[ ] Legal: California, Texas and New York have official research links. All
    states remain Unverified; no numeric compliance-risk assessment is assigned.
    Live source currency and legal interpretation have not been verified.

DATA PRESERVATION AND TROUBLESHOOTING
Keep the same browser, profile and exact http://localhost:4173 origin. Switching
to 127.0.0.1, another port, private browsing or another profile changes storage.
One save overwrites the single browser save slot, so export before saving a new
project. Clearing browser/site data deletes projects and notes. Releases do not
read, delete or migrate B:\True Engine or personally created files.

If the console says the port is occupied, close the earlier Studio console and
try again. Do not change ports to look for old projects. If verification fails,
extract the trusted ZIP to another new folder; do not replace source files.
If Windows blocks a download, verify its source and hash; do not disable security
protections. The batch scripts and optional native EXE are unsigned.

OPTIONAL UPDATES AND ROLLBACK
Direct first-time launch does not require the updater. For its managed mode,
create Build under this extracted release folder, copy the full portable ZIP
there, then run UPDATE APPLICATION.bat. It finds the latest compatible full ZIP,
verifies every file hash and installs a new version under Installed\versions.
It never overwrites an existing version directory. The prior managed version is
retained and the activation pointer is replaced atomically after validation.
Root START APPLICATION.bat uses the managed active version if one exists.
An unsuccessful pre-activation update leaves the active version unchanged.
Only full releases are supported; patches are refused. Reapplying an installed
version is refused. Close the running server before updating.

ROLLBACK APPLICATION.bat switches back to the previous MANAGED installed version.
Initial install has no previous managed version. Old extracted releases and ZIPs
are left in place, so you can also close the server and launch an earlier folder
manually. A runtime/browser failure requires manual rollback; automatic recovery
is limited to refusing invalid packages before activation. Export backups first.

OPTIONAL LOCAL WINDOWS EXE BUILD
Prerequisites: Windows 11, Python 3.12+ (3.12 x64 recommended), Internet access to
pypi.org and files.pythonhosted.org, and a current browser. No Node is needed.
1. In the extracted full portable release, double-click BUILD WINDOWS.bat.
2. It creates an isolated temporary Python environment and installs
   PyInstaller==6.16.0 with normal TLS validation. It bundles the existing web UI
   and Python host into a console EXE, runs its --check asset-verification step,
   and writes a timestamped Native-0.1.1-* folder inside this release's Build.
3. That folder contains the native ZIP, checksum, EXE and native test manifest.
   Earlier builds are not overwritten. Build success is NOT a completed Windows
   interactive test: run the checklist above on the resulting EXE too.
4. Double-click LicensePlateObfuscationStudio-0.1.1.exe inside its app folder.
   End users of the resulting EXE do not need a Python installation.
The cloud did NOT execute this Windows build script. PyInstaller does not
cross-compile Windows binaries on Linux. There is no prebuilt Windows EXE in
this portable download. The build is reproducible by procedure, not guaranteed
to be byte-identical (PyInstaller's transitive dependencies are not hash-locked).

AUTOMATED TESTS AND VERSION EVIDENCE
See TEST_REPORT.md for actual current test results and unrun tests.
release.json lists every packaged file, SHA-256 hashes and changed files.
RELEASE_MANIFEST.json and true-engine.compatibility.json describe versions.
Run VERIFY RELEASE.bat to check ALL packaged file hashes after extraction.
Node 24 is needed only to run the source's Node domain tests, not to use the app.
No future roadmap phase is included in this release.
