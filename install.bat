@echo off
REM Installation : cree le venv et installe les dependances.
REM Pre-requis : Python 3.10+ installe et accessible via "python" dans le PATH.

cd /d "%~dp0"

echo.
echo === Verification de Python ===
python --version
if errorlevel 1 (
    echo.
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Telecharge-le sur https://www.python.org/downloads/ ^(coche "Add to PATH"^)
    pause
    exit /b 1
)

echo.
echo === Creation du venv ===
if exist .venv (
    echo Le venv existe deja, on saute cette etape.
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer le venv.
        pause
        exit /b 1
    )
)

echo.
echo === Installation des dependances ===
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation des dependances.
    pause
    exit /b 1
)

echo.
echo === Installation terminee ! ===
echo.
echo Lance Image_to_ICO.vbs ou Image_to_ICO_ZOOM.vbs pour utiliser l'app.
echo Au premier run, rembg telechargera son modele u2net (~170 Mo).
echo.
pause
