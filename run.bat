@echo off
REM Run the app from source (requires Python 3.8+).
cd /d "%~dp0"
python app.py %*
