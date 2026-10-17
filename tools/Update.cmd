@echo off
cd /d "%~dp0"
py -3 updater.py "..\Build\License-Plate-Obfuscation-Studio-0.1.0.zip" --launch
if errorlevel 1 pause
