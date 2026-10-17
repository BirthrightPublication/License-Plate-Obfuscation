# Architecture — prototype and authorized engine integration restart

The V0.1.2 interface is not approved as the final product. The owner authorized integration restart with published True Engine v0.1.2. The SDK assessment identifies hard orthographic/text APIs missing before the complete editor can be built. No independent renderer or fake engine bridge is permitted.

## Existing code

index.html and src/* are a browser prototype using standard ES modules and CSS
perspective transforms. The plate is an HTML element. There is no engine scene,
mesh renderer, camera/picking system or True Engine SDK adapter. The large intro
is present in the HTML and is not the future professional editing shell.

Project schemaVersion 1 stores name/state/text in browser localStorage key
birthright.plate.project.v1. Notes use birthright.plate.notes.v1 and are not included
in JSON exports. Preserve original exports, notes, same profile and localhost:4173.
No migration or project schema change is part of this audit.

The source host tools/launch.py serves four allowlisted UI assets after root
release.json validation, or a legacy Installed/current.json selection. START
APPLICATION.bat now forwards to primary Start Plate.bat; source-mode routing invokes that Python route. This can work without a native app.

The distinct native distribution freezes the same host/UI in app/PlateStudio.exe,
plus app/PlateUpdater.exe. Native Start/Update batch files require that layout
beside themselves. The repaired primary launchers recognize source mode separately; uppercase Update no longer invokes the legacy slot updater. A source checkout has no app directory; native files in a Build
ZIP are not automatically installed. The screenshot matches the source layout.

Legacy tools/updater.py manages Installed slots from root release.json full ZIPs;
newer tools/github_updater.py manages app with app/manifest.json, backups/journal
and an external updater copy under .plate-studio. Both are full-package systems;
neither implements the proposed patch or repair contract. Do not combine them as
one interchangeable installation or erase their histories.

## Proposed architecture (not implemented)

- [Installation audit](docs/INSTALLATION-AUDIT.md): exact paths, failures, build
  side effects and source-versus-native evidence.
- [Installation/repair plan](docs/INSTALLATION-REPAIR-PLAN.md): one Start, one Update,
  one Repair entry point; independent maintenance bootstrap; developer files under
  Build/Source; versioned full/patch contracts and protected data boundaries.
- [True Engine/UI architecture](docs/TRUE-ENGINE-UI-ARCHITECTURE.md): engine-owned
  GPU scene/viewport/input, a thin documented-SDK adapter, domain commands/project
  storage, compact professional shell and separate source-linked legal metadata.

## Selected SDK compatibility boundary

True Engine0.1.2/SDK0.1 is pinned by immutable Git commit in the separate
integration/true-engine-sdk-probe. It owns shaders, geometry submission, camera
projection, picking and GPU draw calls. The consumer test owns an offscreen target
and device lifecycle as documented; it is not the production app or a UI host.
See docs/TRUE-ENGINE-SDK-ASSESSMENT.md for supported capabilities, exact missing
APIs and next native-host requirements. No engine source is copied or modified.
The production CSS assets, schema and storage remain unchanged. Native editor
hosting can be implemented only after the complete requested capability contract
exists; no CSS or custom renderer fallback will fill those gaps.
