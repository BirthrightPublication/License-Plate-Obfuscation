@echo off
setlocal
cd /d "%~dp0"
set "PLATE_UPDATER=%~dp0app\PlateUpdater.exe"
if not exist "%PLATE_UPDATER%" set "PLATE_UPDATER=%~dp0.plate-studio\recovery-updater.exe"
if not exist "%PLATE_UPDATER%" (
  echo No recovery updater exists. Existing files have been left untouched.
  pause
  exit /b 1
)
"%PLATE_UPDATER%" --bootstrap --rollback --root "%~dp0."
if errorlevel 1 pause
