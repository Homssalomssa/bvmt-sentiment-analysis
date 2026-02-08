@echo off
cls
echo ====================================================
echo TUNISIAN STOCK SENTIMENT ANALYSIS - SETUP
echo ====================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python is installed

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.
echo ====================================================
echo SETUP COMPLETE
echo ====================================================
echo.
echo Next steps:
echo 1. Run test_system.bat to test everything
echo 2. Run run_system.bat to start the full system
echo 3. Check the generated files in this folder
echo.
pause
