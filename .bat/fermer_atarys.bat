@echo off
echo ==============================================
echo        ARRET SERVEURS ATARYS
echo ==============================================

echo [1/3] Arret serveur Flask (port 5000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do (
    echo Arret processus %%a
    taskkill /f /pid %%a >nul 2>&1
)

echo [2/3] Arret serveur Vite (port 3000 et 3001)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do (
    echo Arret processus %%a
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3001') do (
    echo Arret processus %%a
    taskkill /f /pid %%a >nul 2>&1
)

echo [3/3] Arret processus Python et Node...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

echo ==============================================
echo     🛑 SERVEURS ATARYS ARRETES !
echo ==============================================

pause 