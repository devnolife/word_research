# Word Research Analyzer - Web Frontend Launcher
# PowerShell script to start the web application

Write-Host "========================================" -ForegroundColor Blue
Write-Host "Word Research Analyzer - Web Frontend" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing web dependencies..." -ForegroundColor Yellow
try {
    pip install -r web_requirements.txt
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Some dependencies may have failed to install" -ForegroundColor Yellow
    Write-Host "The application may still work with existing packages" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Word Research Analyzer Web Server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Access the application at: " -NoNewline
Write-Host "http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the web server
try {
    python app.py
} catch {
    Write-Host "ERROR: Failed to start the web server" -ForegroundColor Red
    Write-Host "Please check the error messages above" -ForegroundColor Red
}

Read-Host "Press Enter to exit"
