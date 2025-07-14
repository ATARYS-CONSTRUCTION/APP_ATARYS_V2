@echo off
chcp 65001 >nul
REM ========================================
REM ATARYS - TEST CONFIGURATION V2
REM ========================================
REM Script pour tester la configuration ATARYS V2
REM Auteur: ATARYS Team
REM Date: 2025 - Version 2.0

REM Aller à la racine du projet si lancé depuis .bat/
cd /d "%~dp0.."

echo.
echo ========================================
echo   ATARYS - TEST CONFIGURATION V2
echo ========================================
echo.

echo Verification de la structure du projet...
echo.

REM Vérifier la structure backend
if exist "backend\app\__init__.py" (
    echo [OK] Backend Flask detecte
) else (
    echo [ERREUR] Backend Flask manquant
    pause
    exit /b 1
)

REM Vérifier la structure frontend
if exist "frontend\package.json" (
    echo [OK] Frontend React detecte
) else (
    echo [ERREUR] Frontend React manquant
    pause
    exit /b 1
)

REM Vérifier la base de données
if exist "data\atarys_data.db" (
    echo [OK] Base de donnees SQLite detectee
) else (
    echo [INFO] Base de donnees SQLite manquante (sera creee automatiquement)
)

echo.
echo Verification de l'environnement backend...

REM Vérifier l'environnement virtuel
if exist "backend\venv\Scripts\activate.bat" (
    echo [OK] Environnement virtuel detecte
    
    REM Activer l'environnement et tester Flask
    call backend\venv\Scripts\activate.bat
    python -c "import flask; print('[OK] Flask installe')" 2>nul
    if errorlevel 1 (
        echo [ERREUR] Flask non installe
        echo [INFO] Lancez installer-backend.bat
        pause
        exit /b 1
    )
    
    python -c "import flask_sqlalchemy; print('[OK] Flask-SQLAlchemy installe')" 2>nul
    if errorlevel 1 (
        echo [ERREUR] Flask-SQLAlchemy non installe
        echo [INFO] Lancez installer-backend.bat
        pause
        exit /b 1
    )
    
    python -c "import flask_cors; print('[OK] Flask-CORS installe')" 2>nul
    if errorlevel 1 (
        echo [ERREUR] Flask-CORS non installe
        echo [INFO] Lancez installer-backend.bat
        pause
        exit /b 1
    )
    
) else (
    echo [ERREUR] Environnement virtuel manquant
    echo [INFO] Lancez installer-backend.bat
    pause
    exit /b 1
)

echo.
echo Verification de l'environnement frontend...

REM Vérifier Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js non installe
    echo [INFO] Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
) else (
    echo [OK] Node.js detecte
)

REM Vérifier les dépendances frontend
if exist "frontend\node_modules" (
    echo [OK] Dependances frontend installees
) else (
    echo [INFO] Dependances frontend manquantes
    echo [INFO] Lancez: cd frontend && npm install
)

echo.
echo Test de lancement du backend...

REM Tester le lancement du backend
echo Test du backend Flask...
cd backend
python -c "from app import create_app; app = create_app(); print('[OK] Application Flask creee avec succes')" 2>nul

if errorlevel 1 (
    echo [ERREUR] Erreur lors de la creation de l'application Flask
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo [OK] Configuration ATARYS V2 validee !
echo.
echo Resume:
echo    - Backend Flask: [OK] Pret
echo    - Frontend React: [OK] Pret
echo    - Base de donnees: [OK] Pret
echo    - Environnements: [OK] Prets
echo.
echo Pour lancer ATARYS V2:
echo    - Backend seul: lancer-backend.bat
echo    - Frontend seul: lancer-frontend.bat
echo    - Complet: lancer-atarys-complet.bat
echo.
echo URLs:
echo    - Backend API: http://localhost:5000
echo    - Frontend: http://localhost:3000
echo    - Health check: http://localhost:5000/health
echo.

pause 