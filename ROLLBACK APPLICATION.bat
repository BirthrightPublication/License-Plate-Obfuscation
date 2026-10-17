@echo off
setlocal
cd /d "%~dp0"
call "%~dp0tools\run-python.bat" "%~dp0tools\updater.py" --root "%~dp0Installed" --rollback
if errorlevel 1 (
  echo Rollback was not applied. A previous installed version is required.
  pause
  exit /b 1
)
call "%~dp0START APPLICATION.bat"
