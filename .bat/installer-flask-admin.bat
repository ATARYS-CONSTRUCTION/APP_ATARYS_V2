@echo off
REM ========================================
REM ATARYS - INSTALLATION FLASK-ADMIN
REM ========================================
REM Script pour installer Flask-Admin et ses dépendances
REM Auteur: ATARYS Team
REM Date: 2025

REM Aller à la racine du projet si lancé depuis .bat/
cd /d "%~dp0.."

echo.
echo ========================================
echo   ATARYS - INSTALLATION FLASK-ADMIN
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

REM Installer Flask-Admin
echo 📦 Installation de Flask-Admin...
pip install flask-admin

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation de Flask-Admin
    pause
    exit /b 1
)

REM Installer les dépendances supplémentaires
echo 📦 Installation des dépendances supplémentaires...
pip install flask-sqlalchemy flask-migrate

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

REM Vérifier l'installation
echo 🔍 Vérification de l'installation...
python -c "
try:
    import flask_admin
    import flask_sqlalchemy
    import flask_migrate
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
echo 📋 Prochaines étapes:
echo    1. Créer les modèles SQLAlchemy selon modules ATARYS
echo    2. Configurer Flask-Admin dans backend/admin_atarys.py
echo    3. Lancer avec ouvrir-flask-admin.bat
echo.
echo 💡 Pour tester: python -c "import flask_admin; print('OK')"
echo.

pause 