@echo off
setlocal
cd /d "%~dp0"
set "PLATE_UPDATER=%~dp0app\PlateUpdater.exe"
if not exist "%PLATE_UPDATER%" set "PLATE_UPDATER=%~dp0.plate-studio\recovery-updater.exe"
if exist "%PLATE_UPDATER%" goto native
if exist "%~dp0tools\windows_entry.py" goto source
goto missing
:native
if "%~1"=="--check" goto check
if not "%~1"=="" goto arguments
"%PLATE_UPDATER%" --bootstrap --root "%~dp0."
set "PLATE_EXIT_CODE=%errorlevel%"
goto finish
:source
call "%~dp0tools\run-python.bat" "%~dp0tools\windows_entry.py" --root "%~dp0." update -- %*
set "PLATE_EXIT_CODE=%errorlevel%"
goto finish
:check
if not "%~2"=="" goto arguments
"%PLATE_UPDATER%" --check
exit /b %errorlevel%
:arguments
echo Update Plate.bat accepts only --check or no arguments. Use Rollback Plate.bat for rollback.
set "PLATE_EXIT_CODE=2"
goto finish
:missing
echo No installed updater or source updater is available in this folder.
echo Preserve existing files. Extract the complete Windows installation ZIP into a NEW folder first.
set "PLATE_EXIT_CODE=1"
:finish
if "%PLATE_EXIT_CODE%"=="0" exit /b 0
if "%~1"=="--check" exit /b %PLATE_EXIT_CODE%
if not defined PLATE_NO_PAUSE pause
exit /b %PLATE_EXIT_CODE%
