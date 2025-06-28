# DNS Toggler Launcher Script
# This script launches the DNS Toggler application with proper setup

param(
    [switch]$InstallDependencies,
    [switch]$Help
)

if ($Help) {
    Write-Host "DNS Toggler Launcher" -ForegroundColor Green
    Write-Host "Usage: .\run_dns_toggler.ps1 [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -InstallDependencies  Force install/reinstall dependencies" -ForegroundColor White
    Write-Host "  -Help                 Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: This application requires Administrator privileges to modify DNS settings." -ForegroundColor Red
    exit 0
}

# Set console title
$Host.UI.RawUI.WindowTitle = "DNS Toggler - Windows"

Write-Host "Starting DNS Toggler..." -ForegroundColor Green
Write-Host ""
Write-Host "This application requires Administrator privileges to modify DNS settings." -ForegroundColor Yellow
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator!" -ForegroundColor Red
    Write-Host "DNS changes may fail. Consider running as Administrator." -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7 or higher from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check and install dependencies
Write-Host "Checking dependencies..." -ForegroundColor Cyan

$dependencies = @("customtkinter", "pillow", "psutil")
$missingDeps = @()

foreach ($dep in $dependencies) {
    try {
        python -c "import $dep" 2>$null
        if ($LASTEXITCODE -ne 0) {
            $missingDeps += $dep
        }
    } catch {
        $missingDeps += $dep
    }
}

if ($missingDeps.Count -gt 0 -or $InstallDependencies) {
    Write-Host "Installing required dependencies..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install dependencies"
        }
        Write-Host "Dependencies installed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Write-Host "Try running: pip install -r requirements.txt" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "All dependencies are already installed." -ForegroundColor Green
}

# Check if main script exists
if (-not (Test-Path "dns_toggler.py")) {
    Write-Host "ERROR: dns_toggler.py not found!" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the correct directory." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting DNS Toggler application..." -ForegroundColor Green
Write-Host ""

# Run the application
try {
    python dns_toggler.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Application exited with an error (code: $LASTEXITCODE)" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to start the application" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit" 