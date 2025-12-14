@echo off
REM Script de configuración para Sistema de Usuarios Flask - Windows

echo ===================================
echo Sistema de Usuarios Flask - Setup
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no esta instalado.
    echo Por favor instala Python 3.8 o superior.
    pause
    exit /b 1
)

echo Python encontrado:
python --version

REM Create virtual environment
echo.
echo Creando entorno virtual...
python -m venv venv

REM Activate virtual environment
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Install dependencies
echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creando archivo .env...
    copy .env.example .env
    echo IMPORTANTE: Edita el archivo .env con tus credenciales antes de ejecutar la aplicacion.
) else (
    echo Archivo .env ya existe.
)

echo.
echo ===================================
echo Instalacion completada!
echo ===================================
echo.
echo Proximos pasos:
echo 1. Configura MySQL y ejecuta: mysql -u root -p ^< database.sql
echo 2. Edita el archivo .env con tus credenciales
echo 3. Activa el entorno virtual: venv\Scripts\activate
echo 4. Ejecuta la aplicacion: python app.py
echo 5. Abre tu navegador en: http://localhost:5000
echo.
pause
