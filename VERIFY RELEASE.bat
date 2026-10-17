@echo off
setlocal
cd /d "%~dp0"
call "%~dp0tools\run-python.bat" "%~dp0tools\verify_release.py"
if errorlevel 1 (
  pause
  exit /b 1
)
pause
