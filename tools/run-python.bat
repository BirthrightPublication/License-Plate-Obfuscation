@echo off
py -3 -c "import sys; assert sys.version_info >= (3,12)" >nul 2>&1
if errorlevel 1 goto try_python
py -3 %*
exit /b %errorlevel%
:try_python
python -c "import sys; assert sys.version_info >= (3,12)" >nul 2>&1
if errorlevel 1 goto missing
python %*
exit /b %errorlevel%
:missing
echo Python 3.12 or newer is required. Run INSTALL DEPENDENCIES.bat first.
exit /b 1
