@echo off
chcp 65001 >nul
cd /d "%~dp0"
where pythonw3.11 >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw3.11 desktop.py
) else (
    start "" pythonw desktop.py
)
exit
