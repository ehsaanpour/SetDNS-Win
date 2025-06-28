@echo off
title DNS Toggler - Installation
echo ========================================
echo    DNS Toggler - Installation Script
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
) else (
    echo [ERROR] This script requires Administrator privileges
    echo Please right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo Checking Python installation...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python found

echo.
echo Checking dependencies...

REM Check if requirements.txt exists
if not exist "%~dp0requirements.txt" (
    echo [ERROR] requirements.txt not found in current directory
    echo Make sure you're running this script from the DNS Toggler folder
    pause
    exit /b 1
)

REM Check if dependencies are already installed
python -c "import customtkinter, pillow, psutil" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        echo Try running: pip install --upgrade pip
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] Dependencies already installed
)

echo.
echo Creating desktop shortcut...

REM Create desktop shortcut
set "DESKTOP=%USERPROFILE%\Desktop"
set "SCRIPT_PATH=%~dp0"

echo @echo off > "%DESKTOP%\DNS Toggler.bat"
echo cd /d "%SCRIPT_PATH%" >> "%DESKTOP%\DNS Toggler.bat"
echo call run_dns_toggler.bat >> "%DESKTOP%\DNS Toggler.bat"

echo [OK] Desktop shortcut created

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo You can now:
echo 1. Double-click "DNS Toggler.bat" on your desktop
echo 2. Or run "run_dns_toggler.bat" from this folder
echo 3. Or run "python dns_toggler.py" directly
echo.
echo Remember to run as Administrator for DNS changes!
echo.
pause 