@echo off
title DNS Toggler - Uninstall
echo ========================================
echo    DNS Toggler - Uninstall Script
echo ========================================
echo.

echo This script will:
echo 1. Remove desktop shortcut
echo 2. Clean up configuration files
echo 3. Optionally uninstall Python dependencies
echo.

set /p choice="Do you want to continue? (y/N): "
if /i not "%choice%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Removing desktop shortcut...

REM Remove desktop shortcut
set "DESKTOP=%USERPROFILE%\Desktop"
if exist "%DESKTOP%\DNS Toggler.bat" (
    del "%DESKTOP%\DNS Toggler.bat"
    echo [OK] Desktop shortcut removed
) else (
    echo [INFO] Desktop shortcut not found
)

echo.
echo Cleaning up configuration files...

REM Remove configuration files
if exist "custom_dns.json" (
    del "custom_dns.json"
    echo [OK] Custom DNS configuration removed
)

if exist "config.json" (
    del "config.json"
    echo [OK] Application configuration removed
)

echo.
set /p uninstall_deps="Do you want to uninstall Python dependencies? (y/N): "
if /i "%uninstall_deps%"=="y" (
    echo Uninstalling Python dependencies...
    pip uninstall customtkinter pillow psutil -y
    echo [OK] Dependencies uninstalled
) else (
    echo [INFO] Dependencies kept (can be used by other applications)
)

echo.
echo ========================================
echo    Uninstall Complete!
echo ========================================
echo.
echo The DNS Toggler application has been removed.
echo Configuration files have been cleaned up.
echo.
echo Note: The main application files are still in this folder.
echo You can delete the entire folder if you want to completely remove everything.
echo.
pause 