"""Create GitHub Release notes from the exact checked-out source/tag."""
import json
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[1]
version=json.loads((root/'package.json').read_text())['version']
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
print(f'''License Plate Studio v{version} — Windows x64 release/update maintenance

Source: `{sha}` (tag `v{version}`). No new editor features or True Engine changes.

The installation ZIP contains app/PlateStudio.exe and app/PlateUpdater.exe with
embedded Python runtimes. A current system browser is required; Python/Node are
not required on the user's computer. GitHub's source archives are not installers.

First use: verify the .zip.sha256 file, extract to a NEW empty installation folder
(recommended B:\\License Plate Studio), and launch Start Plate.bat. Preserve any
existing installation instead of extracting over it. Keep sources/builds under Build.
For subsequent updates, close Studio and double-click Update Plate.bat. The
updater checks the latest stable release, verifies the ZIP hash and per-file
manifest, stages and tests the runtime, retains backups and restores the previous
app on validation/installation failure. Rollback Plate.bat performs manual rollback.

Persistent data outside app/ is never replaced. This includes projects, media,
outputs, presets, configurations, preferences/history and browser localStorage.
Unmanaged/modified files inside app/ cause refusal. Keep the same browser profile
and localhost:4173 origin. Backups are retained under .plate-studio/backups.

Required assets: License-Plate-Studio-v{version}-windows-x64.zip and matching
.zip.sha256. The attached Windows test report records actual native/build/browser
checks for this package. The workflow also ran Node domain and Python updater,
recovery, downloader and preservation tests on Linux and Windows before release.

True Engine: NOT INTEGRATED; version/commit unavailable, compatibility untested.
The existing CSS browser preview remains a partial V0.1 foundation: no engine
mesh viewport, pan/zoom, dark theme, official artwork/eligibility rules or live
availability provider. Windows packages are unsigned. Hashes detect corruption,
not publisher compromise. No open-source license has been assigned.
''')
