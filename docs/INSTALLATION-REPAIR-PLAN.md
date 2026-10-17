# Proposed clean installation and safe repair plan

**DESIGN ONLY. No repair, migration, script retirement, patch or replacement
utility is implemented/authorized by this document. V0.1.2 remains frozen.**

## Proposed FORGE-style separation

```
B:\License Plate Studio\
  Start Plate.bat                  # ONE primary end-user launcher
  Update Plate.bat                 # ONE update launcher
  Repair Plate.bat                 # ONE future utility: inspect / repair / rollback
  app\                            # replaceable, versioned code/runtime only
    manifest.json
    ...tested application/maintenance runtime...
  .plate-studio\
    bootstrap\                    # verified maintenance runtime independent of app
    backups\                      # retained previous code + backup manifests
    journals\                     # update/repair transactions
    logs\
    staging\
  Build\
    Source\                       # Git source, tests, developer launch/build scripts
    Releases\                     # original full ZIPs + exact checksum sidecars
    Patches\                      # versioned patches + manifests/checksums
  UserData\                       # proposed home for NEW persistent state only
    Projects\
    Settings\
    Presets\
    History\
  ...all existing media/output/config/project folders stay where they are...
```

This is a target, not the current ZIP layout. Existing Build downloads at the
root of Build, existing root data folders, browser storage and legacy Installed
slots must not be relocated by inference. A UserData folder is not a migration.
No automatic move from existing paths or browser localStorage is approved.
Developer files move under Build/Source only AFTER explicit migration approval
and replacement-launcher tests; all old scripts remain in place for now.

The maintenance bootstrap must be verifiable and executable even if app is absent.
Initial bootstrap must come from an independently verified complete installer;
copying an updater only after a successful app launch is not enough for first
repair of a source-only folder. Define one shared manifest/protocol and one
launcher mode check; do not silently switch between legacy Installed slots and
native app. Existing root/custom launchers must not be overwritten without a
reviewed replacement list and confirmation.

One repair utility should offer read-only diagnosis by default, verify-only,
restore-known-release and rollback modes. It must show paths, current/target
versions, protected data, backup location and exact mutations before requesting
approval. It is not the same as today's update: v0.1.2 explicitly refuses same-
version reinstall and is not a repair tool. Rollback selection belongs in repair
rather than multiplying normal-root batch files. No Repair Plate.bat exists yet.

## Safe sequence for THIS reported installation

1. Freeze new features/releases. Identify the full folder shown in the screenshot
   and distinguish source root, any complete native install and any nested app.
   List only installation/manifest paths; no private files or credentials are
   needed. The screenshot alone does not expose the address bar or Build contents.
2. Preserve the working prototype. Use its existing Export backup for the single
   project slot and separately copy research notes, which project export omits.
   Keep the same browser profile and localhost:4173 origin. Do not clear site
   storage, copy credential-bearing browser profiles, reinstall Python or move
   user folders as a diagnostic shortcut.
3. Inventory existing app/Installed/.plate-studio state, original ZIPs and exact
   version-matched checksum files. Preserve unknown source files, local edits and
   custom tools. No legacy/native state conversion is assumed.
4. If a full native prototype is wanted solely for installation validation,
   verify its original 0.1.2 ZIP and manifest. Prepare a reviewable fresh staging
   location OUTSIDE current source/app/data. The expected app/EXEs are known from
   the audit. This would still be the rejected-interface prototype, not a new UI.
5. Present the complete source/destination mapping and verified backup manifest,
   then obtain confirmation BEFORE creating an installation, extracting into an
   installation folder, moving scripts, modifying app, invoking Update/Rollback,
   applying a patch or migrating anything. Backups should include old code and
   affected launcher/configuration files; personal data remains untouched and
   separately protected. Check backup hashes and restore feasibility first.
6. Only after confirmation, stage the approved code, validate inventory and EXE
   architecture, verify hashes and native runtime, then activate transactionally.
   Validate the launcher from the exact intended B: path. Restore automatically
   if activation/validation fails. Keep failed candidates and recovery evidence.
7. Verify saved projects, notes, settings and original/processed media byte-for-
   byte or with a before/after inventory as appropriate. Retain backup versions.
   Do not claim successful repair from a running source launcher alone.

**None of steps 4–7 was executed.** No installer/updater/repair/build was run.
No need to run BUILD WINDOWS.bat to repair this layout has been established; a
verified native artifact already exists independently of the source root.

## Read-only Windows inventory for confirmation (not executed here)

Replace the path with the exact folder shown in Explorer. This reports path
existence only; it does not install, download, extract, delete or read project data.

```powershell
$plateAuditRoot = 'B:\License Plate Studio'
'Full folder: ' + $plateAuditRoot
@(
  'START APPLICATION.bat', 'Start Plate.bat', 'Update Plate.bat',
  'app', 'app\PlateStudio.exe', 'app\PlateUpdater.exe', 'app\manifest.json',
  '.plate-studio\recovery-updater.exe', 'Installed\current.json',
  'tools\launch.py', 'release.json', 'true-engine.compatibility.json'
) | ForEach-Object {
  [pscustomobject]@{
    RelativePath = $_
    Exists = Test-Path -LiteralPath (Join-Path $plateAuditRoot $_)
  }
}
```

## Future build/patch/recovery acceptance (after restart approval)

- Lock exact Windows image/toolchain, x64 Python, PyInstaller/transitive dependency
  versions and hashes; later lock the designated True Engine SDK release/commit.
  Record exact source SHA, toolchain and tests. Distinguish repeatable procedures
  from bit-identical output. Preserve historical full packages and tags.
- Versioned patch name proposal:
  `License-Plate-Studio-v<TARGET>-from-v<BASE>-windows-x64.patch.zip` plus `.sha256`.
  Manifest must include exact base version/source and complete required base-code
  hashes, target manifest, changed/new/deleted MANAGED code paths and hashes.
  Reject mismatched bases and any path outside managed code. No patch is produced
  now; both current updater families support FULL packages only and refuse patches.
- Validate path traversal, reparse points, duplicate/case-colliding names, malformed
  manifests, SHA failure, wrong architecture/SDK, locked files, power-loss gaps,
  missing/corrupt backups and recovery with missing app. Use isolated fixtures,
  never destructive tests on the real installation.
- Use a journal and verified same-volume staging/backup. Test rollback before
  retirement of old launchers. Keep recovery runtime outside replaceable app.
  Do not delete backups after a failed or merely partially verified install.
- Protected state: ALL paths outside managed app, including Projects, UserData,
  settings/preferences/history, presets/templates, original and processed media,
  output/export folders, custom configurations/tools, Build source/archives and
  external/browser data. Unknown data inside app triggers refusal and a reviewable
  preservation plan. Never silently delete or move it to make repair pass.
