@echo off
cls
echo ====================================================
echo RUNNING SENTIMENT ANALYSIS SYSTEM
echo ====================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo Starting Tunisian Stock Sentiment Analysis System...
echo This will analyze major Tunisian stocks...
echo.
python integrate.py

echo.
echo ====================================================
echo ANALYSIS COMPLETE!
echo ====================================================
echo.
echo Generated files:
echo   stock_sentiment_results.json - Analysis results
echo.
echo You can now:
echo 1. Share results.json with frontend team
echo 2. Integrate with trading dashboard
echo 3. Use sentiment scores for decision making
echo.
pause
