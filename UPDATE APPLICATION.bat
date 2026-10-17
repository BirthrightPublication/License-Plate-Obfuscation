@echo off
setlocal
cd /d "%~dp0"
echo Close any running Studio console before updating. Export a project backup first.
call "%~dp0tools\run-python.bat" "%~dp0tools\updater.py" --build-dir "%~dp0Build" --root "%~dp0Installed"
if errorlevel 1 (
  echo Update was not applied. Existing versions and projects are preserved. Read the error above.
  pause
  exit /b 1
)
call "%~dp0START APPLICATION.bat"
