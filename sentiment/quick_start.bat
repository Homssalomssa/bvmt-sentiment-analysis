@echo off
cls
title Tunisian Stock Sentiment Analysis
color 0A

cd /d "%~dp0"

echo ====================================================
echo   TUNISIAN STOCK SENTIMENT ANALYSIS SYSTEM
echo         BVMT Trading Assistant
echo ====================================================
echo.
echo Version: Windows 1.0
echo Focus: Tunisian Stock Exchange (BVMT)
echo.
echo Please select an option:
echo.
echo [1] Setup System (First Time)
echo [2] Test System Components
echo [3] Run Full Analysis
echo [4] Start API Server (Advanced)
echo [5] Exit
echo.

set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" (
    call setup.bat
    goto :end
)

if "%choice%"=="2" (
    call test_system.bat
    goto :end
)

if "%choice%"=="3" (
    call run_system.bat
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo Starting API server on http://localhost:8001
    echo API Docs: http://localhost:8001/docs
    echo Press Ctrl+C to stop.
    echo.
    call venv\Scripts\activate.bat
    python api.py
    goto :end
)

if "%choice%"=="5" (
    exit /b 0
)

echo Invalid choice. Press any key to try again...
pause >nul
call quick_start.bat

:end
pause
