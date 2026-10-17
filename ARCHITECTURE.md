# Architecture

Independent browser application; index.html and src/* use standard ES modules and CSS transforms. No external application libraries, backend database, account service, analytics or True Engine private interfaces. The neutral plate is an HTML element, not an engine model.

Local project schemaVersion 1: name, state, text. One browser localStorage slot (`birthright.plate.project.v1`); notes use `birthright.plate.notes.v1`. JSON exports contain only project fields. Updates do not migrate these schemas. Browser origin/profile must remain stable.

Python tools/launch.py verifies packaged asset hashes, binds only 127.0.0.1:4173, serves an explicit four-file allowlist with ES module MIME types, and opens localhost in the default browser. Personal files, sources and settings are not exposed through the host. The Python process must stay running. All app functionality runs in the browser; Python is only a local file host.

Full-release ZIPs include complete runnable assets, source/tests/docs and Python tools; no native binary is implied. A separate Windows-only script can freeze the host and its assets using PyInstaller. The resulting EXE still uses an external browser. No cross-compilation or engine integration occurs.

Managed updater stages and verifies full releases, retains version slots and atomically switches a current/previous pointer under Installed. It refuses existing slots and patch packages. Hashes detect corruption, not malicious publisher changes; signed distribution remains a later milestone. Failed pre-activation checks leave the active pointer intact. Runtime failure recovery is manual rollback.

## 0.1.2 Windows distribution decision

The current update system uses two PyInstaller onefile EXEs (studio host and separate updater), a versioned managed app manifest, external updater runners and journaled app-directory swaps. This avoids requiring end-user Python while keeping the existing browser UI, data schema and origin. Only app is replaceable; every root data/config/media path is preserved. tools/updater.py remains as a legacy-only full-package updater for historical workflows; new installations use tools/github_updater.py and the standardized ZIP. See docs/WINDOWS-RELEASE-UPDATES.md for protocol, failure recovery and test/publication boundaries.
