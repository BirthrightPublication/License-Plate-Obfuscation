LICENSE PLATE STUDIO - WINDOWS X64 RELEASE / UPDATE SYSTEM
Version 0.1.2 release candidate. Consult the GitHub Release's Windows test report
for actual build/test status. Source alone is NOT an installation ZIP.

SUPPORTED INSTALLATION
Windows 11 x64 and a current Edge, Chrome or Firefox browser. The standardized
installation package embeds its Python runtime. No Python or Node installation
is required to use the Windows release. True Engine is not integrated or required.

FIRST INSTALL (ONCE)
1. From https://github.com/BirthrightPublication/License-Plate-Obfuscation/releases
   download BOTH assets:
   License-Plate-Studio-v[VERSION]-windows-x64.zip
   License-Plate-Studio-v[VERSION]-windows-x64.zip.sha256
   Do NOT download GitHub's automatic 'Source code' archives as an installer.
2. Keep downloads under B:\License Plate Studio\Build. Verify the ZIP's SHA-256
   with PowerShell Get-FileHash and compare the full hash with the .sha256 file.
3. Extract the ZIP to a NEW EMPTY folder. It contains app/, Start Plate.bat,
   Update Plate.bat, Rollback Plate.bat, and this guide.
   Recommended installed location: B:\License Plate Studio. If that directory
   already contains application code, first extract into a separate new folder;
   do not approve overwriting existing files. Preserve the old installation.
   Build and personal data are allowed alongside app, but first extraction must
   never overwrite a pre-existing app or root launcher. No silent legacy migration.
4. Double-click Start Plate.bat. Keep its console open. The browser opens at
   localhost:4173. Use the same browser/profile/origin for existing saved projects.
5. Test the checklist below before relying on the installation.

ONE-CLICK UPDATES
Close the application console before updating. Double-click Update Plate.bat.
It copies the updater out of app so Windows can replace all app files, checks
GitHub's latest stable release, compares numeric versions, downloads the exact
compatible Windows ZIP and checksum, verifies them, stages the new app, runs its
native integrity self-check, backs up the old app, activates and verifies the new
app. If validation/activation fails, it restores the previous app automatically.
No administrator privileges are needed when the installation folder is writable.
Progress/errors remain in a console and .plate-studio\logs. Downloads remain in
Build; backups remain in .plate-studio\backups; failed code is retained separately.
The updater does not force-close processes or kill an application in use. If files
are locked, close Studio and retry; the original app is restored/retained.

Recovery after power loss: run Update Plate.bat again. Its recovery-updater fallback
can restore the old app if app/ is temporarily missing. The OS releases the update
lock after a crash. Recovery occurs before any new network request. Keep the
.plate-studio directory. No backup is automatically garbage-collected. A network
failure may be reported after successful recovery; Start Plate.bat can then open
the restored version. Rollback Plate.bat selects the most recently retained prior
verified version. Initial installation has no prior version to roll back to.

NEVER-OVERWRITTEN DATA
Only app/ is replaceable, and only when its entire file inventory and hashes match
its install manifest. Do not place user data inside app/. Unmanaged files or local
code/config modifications there cause update refusal instead of deletion.
Everything outside app/ is preserved, including:
Projects, Media, Original Media, Processed Media, Output, Exports, Presets, Templates,
Configurations, settings.json, export-preferences.json, history.json, custom tools,
and ANY other unknown personal file/folder. Build source checkouts are untouched;
only new, non-conflicting release ZIP/checksum files are added there. Existing root
launchers are not overwritten. .plate-studio is updater-owned recovery/log storage.
Browser localStorage is outside the installation. It stores one project slot and
research notes; clearing browser/site data deletes those. Export project backups
before saving another project. Notes are not included in project JSON exports.

WHAT TO EXPECT / MANUAL TEST CHECKLIST
The existing light cream/green Birthright studio loads with a generic STUDIO plate
on a grid, state/text controls, Unverified legal status, and project/research panels.
[ ] Plate and controls render without missing assets.
[ ] Change state to Texas and text to ABC123; both update immediately.
[ ] Drag the Orbit SLIDER with the mouse and click Reset view. Dragging the plate
    itself, pan, zoom and free-camera control are NOT implemented.
[ ] Save a named project, close the browser and console, restart Start Plate.bat,
    and click Load saved project in the SAME browser profile/origin.
[ ] Export a JSON backup, change the text, import the JSON, and verify restoration.
[ ] Type a research note and reload. It should remain; copy important notes to a
    separate file before clearing browser data.
[ ] Availability displays an explicit unavailable-provider message. All legal
    assessments stay Unverified; compliance risk is unassessed.
[ ] After an update, confirm saved project/notes and personal files still exist.
There is no new media-processing functionality in this application. Existing
external tools/media/configurations are preserved without being modified.

BUILD FROM SOURCE (DEVELOPERS)
GitHub source/build files belong in B:\License Plate Studio\Build (for example
Build\Source). On Windows x64 with x64 Python 3.12 and Node 24, use BUILD WINDOWS.bat.
It installs the pinned PyInstaller build requirement in an isolated temporary
venv and runs tools/windows_release.py. A clean Git commit is required; generated
packages include its full SHA. Output uses the exact standardized filenames in
Build and refuses to overwrite an earlier build. The workflow runs tests before
publication and attaches a Windows-native test report. Linux cannot cross-compile
this distribution. A current browser remains a separate system prerequisite.
The executables are unsigned; do not disable Windows security protections.

DETAILS
See docs/WINDOWS-RELEASE-UPDATES.md, TEST_REPORT.md and KNOWN_ISSUES.md in source.
Github API/download failures must leave the installed app untouched. Only the
public Birthright repository and HTTPS GitHub asset hosts are used; no token is
needed on the user's Windows computer. Stable updates do not install prereleases
or silently downgrade. A SHA-256 checksum is integrity evidence, not a publisher
signature or protection against a compromised release publisher.
