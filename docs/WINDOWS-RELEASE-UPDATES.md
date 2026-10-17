# Current source launcher repair and release gate

Start Plate.bat and Update Plate.bat are the primary user-facing launchers in
current source; uppercase START/UPDATE APPLICATION.bat are compatibility aliases.
They prefer installed native EXEs; source-only mode uses tools/windows_entry.py
and the existing Python helper. Source start labels the old unintegrated CSS
prototype. Source update asks typed INSTALL confirmation before creating app/;
read-only --check never downloads/installs. Native-only packages remain Python-
free. These changes do not migrate an existing user folder or refresh old root
BAT files automatically. The native updater intentionally never overwrites
existing root scripts; a future repair requires exact paths and verified backups.

The separate SDK consumer workflow is now a required packaging dependency, and
new stable tags are refused while application integration is incomplete. Current
selected engine0.1.2/SDK0.1 lacks required orthographic/text APIs; no new integrated
release is available. Full evidence and unrun Windows checks: TEST_REPORT.md.
The following contract describes the existing native0.1.2 update system.

# Windows GitHub release / update contract (protocol 1)

Target installation: `B:\License Plate Studio`. Target source/build directory:
`B:\License Plate Studio\Build` (clone source in Build\Source if desired).
No engine repository changes or new editor features are part of this iteration.

## Stable asset and source contract

A stable `vMAJOR.MINOR.PATCH` Git tag must exactly match package.json. The Actions
workflow tests that tagged source on Linux and Windows, builds on Windows x64 with
Python 3.12/PyInstaller 6.16.0, tests the native installation and browser workflow,
and uploads the following exact names to a draft GitHub Release:

- `License-Plate-Studio-v[VERSION]-windows-x64.zip`
- `License-Plate-Studio-v[VERSION]-windows-x64.zip.sha256`
- `windows-test-report.txt`

It re-downloads draft assets and verifies the checksum before publishing the
stable release. A final Windows job exercises the real public updater API/download, native install, data preservation and already-current path; it attaches its report permanently. If this post-publication acceptance fails, the release is returned to draft for diagnosis without deleting assets/history. Failed pre-publication tests do not publish a stable release. Source-code archives
are never substituted for installers. Existing releases/assets are not clobbered;
a pre-existing release makes creation fail for manual diagnosis. Workflow artifacts
from development branches are test candidates, not stable releases. A successful
branch build is not proof that tag publication or asset upload succeeded.

The ZIP has a complete app directory containing PlateStudio.exe, PlateUpdater.exe,
app/manifest.json, compatibility information, changelog and limitations. Both EXEs
embed their own Python runtime; the studio EXE embeds the existing browser UI and
asset-integrity metadata. Root Start/Update/Rollback batch files and first-use
instructions are also supplied. A current system browser remains a prerequisite.
Executables are unsigned. No Python/Node installation is required on end-user PCs.

Manifest protocol 1 records application identity, windows-x64, semantic version,
exact source SHA and every managed app file hash. No True Engine SDK is integrated;
its version is null rather than fabricated. Changing that dependency requires an
explicit SDK version/commit and compatibility testing in its own authorized task.

## First installation and legacy installations

Verify the ZIP checksum and extract into a NEW empty destination. Do not overwrite
an existing app directory, source checkout, old launchers or user files. This is a
one-time bootstrap, after which Update Plate.bat does all downloads/extraction.
Earlier v0.1.0/v0.1.1 folder layouts are not automatically migrated; leave their
folders/ZIPs intact and export backups before moving to the new installation.
Browser storage is preserved by using the same profile and localhost:4173 origin.
There is one project slot; important research notes require a separate backup.

## Transaction and recovery

The root batch file starts the packaged updater with --bootstrap. Before touching
app, it copies itself to .plate-studio/runners/<id> and creates a durable recovery
updater outside app. The parent exits so Windows can release its old EXE. A worker
uses an OS file lock, released automatically if the process dies, and recovers any
prior journal before contacting GitHub. It checks only the public repository's
latest stable release and exact Windows asset names. Numeric version comparison
prevents lexical errors, silent downgrades and reinstalls. Only public HTTPS API/
GitHub asset hosts are allowed, including redirect targets; TLS verification stays
on. No user GitHub credential is requested or stored.

The worker verifies the downloaded outer SHA-256, saves a non-conflicting copy in
Build, rejects unsafe/colliding/linked ZIP entries, stages the complete app and
verifies manifest coverage/hashes and the native --check result. It refuses to
replace an existing app with unknown extra files or modified managed files. Root
launchers are created only if absent; existing root files are never overwritten.

Before renames, a flushed journal records a transaction id. Old app is renamed to
.plate-studio/backups/<id>/app, staged app is activated, and native integrity checks
run again. Failure restores the prior app and retains failed code separately.
After success, backups remain; there is no automatic deletion/garbage collection.
Interrupted transactions recover on the next run, including the gap between app
renames. The root batch file falls back to the durable recovery updater if app is
missing. Explicit Rollback Plate.bat restores the most recent prior verified backup
and preserves the displaced current version too. Do not delete .plate-studio.

Renames are atomic on the same volume, but a power failure does not make an entire
directory swap a single operation. The journal and external recovery launcher
provide recovery, not a claim of impossible disk-failure immunity. If Windows locks
files, the updater retries briefly then reports that Studio must be closed; it
does not kill unrelated processes. Storage corruption, absent backups or manual
changes require diagnosis without deleting unknown files. No application data is
stored in replaceable app, and no data/schema migration runs in this update.

## Never-overwrite boundary

The updater never scans/replaces arbitrary installation-root files. ALL paths
outside app are preserved, not merely a short list. In particular:

- Projects/, Media/, Original Media/, Processed Media/, Output/, Exports/
- Presets/, Templates/, Configurations/, custom scripts/tools and assets
- settings.json, export-preferences.json, history.json and unknown config names
- Build source checkouts and previous build/patch files (new release files only)
- Browser localStorage, user profiles and external data anywhere else

.plate-studio is reserved updater storage: logs, lock/journal, downloads/stages,
backup/failed app versions and external updater runners. No code writes to True
Engine or an old installation elsewhere. Never put personal files in app. If they
are there, updates refuse rather than deciding which user file may be discarded.

## Validation and publication limitations

Local tests use explicit fake-runtime fixtures and injected transport/probe hooks
for deterministic failure coverage; they do not claim those fixture EXEs run. The
Windows job separately executes real frozen EXEs, Start Plate.bat, native install
and interrupted recovery, loopback HTTP/JS delivery and real Chromium UI checks.
Live asset download is checked in the draft-release publication job; branch tests
simulate GitHub responses and do not claim a live published update was downloaded.

GitHub Release creation requires repository contents-write permission and usable
api.github.com/uploads.github.com access. Native Git push permission does not prove
those operations are allowed. A draft network change is not runtime activation.
Record actual workflow/run/release results before declaring the release complete.
