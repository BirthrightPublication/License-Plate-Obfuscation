# True Engine integration gate and proposed editor architecture

**PLAN ONLY. No renderer, engine adapter, camera system, revised UI or feature
version is implemented here. The current CSS prototype is not approved.**

## Permanent engine boundary

True Engine is the permanent 3D foundation and lives in its own repository:
https://github.com/BirthrightPublication/True-Engine. Plate Studio must consume a
tested, versioned SDK, not copy its source, modify the engine repository or build
a competing renderer. CSS transforms must never be described as engine integration.

Current evidence: true-engine.compatibility.json has sdkPackage/sdkVersion null,
no tested engine versions and blocked-sdk-not-supplied. package.json has no engine
SDK dependency. Browser code manipulates HTML/CSS, not an engine scene. The studio
EXE embeds this browser host; native packaging did not add an engine. This does
not determine what may exist in the separate engine repository; it establishes
that Plate Studio has no selected/delivered/tested SDK integration.

## Required gates before any redesign implementation

1. User explicitly approves restarting the relevant True Engine development in
   its OWN project. This audit is not that approval and changes no engine files.
2. Engine maintainers deliver a designated tested SDK release or commit, package
   source/artifact/checksum, authoritative API documentation, supported Windows
   host/embedding contract, runtime dependencies, compatibility/license terms,
   and evidence that its sample runs on the target GPU/platform.
3. Record exact SDK version/commit and API/ABI constraints in the existing
   compatibility manifest. Do not invent a version, API symbol or minimum SDK.
   Until delivery, those fields remain null. Missing capabilities become explicit
   requests to engine maintainers, not private API calls or local engine copies.
4. After explicit integration approval, run an isolated Windows SDK proof against
   documented interfaces: attach a supported render surface, render a real mesh,
   resize, navigate camera with real mouse input, select/edit an object, release
   resources, and reopen the scene. Test device/error handling and supported
   software/driver combinations as the SDK contract permits. Evidence must show
   True Engine owns rendering, not a CSS/WebGL substitute written in this app.
5. Only after engine operation is proven AND the user approves resuming Plate
   Studio work may the approved editor design be implemented. A working SDK alone
   does not automatically lift the development hold or authorize V0.2.

SDK changes later require an exact dependency update, compatibility matrix,
application regression tests and release notes. Engine changes belong in a
separate engine task/repository, not this application's working tree.

## Responsibility split (capabilities, not invented SDK calls)

| Layer | Responsibilities |
| --- | --- |
| True Engine SDK | GPU rendering/resources, scene objects, supported camera/input navigation, object picking, transforms/materials and lifecycle through documented interfaces |
| Thin application adapter | Version/availability checks; translate domain commands to documented SDK operations; map returned object IDs; propagate errors. No renderer/camera math fallback. |
| Plate Studio domain | Plate configuration, jurisdiction/style metadata, legal research and provenance, project schemas, command/undo history and edit validation |
| Desktop editor shell | Toolbar, collapsible browser/inspector, shortcuts, selection UI, compact legal status and first-use New/Open actions |
| Persistence | Local-first projects, notes/settings and exports outside replaceable app; explicit schema migration copies and backups |
| Maintenance | Separate verified launch/update/repair runtime; no project/media writes during code repair |

Actual native versus browser/webview host, GPU backend, viewport embedding and
input mechanism remain decisions for the delivered SDK's supported contract. No
specific API surface or backend is assumed operational. App geometry/parameters
must use documented SDK mesh/asset facilities; no second rendering engine.

## Proposed professional UI layout

```
+-----------------------------------------------------------------------+
| Birthright | New/Open/Save | Undo/Redo | Select/Transform | View | Help |
+-------------+-------------------------------------------+-------------+
| Object      |                                           | Properties  |
| browser     |     LARGE TRUE ENGINE GPU VIEWPORT        | inspector   |
| collapsible |     real mesh, selection and navigation   | collapsible |
|             |                                           |             |
+-------------+-------------------------------------------+-------------+
| Selection / units / engine state | Legal status | Risk / source access |
+-----------------------------------------------------------------------+
```

This is a wireframe proposal, not a screenshot or implemented interface. There is
no oversized marketing introduction, hero typography or landing-page section.
Birthright identity is a compact wordmark/accent and consistent typography.
A new user reaches New/Open or a genuine SDK-rendered generic plate scene; if the
engine is unavailable, show an honest engine-unavailable state instead of a fake
interactive 3D viewport.

The viewport receives most available area. Side panels collapse independently;
width-constrained layouts retain a usable viewport and expose panels as docks or
flyouts. Keyboard access, visible focus, readable labels and status text must not
depend solely on color. Layout preferences belong in user settings, not app code.

Mouse navigation must control the SDK camera. Proposed defaults are middle-drag
orbit, Shift+middle-drag pan, wheel zoom/dolly and a frame-selection shortcut,
subject to SDK support and user approval. Provide accessible mouse/keyboard or
trackpad alternatives. Left-click selection uses SDK picking; transform tools and
numeric inspector edits operate through validated domain commands and SDK updates.
No CSS rotate/scale substitute or independently implemented camera engine.

Object browser and inspector share selection state. Edits preview responsively,
commit through undoable commands and persist only after valid application state
is confirmed. Engine failure must produce actionable status while retaining the
project; it must not silently discard edits or overwrite original project files.

Legal status occupies a compact status area with a source/details drawer. Keep
Legal/Illegal/Obscure/Unverified separate from five-level compliance risk; unknown
risk remains unassessed. Surface source, effective/review dates, interpretation
and unavailable evidence without guaranteeing legality. No identification-evasion
optimizer is permitted. Educational research is a dock/workspace, not a landing
page replacing the editing surface.

## Data and approval preservation

Current schemaVersion 1 contains name/state/text, one browser save slot and
separate notes. Preserve existing JSON exports and original browser data. Future
SDK scenes need an explicitly versioned application schema with the exact SDK
reference and documented units/coordinate/asset semantics. Migration must write
copies, retain original files and be tested before approval; no migration occurs
in this audit. Future geometry/camera state is not claimed present in current
exports. Local notes are currently not exported with projects.

Before implementation, review a UI specification and acceptance checklist after
the SDK proof: actual GPU/SDK trace, mouse orbit/pan/zoom, picking, reversible
object edits, resize/collapse behavior, save/reopen equivalence, project retention,
compact source-linked legal state and clear engine failure behavior. Prototype
packaging tests are not substitutes for those editor acceptance checks.
