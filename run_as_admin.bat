@echo off
title DNS Toggler - Run as Administrator
echo ========================================
echo    DNS Toggler - Administrator Mode
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
    echo.
    echo Starting DNS Toggler with full privileges...
    echo.
    python dns_toggler.py
) else (
    echo [INFO] Not running as Administrator
    echo.
    echo DNS Toggler requires Administrator privileges to modify DNS settings.
    echo This script will restart the application with Administrator privileges.
    echo.
    echo Click "Yes" when prompted by User Account Control (UAC).
    echo.
    pause
    
    REM Restart with Administrator privileges
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%~dp0\" && python dns_toggler.py' -Verb RunAs"
)

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
) 