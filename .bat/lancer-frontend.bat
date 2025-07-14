@echo off
REM ========================================
REM ATARYS - LANCEMENT FRONTEND V2
REM ========================================
REM Script pour lancer le frontend React ATARYS V2
REM Auteur: ATARYS Team
REM Date: 2025 - Version 2.0

REM Aller à la racine du projet si lancé depuis .bat/
cd /d "%~dp0.."

echo.
echo ========================================
echo   ATARYS - LANCEMENT FRONTEND V2
echo ========================================
echo.

REM Vérifier si on est dans le bon dossier
if not exist "frontend\package.json" (
    echo ❌ Erreur: Ce script doit être exécuté depuis la racine du projet ATARYS
    echo 📁 Dossier actuel: %CD%
    echo.
    echo 💡 Solution: Naviguez vers le dossier racine du projet
    pause
    exit /b 1
)

REM Vérifier si Node.js est installé
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Node.js non trouvé
    echo.
    echo 💡 Solution: Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js détecté
echo 📁 Dossier: %CD%
echo.

REM Vérifier si les dépendances sont installées
if not exist "frontend\node_modules" (
    echo 📦 Installation des dépendances frontend...
    cd frontend
    npm install
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation des dépendances
        pause
        exit /b 1
    )
    cd ..
)

echo ✅ Dépendances frontend disponibles
echo.

echo 🚀 Démarrage du frontend ATARYS V2...
echo 🌐 Interface: http://localhost:3000
echo 🔗 Proxy API: http://localhost:5000
echo.
echo 💡 Pour arrêter: Ctrl+C
echo.
cd frontend
npm run dev
cd ..
echo.
echo ✅ Frontend ATARYS V2 fermé
echo.
echo Appuyez sur une touche pour fermer...
pause 