# v0.1.0 validation report

Validated in Linux cloud on 2026-10-16 (America/Los_Angeles).

- Node v24.19.0: 5 domain tests passed, 0 failed, 0 skipped.
- Python 3.12.14: 3 updater tests passed, 0 failed. Includes synthetic two-version rollback and preservation, corrupted/path-traversal rejection, existing-version protection.
- Playwright 1.62.1 with system Chromium: browser workflow passed. Exercised state/text editing, save/reload/load, unavailable availability response, orbit control, research-note persistence, 390px layout and absence of script errors.
- HTTP service started successfully on port 4173. Required browser checks used real loaded ES modules and localStorage.
- True Engine versions tested: none; SDK missing. Compatibility manifest intentionally has no SDK version.
- Windows .cmd launchers: unrun. B: deployment: unavailable on Linux.
- Official source currency, law interpretation, style artwork and jurisdiction-specific eligibility: unverified; no authoritative availability integration configured.

Build/release.json is the complete packaged file list with per-file checksums and initial-release changed-file inventory. Build/SHA256SUMS.txt records the ZIP checksum. This file is included in the ZIP. There is no prior release for a patch. Browser automation requires externally supplied Playwright/Chromium as described in README; the product itself has no runtime npm dependencies.
