# License Plate Obfuscation Studio · v0.1.0

Birthright membership product foundation. This release is an independent, local-first educational browser application. True Engine integration is blocked until a versioned SDK and its documented contract are supplied. No engine APIs or engine files have been modified. Membership authentication is not implemented.

## Run and test

Requires Python 3.12+; Node 24 for automated tests. No application dependencies or installation step.

```
cd /workspace/License-Plate-Obfuscation
npm start
npm test
```

The server runs on port 4173. Use a consistent origin (`http://localhost:4173` on a local workstation) because browser storage is scoped to origin and browser profile. The cloud UI has no supported web preview. Browser automation: Playwright 1.62.1 is supplied by this cloud runtime; run `CHROMIUM_PATH=/usr/bin/chromium node tools/smoke.cjs` with the server running. For another machine, install that Playwright version outside the checkout and set NODE_PATH and CHROMIUM_PATH appropriately. Chromium downloads require cdn.playwright.dev; this environment's policy blocks that domain, so the installed system Chromium is used instead.

## First use and supported scope

Choose one of 50 US states, edit illustrative preview text, orbit the CSS 3D plate, then save on this device. There is one saved project slot; use JSON export/import for additional projects and backups. Research notes are stored separately in browser localStorage, not included in project exports. A denied storage permission produces an error message. Clearing browser data removes local projects and notes. No plate data is sent to a provider.

California, Texas and New York have curated links to official catalogs and statutes. These are research leads, not a complete official style catalog or currently verified legal evidence. The neutral preview is not official plate artwork. Validation covers preview syntax only, not jurisdiction-specific registration eligibility. All legal assessments remain Unverified; risk is unassessed. Availability returns unavailable because there is no authorized provider integration. No scraping, fabricated responses, or legal certainty claims.

Legal, Illegal, Obscure and Unverified are defined in the UI. Risk is independent: 1 Minimal, 2 Low, 3 Moderate, 4 High, 5 Critical; unknown is not a sixth level and is never scored as minimal. Verified records will require specific scope, current source text, review date and interpretation. Vehicle-model support is reserved in the compatibility manifest but unavailable.

## Release and updater

Run `npm run release`. Build contains the full ZIP, release.json (every packaged file and SHA-256), and SHA256SUMS.txt (ZIP checksum). Initial release has no prior base, so no patch is manufactured. Future patches require approval, an exact base version and validation.

This Linux cloud cannot write a Windows B: drive. Copy the repository release bundle to `B:\License Plate Obfuscation Studio`; ZIPs belong in its `Build` subfolder. With Python 3.12+ installed on Windows, double-click `tools\Update.cmd` to verify, install and launch. Close any existing server before updating. Double-click `tools\Rollback.cmd` to activate the previous installed version and launch. Initial installation has no rollback target. Windows launchers have not been run in this Linux environment.

Updater installs immutable version slots under Installed, verifies manifest hashes, rejects unsafe ZIP paths, and atomically replaces a current-version pointer. It refuses to overwrite existing versions. No user project/settings paths are removed. It preserves browser data by keeping the same localhost port/origin; use the same browser profile. Back up browser projects before updates. Rollback tests exercise two synthetic versions; there is only one product release today. Hashes detect corruption, not publisher identity: accept release archives only from a trusted distribution channel and compare the published ZIP checksum independently. Interrupted copies can leave an unused version directory but do not switch the active pointer.

## Remaining prerequisites

Supply the True Engine SDK package/repository, exact version and supported host/platform contract. Provide authorized availability-provider terms and credentials through secure environment settings, not chat. A complete official catalog, jurisdiction-specific rule datasets and reviewed legal evidence remain future approved work. Do not deploy this foundation as a completed engine-powered product.
