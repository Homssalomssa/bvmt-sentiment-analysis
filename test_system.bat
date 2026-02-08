@echo off
cls
echo ====================================================
echo TESTING SENTIMENT ANALYSIS SYSTEM
echo ====================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo 1. Testing Sentiment Analyzer...
echo =================================
python analyzer.py
echo.

echo.
echo 2. Testing News Scraper...
echo ===========================
python scraper.py
echo.

echo.
echo 3. Testing Full System Integration...
echo =====================================
python integrate.py
echo.

echo ====================================================
echo ALL TESTS COMPLETE!
echo ====================================================
echo.
echo Check the output above for any errors.
echo If everything ran successfully, the system is working.
echo.
pause
