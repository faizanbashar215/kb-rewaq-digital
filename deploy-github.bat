@echo off
chcp 65001 >nul
REM ============================================================
REM  KB Rewaq Digital — Deploy to GitHub Pages (ONE COMMAND)
REM ============================================================
REM  STEP 1: Get a GitHub token (free, 2 min):
REM    1. Go to https://github.com/settings/tokens
REM    2. Click "Generate new token (classic)"
REM    3. Tick "repo" (full control) + "workflow"
REM    4. Copy the token (starts with ghp_)
REM    5. Paste it below OR save to token.txt in this folder
REM  STEP 2: Double-click this file (or run: deploy-github.bat)
REM  Result: live site at https://<user>.github.io/kb-rewaq-digital/
REM ============================================================

SET REPO=kb-rewaq-digital
SET /P USER=Enter your GitHub username: 

REM --- token: from token.txt if present, else prompt ---
IF EXIST token.txt (
  SET /P TOKEN=<token.txt
) ELSE (
  SET /P TOKEN=Enter GitHub token (ghp_...): 
)

SET API=https://api.github.com
SET AUTH=-H "Authorization: token %TOKEN%" -H "Accept: application/vnd.github+json"

echo.
echo [1/5] Creating repo %REPO% ...
curl -s %AUTH% -d "{\"name\":\"%REPO%\",\"description\":\"KB Rewaq Digital — websites & marketing for Kuwait businesses\",\"homepage\":\"https://%USER%.github.io/%REPO%/\",\"public\":true}" %API%/user/repos >repo.json
findstr /C:"\"full_name\"" repo.json >nul && echo OK || (echo FAILED to create repo. Check token/username. & pause & exit /b 1)

echo [2/5] Initializing git ...
IF NOT EXIST .git (git init -q)
git checkout -B main
git config user.email "kb.rewaq@local"
git config user.name "%USER%"

echo [3/5] Adding files ...
git add -A
git commit -q -m "KB Rewaq Digital site v1.0" || echo (nothing to commit)

echo [4/5] Pushing to GitHub ...
git remote remove origin >nul 2>&1
git remote add origin https://%TOKEN%@github.com/%USER%/%REPO%.git
git push -f origin main
IF ERRORLEVEL 1 (echo PUSH FAILED. & pause & exit /b 1)

echo [5/5] Enabling GitHub Pages ...
curl -s %AUTH% -X PUT -d "{\"source\":{\"branch\":\"main\",\"path\":\"/\"}}" %API%/repos/%USER%/%REPO%/pages >pages.json
echo.
echo ============================================================
echo  DONE! Your site goes live in 1-2 minutes at:
echo  https://%USER%.github.io/%REPO%/
echo ============================================================
echo (If Pages shows 404 first, wait 60s and refresh)
del repo.json pages.json >nul 2>&1
pause
