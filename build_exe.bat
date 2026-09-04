@echo off
REM ============================================================
REM  Build a single standalone PythonTutor.exe for Windows.
REM  The .exe runs on PCs that do NOT have Python installed.
REM
REM  Run this once on any machine that HAS Python:
REM      double-click build_exe.bat    (or run it from a cmd window)
REM
REM  The result is written to:  dist\PythonTutor.exe
REM ============================================================
cd /d "%~dp0"

echo [1/3] Installing PyInstaller (build tool only)...
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [2/3] Building PythonTutor.exe ...
python -m PyInstaller --noconfirm --clean python_tutor.spec
if errorlevel 1 goto :fail

echo [3/3] Done!
echo.
echo    Your standalone program is here:
echo        %~dp0dist\PythonTutor.exe
echo.
echo    Copy that single file to any Windows PC (Python not needed)
echo    and double-click it. The app opens in the default web browser.
echo.
pause
exit /b 0

:fail
echo.
echo Build failed. Make sure Python is installed and on your PATH.
pause
exit /b 1
