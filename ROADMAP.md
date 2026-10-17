# V0.1 integration restart — blocked on selected SDK capabilities

The owner explicitly authorized replacing the rejected interface around the real
True Engine renderer and repairing source/native launcher workflows. The selected
engine is published v0.1.2, SDK0.1, immutable commit
8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0. This updates the previous audit-only hold;
it does not approve the CSS prototype as the final editor.

## Current iteration

- Inspect the real public SDK and host example; record exact support and gaps.
- Maintain a separate Git-pinned SDK consumer test for CPU scene/camera/project
  behavior and actual engine-rendered pixels, independent of the application.
- Repair one primary Start and one primary Update with compatibility aliases;
  clearly distinguish installed native files from experimental source mode.
- Preserve every project, browser save/note/profile/origin, setting, source file,
  media file, existing script, prior binary and release. No user-drive mutation.
- Publish source work on a review branch. No integrated version/tag/package until
  the complete editor and actual Windows acceptance are verified.

## Hard SDK gaps

The existing renderer supports perspective primitives, transforms, opaque color,
orbit/pan/zoom, picking and resize. It lacks orthographic rendering and suitable
text/custom-mesh submission. Additional material properties are also unavailable.
See docs/TRUE-ENGINE-SDK-ASSESSMENT.md and the precise, issue-ready
request docs/TRUE-ENGINE-FEATURE-REQUEST.md. Do not edit True Engine or create a
local rendering/camera fallback. The SDK probe is not an integrated application.

## Next milestone: actual first working V0.1 studio

1. Obtain a tested, versioned True Engine SDK resolving the required APIs.
2. Pin that exact source; rerun external CPU/GPU compatibility on Linux/Windows.
3. Implement the professional editor using its supported host/geometry/material/
   camera APIs: compact toolbar, left objects/styles, large real viewport, right
   inspector, bottom status/legal area, collapsible docks and minimal scrolling.
4. Implement plate text, dimensions, color/material properties actually supported,
   rotation, orbit/pan/zoom, perspective/orthographic, responsive resize, selection,
   local-first save/reopen and explicit data-preserving legacy import.
5. Validate Windows11 package, real mouse/editor behavior, save/reopen, native and
   source launcher diagnostics, updater download/hash/install/failure rollback,
   project/settings/media preservation and compatibility manifests.
6. Review/merge approved source and only then tag/publish the integrated release
   with complete runnable ZIP, SHA-256, evidence, limitations and install notes.

The original long-term roadmap in docs/MASTER-DEVELOPMENT-ROADMAP.md remains
preserved. Later style/catalog/legal/provider/simulation/vehicle/membership phases
must not automatically begin while this first studio milestone is incomplete.
Legal remains Unverified, regulatory risk unassessed, availability unavailable.
