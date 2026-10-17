# License Plate Obfuscation Studio

## ACTIVE ITERATION — authorized SDK integration restart

The owner explicitly restarted Plate Studio engine/interface development and launcher/update repair, selecting the published True Engine v0.1.2 SDK. This supersedes the prior audit-only hold within this iteration. The rejected landing-page/CSS interface remains an experimental prototype, never the approved final editor. Do not implement a competing renderer, invent SDK APIs, modify the engine repository, or publish an integrated release until real application rendering and Windows acceptance pass.

Read docs/TRUE-ENGINE-SDK-ASSESSMENT.md and docs/TRUE-ENGINE-FEATURE-REQUEST.md. Selected dependency is true-engine0.1.2, SDK contract0.1, exact commit8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0. Public APIs support perspective primitives, orbit/pan/zoom, picking and color, but not orthographic rendering or suitable plate text/custom-mesh submission. The separate integration/true-engine-sdk-probe tests the supported subset; it does not integrate the production application. Record actual CPU/GPU/Windows outcomes separately. Missing APIs are engine feature requests, never app-side renderer workarounds.

Repository launcher repair/testing is authorized. Do not delete old scripts; aliases must retain arguments and exit codes. Never silently convert a source checkout to an installation, migrate projects or change browser origin/profile. Before mutations to an existing Windows installation, confirm exact paths and concrete verified backup/recovery plan. No B: drive is accessible here. Preserve all data and prior releases. Package version stays0.1.2 until an actual tested release is ready; no integrated tag/package is authorized while the required SDK capabilities are absent.

## Authoritative repository and Git workflow

The authoritative repository for this conversation is https://github.com/BirthrightPublication/License-Plate-Obfuscation, with stable branch `main`. FORGE and True Engine are separate projects. Read docs/GITHUB-REPOSITORY-RULES.md before development or release work.

Before each update, inspect status/branch/remotes and fetch origin; compare with origin/main and inspect the implementation. Preserve unrelated and uncommitted work. Develop on a dedicated feature branch, make meaningful commits, run applicable tests and document architectural decisions. Push the branch and open a PR where supported; merge approved changes without force-pushing stable history. Confirm remote refs before reporting success. Never claim an API operation, push, merge or asset upload succeeded without evidence.

Preserve completed version history and tags. docs/releases/history.json associates release filenames/checksums with exact tagged source commits. Publish ZIPs as release assets rather than committing build binaries. Keep local release ZIPs in Build; never overwrite older packages or replace newer source with an older ZIP. GitHub API restrictions must be reported separately from native Git access. The explicit integration restart authorizes this iteration; later phases still require approval.

This repository is independent of True Engine. Never edit the engine repository. Use only documented, explicitly versioned SDK interfaces; do not invent SDK APIs. No future phase without user approval.

v0.1.0 is an educational foundation, not a production road-plate design or legal service. Never optimize physical plate configurations to evade identification. Never infer legality, availability, or low risk from missing data. Keep verified evidence, interpretation, and unavailable information distinct. Legal classifications and five-level risk assessments are independent.

Use the existing checkout; cloud tasks are isolated. Do not create worktrees unless requested. Run `npm test` for changes and the browser smoke test when changing UI. Preserve projects/settings across updates. Never write secret values into source or logs. Document actual tests, compatibility, changed files and checksums for each release. Package into Build locally; Windows deployment target is B:\License Plate Studio\Build.

## Permanent project directives

Read docs/PERMANENT-DEVELOPMENT-DIRECTIVE.md and docs/MASTER-DEVELOPMENT-ROADMAP.md. Read NEXT_ITERATION.md before any new iteration, reconcile actual state, and perform only one authorized iteration. Maintain ROADMAP.md, ARCHITECTURE.md, KNOWN_ISSUES.md, TEST_REPORT.md, RELEASE_MANIFEST.json and NEXT_ITERATION.md. Tag actual releases; keep full ZIPs in this project's Build directory and preserve earlier outputs. Keep user data outside replaceable code directories. No engine modifications.

Historical release 0.1.1 fixed V0.1 Windows distribution only. V0.1 is not complete against the master roadmap. Do not begin V0.2 until existing V0.1 is tested and the user authorizes advancement. Linux checks alone cannot validate Windows; actual Windows/native/batch/browser checks for 0.1.2 are recorded in docs/releases.

## Historical completed release/update iteration

Current completed release is 0.1.2: standardized Windows-x64 GitHub assets and transactional one-click updater only. Read docs/WINDOWS-RELEASE-UPDATES.md. Installation root is B:\License Plate Studio; Build is reserved for source/build/downloads. Only managed app/ is replaceable, and only with exact manifest inventory/hashes. Preserve EVERY other path, all root user files and browser data. Unknown/changed app files cause refusal. Retain backups; do not delete projects/media or old packages. The latest user-approved integration restart supersedes the historical editor hold, subject to the SDK blockers above. Tag/publish stable only after actual Windows runner tests pass; never treat source archives as installers.
