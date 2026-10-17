@echo off
cd /d "%~dp0"
py -3 updater.py --rollback --launch
if errorlevel 1 pause
