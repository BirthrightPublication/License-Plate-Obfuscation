# Permanent GitHub repository and release management

This project's authoritative source of truth is https://github.com/BirthrightPublication/License-Plate-Obfuscation (stable branch main). FORGE uses BirthrightPublication/forge; True Engine uses BirthrightPublication/True-Engine. Never push this application to either of those repositories.

## Before development

1. Inspect repository identity, workspace status, branch, origin and history. Fetch origin and compare the selected source with the remote. The configured fetch refspec must include remote branches, not only HEAD.
2. Read AGENTS.md, NEXT_ITERATION.md, relevant implementation, roadmap, manifest, changelog and test evidence. Preserve uncommitted/unrelated work. Do not restore an older ZIP over newer working source.
3. Use a dedicated feature branch based on the appropriate current source. Never use force push to overwrite stable history. Existing cloud checkouts are isolated; do not create worktrees without a request.

## During and after development

- Make meaningful commits, preserve working functionality, run applicable tests and record significant architectural decisions.
- Push commits to the correct origin. Open a PR for review where API/tools support it; merge approved changes into main. Do not bypass branch protection or claim approval without evidence.
- Initial empty-repository setup is expressly authorized to push the verified source to main. The initial preservation task may fast-forward its repository-governance documentation into main without a PR when API access is unavailable. This does not waive review for future feature work.
- Confirm remote refs and expected commit SHAs after every push/merge. Report the exact blocker for access, Git permission, API or source failures. Never claim an unsuccessful operation worked.
- Tag every completed release and preserve existing version history. Do not move a published tag or rewrite previous release records. A documentation-only change after a tag does not create a new application release.
- Associate each tested package with its exact source tag/commit, SHA-256, filename, manifest, changed-file list, tests and limitations. Put full ZIPs and patches in this project's Build directory locally, and use GitHub Release assets for remote package distribution when available. Do not commit binary builds, credentials, databases, private files or dependency/build caches as source.
- Full source and reproduction scripts must be preserved in GitHub rather than relying only on chat or a temporary workspace. Keep each release's history and patches. Patches must check exact base version/file hashes; currently this application's updater accepts full releases only and rejects patches.
- Never report a package was uploaded to GitHub when only its source or checksum was pushed. Record remote asset availability separately.

## Cross-repository integration

True Engine is an independent reusable engine. Depend only on an explicitly versioned release or commit and record/test compatibility. The selected SDK is true-engine0.1.2, contract0.1, commit8d751dbe76ca1dfd02c826e60ec68dda7e7d51b0. Application integration remains blocked by the documented missing orthographic/text submission APIs. Do not duplicate or silently alter engine code in this repository. Any engine changes require their own authorized task/commits in the engine repository and tests against affected applications.

## Release completion report

Report repository name/URL, source branch and final SHA, actual push confirmation, PR/merge status where applicable, version tag, package filename, tests, update instructions and unresolved issues. Distinguish tagged application source from later documentation commits and Windows-targeted packages from actual Windows-tested executables.
