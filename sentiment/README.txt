TUNISIAN STOCK SENTIMENT ANALYSIS SYSTEM - Windows
==================================================

Project: Sentiment analysis for Tunisian Stock Exchange (BVMT)
Version: 1.0 (Windows Compatible)

FOLDER STRUCTURE
----------------
d:\sentiment\
  venv\                          - Virtual environment
  analyzer.py                     - Sentiment analyzer (FR/AR/EN)
  scraper.py                      - News scraper (mock)
  integrate.py                    - Integration system
  api.py                          - FastAPI server (optional)
  requirements.txt                - Dependencies
  setup.bat                       - Setup script
  test_system.bat                 - Test script
  run_system.bat                  - Run full analysis
  quick_start.bat                 - Menu script
  stock_sentiment_results.json    - Generated results (after run)
  README.txt                      - This file

QUICK START
-----------
1. First time: Double-click setup.bat (creates venv, installs deps)
2. Test: Double-click test_system.bat
3. Run analysis: Double-click run_system.bat
4. Or use quick_start.bat for menu

API SERVER (optional)
--------------------
Run: quick_start.bat -> option 4, or: venv\Scripts\activate && python api.py
Then open: http://localhost:8001/docs

REQUIREMENTS
------------
- Windows x64
- Python 3.8 or higher (python.org)
- No GPU or ML libraries required (keyword-based analyzer)
