@echo off
REM ========================================
REM ATARYS - OUVERTURE FLASK-ADMIN
REM ========================================
REM Script pour ouvrir l'interface Flask-Admin
REM Auteur: ATARYS Team
REM Date: 2025

echo.
echo ========================================
echo   ATARYS - OUVERTURE FLASK-ADMIN
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

REM Vérifier les dépendances Flask-Admin
echo 🔍 Vérification des dépendances...
python -c "import flask_admin" 2>nul
if errorlevel 1 (
    echo ❌ Flask-Admin non installé
    echo.
    echo 💡 Installation des dépendances...
    pip install flask-admin
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation
        pause
        exit /b 1
    )
)

echo ✅ Flask-Admin disponible
echo.

REM Démarrer Flask-Admin
echo 🚀 Démarrage de Flask-Admin...
echo 📊 Interface: http://localhost:5000/admin
echo.
echo 💡 Pour arrêter: Ctrl+C
echo.

REM Lancer le serveur Flask avec Flask-Admin
cd backend
python -c "
from app import create_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = create_app('development')

# Configuration Flask-Admin
admin = Admin(app, name='ATARYS Admin', template_mode='bootstrap4')

# Les vues seront ajoutées au fur et à mesure du développement
# selon les modules ATARYS créés

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
"

echo.
echo ✅ Flask-Admin fermé
pause 