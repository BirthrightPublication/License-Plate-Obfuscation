@echo off
setlocal
cd /d "%~dp0"
if exist "%~dp0app\PlateStudio.exe" goto native
if exist "%~dp0tools\windows_entry.py" goto source
goto missing
:native
"%~dp0app\PlateStudio.exe" %*
set "PLATE_EXIT_CODE=%errorlevel%"
goto finish
:source
call "%~dp0tools\run-python.bat" "%~dp0tools\windows_entry.py" --root "%~dp0." start -- %*
set "PLATE_EXIT_CODE=%errorlevel%"
goto finish
:missing
echo No complete native application was found at "%~dp0app\PlateStudio.exe".
echo A GitHub source archive is not an installation. Keep your projects and obtain the complete Windows installation ZIP.
echo Update Plate.bat can recover only when an installed updater is available.
set "PLATE_EXIT_CODE=1"
:finish
if "%PLATE_EXIT_CODE%"=="0" exit /b 0
if "%~1"=="--check" exit /b %PLATE_EXIT_CODE%
if not defined PLATE_NO_PAUSE pause
exit /b %PLATE_EXIT_CODE%
