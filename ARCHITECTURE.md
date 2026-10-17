# Architecture — experimental prototype on development hold

The V0.1.2 interface is not approved as the final product. This document separates
what exists from proposals. No competing renderer or visual implementation is
authorized before a tested True Engine SDK and explicit restart approval.

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
APPLICATION.bat invokes that Python route. This can work without a native app.

The distinct native distribution freezes the same host/UI in app/PlateStudio.exe,
plus app/PlateUpdater.exe. Native Start/Update batch files require that layout
beside themselves. A source checkout has no app directory; native files in a Build
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

The SDK must define the actual host/render/input contract. Do not invent APIs or
implement a local engine fallback. A working engine proof must precede any editor
redesign; explicit user restart approval is also required. No app version, source
implementation, launcher, existing installation or project was changed by this
architecture documentation update.
