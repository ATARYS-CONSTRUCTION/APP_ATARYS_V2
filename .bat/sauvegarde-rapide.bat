@echo off
REM ATARYS V2 - Sauvegarde Rapide
echo ====================================
echo    ATARYS V2 - SAUVEGARDE RAPIDE
echo ====================================

cd /d "C:\DEV\APP_ATARYS V2"

REM Vérifier si PowerShell est disponible
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur: PowerShell n'est pas disponible
    pause
    exit /b 1
)

REM Lancer le script de sauvegarde
echo Lancement de la sauvegarde automatique...
powershell -ExecutionPolicy Bypass -File ".\.bat\sauvegarde-auto.ps1"

echo.
echo Sauvegarde terminée !
pause 