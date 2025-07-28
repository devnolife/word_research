@echo off
echo ========================================
echo Word Research Analyzer - Web Frontend
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing web dependencies...
pip install -r web_requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies may have failed to install
    echo The application may still work with existing packages
)

echo.
echo Starting Word Research Analyzer Web Server...
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
