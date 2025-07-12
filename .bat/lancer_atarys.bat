@echo off
REM === Script de lancement ATARYS V2 avec activation des environnements ===

REM Se placer à la racine du projet, peu importe d'où on lance le .bat
cd /d "%~dp0.."

REM Backend : active le venv puis lance Flask
start "ATARYS Backend" cmd /k "cd backend && call venv\Scripts\activate && set FLASK_APP=app && set FLASK_ENV=development && flask run --port=5000"

REM Frontend : lance Vite/React
start "ATARYS Frontend" cmd /k "cd frontend && npm run dev -- --port 3000"

REM Ouvre le navigateur
timeout /t 3 >nul
start http://localhost:3000

echo ATARYS V2 : Backend sur http://localhost:5000 et Frontend sur http://localhost:3000
pause 