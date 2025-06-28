@echo off
title DNS Toggler - Build Executable
echo ========================================
echo    DNS Toggler - Building Executable
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [OK] Python found
echo.

echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)

echo [OK] PyInstaller installed
echo.

echo Building executable...
echo This may take a few minutes...
echo.

REM Build the executable
pyinstaller --onefile --windowed --uac-admin --name="DNS_Toggler" --version-file=file_version_info.txt dns_toggler.py

if errorlevel 1 (
    echo [ERROR] Failed to build executable
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo Executable created: dist\DNS_Toggler.exe
echo.
echo The executable requires Administrator privileges to modify DNS settings.
echo Users should right-click and select "Run as Administrator".
echo.
pause 