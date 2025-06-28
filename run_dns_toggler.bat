@echo off
title DNS Toggler - Windows
echo Starting DNS Toggler...
echo.
echo This application requires Administrator privileges to modify DNS settings.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    if exist "%~dp0requirements.txt" (
        pip install -r "%~dp0requirements.txt"
    ) else (
        pip install customtkinter pillow psutil
    )
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting DNS Toggler application...
if exist "%~dp0dns_toggler.py" (
    python "%~dp0dns_toggler.py"
) else (
    echo ERROR: dns_toggler.py not found in current directory
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
) 