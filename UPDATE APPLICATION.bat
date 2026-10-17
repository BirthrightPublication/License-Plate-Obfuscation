@echo off
setlocal
call "%~dp0Update Plate.bat" %*
exit /b %errorlevel%
