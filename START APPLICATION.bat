@echo off
setlocal
cd /d "%~dp0"
call "%~dp0tools\run-python.bat" "%~dp0tools\launch.py" %*
if errorlevel 1 (
  echo Application did not start. Read the error above and README - FIRST TIME SETUP.txt.
  pause
  exit /b 1
)
