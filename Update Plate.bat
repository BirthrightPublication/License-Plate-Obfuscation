@echo off
setlocal
cd /d "%~dp0"
set "PLATE_UPDATER=%~dp0app\PlateUpdater.exe"
if not exist "%PLATE_UPDATER%" set "PLATE_UPDATER=%~dp0.plate-studio\recovery-updater.exe"
if not exist "%PLATE_UPDATER%" (
  echo No installed updater found. Extract the complete installation ZIP into a NEW folder first.
  pause
  exit /b 1
)
"%PLATE_UPDATER%" --bootstrap --root "%~dp0."
if errorlevel 1 (
  echo The updater could not start. Previous application files were not removed.
  pause
  exit /b 1
)
