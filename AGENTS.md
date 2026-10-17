# License Plate Obfuscation Studio

## Authoritative repository and Git workflow

The authoritative repository for this conversation is https://github.com/BirthrightPublication/License-Plate-Obfuscation, with stable branch `main`. FORGE and True Engine are separate projects. Read docs/GITHUB-REPOSITORY-RULES.md before development or release work.

Before each update, inspect status/branch/remotes and fetch origin; compare with origin/main and inspect the implementation. Preserve unrelated and uncommitted work. Develop on a dedicated feature branch, make meaningful commits, run applicable tests and document architectural decisions. Push the branch and open a PR where supported; merge approved changes without force-pushing stable history. Confirm remote refs before reporting success. Never claim an API operation, push, merge or asset upload succeeded without evidence.

Preserve completed version history and tags. docs/releases/history.json associates release filenames/checksums with exact tagged source commits. Publish ZIPs as release assets rather than committing build binaries. Keep local release ZIPs in Build; never overwrite older packages or replace newer source with an older ZIP. GitHub API restrictions must be reported separately from native Git access. Do not begin new editor features while Windows V0.1 test feedback remains outstanding.

This repository is independent of True Engine. Never edit the engine repository. Use only documented, explicitly versioned SDK interfaces; do not invent SDK APIs. No future phase without user approval.

v0.1.0 is an educational foundation, not a production road-plate design or legal service. Never optimize physical plate configurations to evade identification. Never infer legality, availability, or low risk from missing data. Keep verified evidence, interpretation, and unavailable information distinct. Legal classifications and five-level risk assessments are independent.

Use the existing checkout; cloud tasks are isolated. Do not create worktrees unless requested. Run `npm test` for changes and the browser smoke test when changing UI. Preserve projects/settings across updates. Never write secret values into source or logs. Document actual tests, compatibility, changed files and checksums for each release. Package into Build locally; Windows deployment target is B:\License Plate Obfuscation Studio\Build.

## Permanent project directives

Read docs/PERMANENT-DEVELOPMENT-DIRECTIVE.md and docs/MASTER-DEVELOPMENT-ROADMAP.md. Read NEXT_ITERATION.md before any new iteration, reconcile actual state, and perform only one authorized iteration. Maintain ROADMAP.md, ARCHITECTURE.md, KNOWN_ISSUES.md, TEST_REPORT.md, RELEASE_MANIFEST.json and NEXT_ITERATION.md. Tag actual releases; keep full ZIPs in this project's Build directory and preserve earlier outputs. Keep user data outside replaceable code directories. No engine modifications.

Current release 0.1.1 fixes V0.1 Windows distribution only. V0.1 is not complete against the master roadmap. Do not begin V0.2 until existing V0.1 is tested and the user authorizes advancement. No native Windows build or Windows batch execution has been validated in Linux; do not claim otherwise.
