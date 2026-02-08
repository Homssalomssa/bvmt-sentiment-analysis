@echo off
setlocal EnableDelayedExpansion
title Push to GitHub - BVMT Sentiment Analysis
color 0B
cd /d "%~dp0"

echo.
echo  ============================================================
echo    BVMT SENTIMENT ANALYSIS - PUSH TO GITHUB
echo    IHEC-CODELAB 2.0 Hackathon
echo  ============================================================
echo.

REM --- 1. Check if Git is installed ---
git --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo  [X] Git is not installed or not in PATH.
    echo.
    echo  Please install Git:
    echo    1. Download: https://git-scm.com/download/win
    echo    2. Run the installer and choose "Git from the command line"
    echo    3. Restart this script
    echo.
    pause
    exit /b 1
)
echo  [OK] Git is installed.
git --version
echo.

REM --- 2. Initialize Git if not already ---
if not exist ".git" (
    echo  [*] Initializing Git repository...
    git init
    if errorlevel 1 (
        color 0C
        echo  [X] Failed to initialize Git.
        pause
        exit /b 1
    )
    echo  [OK] Git repository initialized.
) else (
    echo  [OK] Git repository already exists.
)
echo.

REM --- 3. Ensure .gitignore exists ---
if not exist ".gitignore" (
    echo  [*] Creating .gitignore...
    (
        echo venv/
        echo __pycache__/
        echo *.pyc
        echo stock_sentiment_results.json
        echo *.log
        echo .DS_Store
    ) > .gitignore
    echo  [OK] .gitignore created.
) else (
    echo  [OK] .gitignore found.
)
echo.

REM --- 4. Create README.md if missing ---
if not exist "README.md" (
    echo  [!] README.md not found. Please add README.md and run again.
    echo      You can copy from the repo or create one.
    set /p cont="Continue without README? (y/n): "
    if /i not "!cont!"=="y" exit /b 0
) else (
    echo  [OK] README.md found.
)
echo.

REM --- 5. Add all files (respecting .gitignore) ---
echo  [*] Adding files...
git add -A
if errorlevel 1 (
    color 0C
    echo  [X] Failed to add files.
    pause
    exit /b 1
)
echo  [OK] Files staged.
git status --short
echo.

REM --- 6. Commit ---
set "COMMIT_MSG=Sentiment Analysis Module - Ready for team integration - IHEC-CODELAB 2.0 Hackathon"
echo  [*] Committing with message: "%COMMIT_MSG%"
git commit -m "%COMMIT_MSG%" 2>nul
if errorlevel 1 (
    git diff --cached --quiet 2>nul
    if errorlevel 1 (
        echo  [OK] Nothing to commit (working tree clean^).
    ) else (
        echo  [!] Commit failed or nothing to commit. Check 'git status'.
    )
) else (
    echo  [OK] Commit created.
)
echo.

REM --- 7. Set remote ---
set REMOTE_URL=https://github.com/Homssalomssa/bvmt-sentiment-analysis
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo  [*] Adding remote 'origin'...
    git remote add origin %REMOTE_URL%
    echo  [OK] Remote added.
) else (
    git remote set-url origin %REMOTE_URL%
    echo  [OK] Remote 'origin' set to %REMOTE_URL%
)
echo.

REM --- 8. Push to main ---
echo  [*] Pushing to main...
git branch -M main 2>nul
git push -u origin main 2>nul
if errorlevel 1 (
    echo.
    echo  [!] If this is your first push, you may need to:
    echo      - Create the repo on GitHub: %REMOTE_URL%
    echo      - Log in: git config --global user.name "Your Name"
    echo                git config --global user.email "your@email.com"
    echo      - If you use 2FA, use a Personal Access Token as password
    echo.
    git push -u origin main
    if errorlevel 1 (
        color 0C
        echo  [X] Push failed. Check errors above.
        pause
        exit /b 1
    )
)
echo.
color 0A
echo  ============================================================
echo    SUCCESS - Code pushed to GitHub
echo  ============================================================
echo.
echo    Repository: %REMOTE_URL%
echo.
echo    Next steps:
echo    - Share the link with your team (Person 1, 2, 4^)
echo    - Clone on other machines: git clone %REMOTE_URL%
echo    - See README.md and team_integration.md for integration
echo.
echo  ============================================================
pause
