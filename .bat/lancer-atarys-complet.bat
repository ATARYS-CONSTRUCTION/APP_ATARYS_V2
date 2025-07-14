@echo off
REM ========================================
REM ATARYS - LANCEMENT COMPLET V2
REM ========================================
REM Script pour lancer l'ensemble ATARYS V2 (Backend + Frontend)
REM Auteur: ATARYS Team
REM Date: 2025 - Version 2.0

REM Aller à la racine du projet si lancé depuis .bat/
cd /d "%~dp0.."

echo.
echo ========================================
echo   ATARYS - LANCEMENT COMPLET V2
echo ========================================
echo.

REM Vérifier si on est dans le bon dossier
if not exist "backend\app\__init__.py" (
    echo ❌ Erreur: Ce script doit être exécuté depuis la racine du projet ATARYS
    echo 📁 Dossier actuel: %CD%
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ❌ Erreur: Frontend non trouvé
    echo 📁 Cherché: frontend\package.json
    pause
    exit /b 1
)

echo ✅ Structure du projet détectée
echo 📁 Dossier: %CD%
echo.

REM Vérifier l'environnement virtuel backend
if not exist "backend\venv\Scripts\activate.bat" (
    echo ❌ Erreur: Environnement virtuel backend non trouvé
    echo.
    echo 💡 Solution: Lancez d'abord installer-backend.bat
    pause
    exit /b 1
)

REM Vérifier Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Node.js non trouvé
    echo.
    echo 💡 Solution: Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Environnements détectés
echo.

echo 🚀 Lancement d'ATARYS V2 complet...
echo.
echo 📊 Backend API: http://localhost:5000
echo 🌐 Frontend: http://localhost:3000
echo 🔍 Health check: http://localhost:5000/health
echo.
echo 💡 Pour arrêter: Ctrl+C dans chaque fenêtre
echo.

REM Lancer le backend dans une nouvelle fenêtre
echo 🔧 Lancement du backend...
start "ATARYS Backend" cmd /k "cd /d %CD% && call backend\venv\Scripts\activate.bat && cd backend && python app.py"

REM Attendre un peu pour que le backend démarre
timeout /t 3 /nobreak >nul

REM Lancer le frontend dans une nouvelle fenêtre
echo 🌐 Lancement du frontend...
start "ATARYS Frontend" cmd /k "cd /d %CD% && cd frontend && npm run dev"

REM Attendre que le frontend démarre puis ouvrir le navigateur
echo.
echo ⏳ Attente du démarrage du frontend...
timeout /t 5 /nobreak >nul

echo 🌐 Ouverture du navigateur sur http://localhost:3000...
start http://localhost:3000

echo.
echo ✅ ATARYS V2 lancé avec succès !
echo.
echo 📋 Fenêtres ouvertes:
echo    - Backend Flask (port 5000)
echo    - Frontend React (port 3000)
echo    - Navigateur (http://localhost:3000)
echo.
echo 💡 Pour arrêter: Fermez les fenêtres ou Ctrl+C
echo.
pause 