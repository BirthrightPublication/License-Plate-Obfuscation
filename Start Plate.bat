@echo off
setlocal
cd /d "%~dp0"
if not exist "%~dp0app\PlateStudio.exe" (
  echo Application files are missing. Run Update Plate.bat to recover an interrupted update.
  pause
  exit /b 1
)
"%~dp0app\PlateStudio.exe" %*
if errorlevel 1 (
  echo Studio did not start. Close an earlier Studio console if port 4173 is occupied.
  pause
  exit /b 1
)
