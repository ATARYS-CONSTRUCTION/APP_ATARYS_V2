@echo off
REM ========================================
REM ATARYS - INSTALLATION BACKEND API REST V2
REM ========================================
REM Script pour installer les dépendances backend API REST ATARYS V2
REM Auteur: ATARYS Team
REM Date: 2025 - Version 2.0

REM Aller à la racine du projet si lancé depuis .bat/
cd /d "%~dp0.."

echo.
echo ========================================
echo   ATARYS - INSTALLATION BACKEND API REST V2
echo ========================================
echo.

REM Vérifier si on est dans le bon dossier
if not exist "backend\app\__init__.py" (
    echo ❌ Erreur: Ce script doit être exécuté depuis la racine du projet ATARYS
    echo 📁 Dossier actuel: %CD%
    pause
    exit /b 1
)

REM Vérifier si l'environnement virtuel existe
if not exist "backend\venv\Scripts\activate.bat" (
    echo ❌ Erreur: Environnement virtuel non trouvé
    echo.
    echo 💡 Création de l'environnement virtuel...
    cd backend
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erreur lors de la création de l'environnement virtuel
        pause
        exit /b 1
    )
    cd ..
)

echo ✅ Environnement virtuel détecté
echo.

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call backend\venv\Scripts\activate.bat

REM Installer les dépendances principales
echo 📦 Installation des dépendances principales...
pip install -r backend\requirements\development.txt

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

REM Installer les dépendances supplémentaires si nécessaire
echo 📦 Installation des dépendances supplémentaires...
pip install flask-cors marshmallow

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances supplémentaires
    pause
    exit /b 1
)

REM Vérifier l'installation
echo 🔍 Vérification de l'installation...
python -c "
try:
    import flask
    import flask_sqlalchemy
    import flask_migrate
    import flask_cors
    import marshmallow
    print('✅ Toutes les dépendances sont installées')
except ImportError as e:
    print(f'❌ Erreur: {e}')
    exit(1)
"

if errorlevel 1 (
    echo ❌ Erreur lors de la vérification
    pause
    exit /b 1
)

echo.
echo ✅ Installation terminée avec succès !
echo.
echo 📋 Architecture ATARYS V2:
echo    - Backend Flask avec API REST
echo    - Base de données SQLite dans /data/
echo    - Génération automatique de tables (Module 12.1)
echo    - Frontend React avec Vite
echo.
echo 🚀 Pour lancer le backend:
echo    cd backend
echo    python app.py
echo    ou
echo    python -m flask run
echo.
echo 🌐 URLs:
echo    - Backend API: http://localhost:5000
echo    - Frontend: http://localhost:3000
echo    - Health check: http://localhost:5000/health
echo.

pause 