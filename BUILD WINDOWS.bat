@echo off
setlocal
cd /d "%~dp0"
call "%~dp0tools\run-python.bat" "%~dp0tools\build_windows.py"
if errorlevel 1 (
  echo Build failed. Earlier releases and user data have not been removed.
  pause
  exit /b 1
)
echo Build completed. See the new timestamped Native build folder inside Build.
pause
