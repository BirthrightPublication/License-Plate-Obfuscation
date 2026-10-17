# True Engine integration gate and proposed editor architecture

**Editor architecture target; not implemented in the application.**

Update: the owner authorized integration restart and selected published Engine
v0.1.2/SDK0.1. The separate consumer probe exercises real rendering; it is not an
app adapter or editor. See TRUE-ENGINE-SDK-ASSESSMENT.md for the selected public
contract and hard text/orthographic gaps. Those current facts supersede historical
audit-only approval/SDK-absence language below. No competing renderer is permitted.

## Permanent engine boundary

True Engine is the permanent 3D foundation and lives in its own repository:
https://github.com/BirthrightPublication/True-Engine. Plate Studio must consume a
tested, versioned SDK, not copy its source, modify the engine repository or build
a competing renderer. CSS transforms must never be described as engine integration.

Current evidence: the owner selected published True Engine v0.1.2, SDK0.1,
commit8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0. The compatibility manifest records
that selection and explicitly states the production application does not render
through True Engine. The separate Rust consumer has passed4CPU+1offscreen pixel
checks locally on Linux Mesa llvmpipe/GL and in Ubuntu/Vulkan and Windows/DX12 CI with software adapters. This is programmatic software-renderer evidence,
not a Windows interactive editor or application integration test.

See TRUE-ENGINE-SDK-ASSESSMENT.md: the supported Rust host owns device/surface and
calls public Renderer APIs. Orthographic projection and suitable text/custom-mesh
submission are missing. The CSS application remains unchanged and unapproved.

## Remaining gates before production redesign

1. Owner restart approval and exact SDK selection have been received. No new
   general restart approval is needed to continue this authorized integration
   iteration. No True Engine source modifications are authorized in this repo.
2. Engine maintainers must deliver the missing supported APIs in a tested,
   versioned SDK. TRUE-ENGINE-FEATURE-REQUEST.md gives the exact requests; do not
   invent a future minimum version or duplicate engine implementation locally.
3. Pin the compatible SDK commit, update the compatibility manifest and lockfile,
   and rerun external CPU/GPU tests. Validate actual native Windows rendering and
   failure handling; software Linux pixels do not qualify user hardware.
4. Implement the professional editor through supported engine APIs: actual GPU
   plate geometry/text, materials, orbit/pan/zoom, perspective/orthographic,
   picking/property editing, responsive resize and data-preserving save/reopen.
   No fake CSS viewport or renderer/camera fallback may satisfy acceptance.
5. Validate the complete editor and full installation/update/recovery package on
   Windows before publishing a new integrated version/tag. Preserve the existing
   prototype release, source history and all projects/settings/media.

SDK changes require exact dependency updates, compatibility evidence, application
regression tests and release notes. Any needed engine code change belongs to a
separate authorized engine task, never this application's working tree. Later
roadmap phases still require approval after the first working studio is verified.

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
