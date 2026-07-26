@echo off
chcp 65001 >nul
REM Deploy using secrets.txt (token never printed to chat)
SETLOCAL
SET "SECFILE=secrets.txt"
IF NOT EXIST "%SECFILE%" (echo secrets.txt missing & exit /b 1)
FOR /F "tokens=1,* delims==" %%A IN ('findstr /B "username=" "%SECFILE%"') DO SET "USER=%%B"
FOR /F "tokens=1,* delims==" %%A IN ('findstr /B "token=" "%SECFILE%"') DO SET "TOKEN=%%B"
SET "REPO=kb-rewaq-digital"
SET "API=https://api.github.com"
IF "%USER%"=="" (echo username empty & exit /b 1)
IF "%TOKEN%"=="" (echo token empty & exit /b 1)

echo [1/5] Creating repo %REPO% for %USER% ...
curl -s -H "Authorization: token %TOKEN%" -H "Accept: application/vnd.github+json" -d "{\"name\":\"%REPO%\",\"description\":\"KB Rewaq Digital - 3D websites & marketing for Kuwait\",\"homepage\":\"https://%USER%.github.io/%REPO%/\",\"public\":true}" %API%/user/repos >repo.json
findstr /C:"full_name" repo.json >nul && echo OK || (echo REPO CREATE FAILED & type repo.json & exit /b 1)

echo [2/5] Git setup ...
git config user.email "kb.rewaq@local"
git config user.name "%USER%"
git rm -r --cached --quiet . >nul 2>&1
git add -A
git commit -q -m "KB Rewaq Digital 3D site v2.0" || echo (nothing new)

echo [3/5] Push ...
git remote remove origin >nul 2>&1
git remote add origin https://%TOKEN%@github.com/%USER%/%REPO%.git
git push -f origin main
IF ERRORLEVEL 1 (echo PUSH FAILED & exit /b 1)

echo [4/5] Enable Pages ...
curl -s -X PUT -H "Authorization: token %TOKEN%" -H "Accept: application/vnd.github+json" -d "{\"source\":{\"branch\":\"main\",\"path\":\"/\"}}" %API%/repos/%USER%/%REPO%/pages >pages.json
echo [5/5] Done.

echo.
echo ============================================================
echo  LIVE IN 1-2 MIN AT:  https://%USER%.github.io/%REPO%/
echo ============================================================
del repo.json pages.json >nul 2>&1
ENDLOCAL
