@echo off
setlocal
cd /d "%~dp0"
call "%~dp0tools\run-python.bat" -c "import sys; print('Python prerequisite already satisfied:', sys.version.split()[0])"
if not errorlevel 1 goto done
where winget >nul 2>&1
if errorlevel 1 goto manual
echo Installing Python 3.12 using Windows Package Manager. No app files or user data will be removed.
winget install --id Python.Python.3.12 --exact --source winget --scope user --accept-source-agreements --accept-package-agreements
if errorlevel 1 goto manual
echo Close this window, then double-click START APPLICATION.bat.
pause
exit /b 0
:manual
echo Automatic installation was unavailable. Install Python 3.12 or newer from https://www.python.org/downloads/windows/
echo Include the Python launcher during installation. Then run START APPLICATION.bat.
pause
exit /b 1
:done
echo Ready. A current Microsoft Edge, Chrome or Firefox browser is also required.
pause
