@echo off
REM ========================================
REM ATARYS - LANCEMENT BACKEND API REST V2
REM ========================================
REM Script pour lancer le backend Flask API REST ATARYS V2
REM Auteur: ATARYS Team
REM Date: 2025 - Version 2.0

REM Aller à la racine du projet si lancé depuis .bat/
cd /d "%~dp0.."

echo.
echo ========================================
echo   ATARYS - LANCEMENT BACKEND API REST V2
echo ========================================
echo.

REM Vérifier si on est dans le bon dossier
if not exist "backend\app\__init__.py" (
    echo ❌ Erreur: Ce script doit être exécuté depuis la racine du projet ATARYS
    echo 📁 Dossier actuel: %CD%
    echo.
    echo 💡 Solution: Naviguez vers le dossier racine du projet
    pause
    exit /b 1
)

REM Vérifier si l'environnement virtuel existe
if not exist "backend\venv\Scripts\activate.bat" (
    echo ❌ Erreur: Environnement virtuel non trouvé
    echo 📁 Cherché: backend\venv\Scripts\activate.bat
    echo.
    echo 💡 Solution: Créez l'environnement virtuel avec:
    echo    installer-backend.bat
    echo    ou manuellement:
    echo    cd backend
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo    pip install -r requirements\development.txt
    pause
    exit /b 1
)

echo ✅ Environnement détecté
echo 📁 Dossier: %CD%
echo.

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call backend\venv\Scripts\activate.bat

REM Vérifier les dépendances Flask
echo 🔍 Vérification des dépendances...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Flask non installé
    echo.
    echo 💡 Installation des dépendances...
    pip install -r backend\requirements\development.txt
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation
        pause
        exit /b 1
    )
)

echo ✅ Flask disponible
echo.

echo 🚀 Démarrage du backend ATARYS V2 (API REST)...
echo 📊 API REST: http://localhost:5000
echo 🔍 Health check: http://localhost:5000/health
echo 📋 API Table Generator: http://localhost:5000/api/table-generator/
echo.
echo 💡 Pour arrêter: Ctrl+C
echo.
cd backend
python app.py
cd ..
echo.
echo ✅ Backend ATARYS V2 fermé
echo.
echo Appuyez sur une touche pour fermer...
pause 