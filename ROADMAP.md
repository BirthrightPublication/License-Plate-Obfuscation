# Development hold — experimental V0.1.2

**New features, visual implementation and feature-version advancement are paused.**
The present build is an experimental browser prototype. The current interface is
not approved as the final design. True Engine is the permanent 3D foundation; no
competing engine or CSS-as-engine substitution is authorized.

The original user roadmap remains preserved in docs/MASTER-DEVELOPMENT-ROADMAP.md.
This hold takes precedence over its next milestones and the general Continue
workflow. No next feature version is scheduled or implicitly authorized.

## Actual state

| Area | Evidence-backed status |
| --- | --- |
| Release identity | v0.1.2 source/tag/package preserved; packaging history is not UI approval |
| True Engine | No selected SDK package/version/commit, adapter or compatibility test |
| Viewport | HTML/CSS perspective prototype, not a True Engine GPU viewport |
| Input/editing | Text/state preview and an Orbit slider; no real 3D mouse navigation, pan/zoom or object-editing system |
| Interface | Landing-page intro with light panels; user rejected final-design direction |
| Projects | One browser save slot and JSON import/export; separate notes; no native scene schema |
| Installation | Source/Python, legacy Installed and native app launcher contracts coexist and are confusing; screenshot has source layout with no visible app folder |
| Windows package | Published ZIP includes x64 app/runtime/updater; verified hash/manifest/PE now; not automatically installed by a source checkout or BUILD WINDOWS |
| Maintenance | Full-package native updater/backups exist; no dedicated repair utility or patch application implementation |
| Legal/research | Prototype source links only; legal status Unverified, risk unassessed, availability unavailable |

## This iteration — documentation/audit only

- Trace scripts and verify source/release layout: docs/INSTALLATION-AUDIT.md.
- Propose one launcher, one updater, one repair utility and a safe plan:
  docs/INSTALLATION-REPAIR-PLAN.md.
- Record SDK gates and professional editor architecture:
  docs/TRUE-ENGINE-UI-ARCHITECTURE.md.
- Keep all scripts, source, binaries, releases, projects/settings and versions intact.
- No build, installation, repair, migration, new UI, SDK integration, patch or tag.

## Gates for later authorized work

1. Confirm exact Windows installation paths; approve a concrete preservation and
   repair/replacement plan before any installation mutation. Repair approval does
   not approve an interface redesign or feature-version advancement.
2. Await explicit approval to restart True Engine work in its own repository and
   delivery of a tested, documented versioned SDK; do not invent its capabilities.
3. Prove engine operation through supported interfaces in an explicitly authorized
   integration task. Preserve current projects and record exact compatibility.
4. Obtain explicit approval to resume Plate Studio and implement the professional
   editor architecture after engine operation is established.
5. Reassess V0.1 acceptance before discussing V0.2. Never automatically advance
   later design/legal/simulation/vehicle/membership milestones from this audit.
