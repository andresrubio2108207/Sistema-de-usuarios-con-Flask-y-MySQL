#!/bin/bash

# Script de configuración para Sistema de Usuarios Flask

echo "==================================="
echo "Sistema de Usuarios Flask - Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado."
    echo "Por favor instala Python 3.8 o superior."
    exit 1
fi

echo "✓ Python 3 encontrado: $(python3 --version)"

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "⚠️  Advertencia: MySQL no está en el PATH."
    echo "Asegúrate de tener MySQL instalado y en ejecución."
fi

# Create virtual environment
echo ""
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activando entorno virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales antes de ejecutar la aplicación."
else
    echo "✓ Archivo .env ya existe."
fi

echo ""
echo "==================================="
echo "✅ Instalación completada!"
echo "==================================="
echo ""
echo "Próximos pasos:"
echo "1. Configura MySQL y ejecuta: mysql -u root -p < database.sql"
echo "2. Edita el archivo .env con tus credenciales"
echo "3. Activa el entorno virtual:"
echo "   - Linux/Mac: source venv/bin/activate"
echo "   - Windows: venv\\Scripts\\activate"
echo "4. Ejecuta la aplicación: python app.py"
echo "5. Abre tu navegador en: http://localhost:5000"
echo ""
