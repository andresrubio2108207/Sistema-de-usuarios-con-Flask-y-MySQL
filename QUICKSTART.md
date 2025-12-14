# Guía Rápida de Inicio

## Instalación Express (5 minutos)

### 1. Requisitos
- Python 3.8+
- MySQL 5.7+

### 2. Instalación Automática

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### 3. Configurar MySQL
```bash
mysql -u root -p < database.sql
```

### 4. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

**Configuración mínima requerida en .env:**
```env
DB_PASSWORD=tu_password_mysql
SECRET_KEY=genera_una_clave_aleatoria
```

### 5. Ejecutar
```bash
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

python app.py
```

### 6. Abrir en el Navegador
```
http://localhost:5000
```

## Configuración Rápida de Email (Opcional)

Para habilitar la recuperación de contraseña, configura en `.env`:

```env
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
```

**Para Gmail:**
1. Activa verificación en 2 pasos
2. Ve a: https://myaccount.google.com/apppasswords
3. Genera una contraseña de aplicación
4. Úsala en `MAIL_PASSWORD`

## Primera Prueba

1. Abre http://localhost:5000
2. Haz clic en "Crear Cuenta"
3. Registra un usuario
4. Inicia sesión
5. Accede al Dashboard

¡Listo! 🎉

## Comandos Útiles

```bash
# Validar instalación
python validate.py

# Ver logs de MySQL
mysql -u root -p -e "USE flask_users_db; SELECT * FROM users;"

# Limpiar base de datos
mysql -u root -p -e "DROP DATABASE flask_users_db;"
mysql -u root -p < database.sql
```

## Estructura del Proyecto

```
.
├── app.py              # Aplicación principal
├── config.py           # Configuración
├── database.sql        # Schema de BD
├── requirements.txt    # Dependencias
├── templates/          # HTML templates
├── static/css/         # Estilos
└── .env               # Variables (crear desde .env.example)
```

## Soporte

- **Documentación completa:** Ver README.md
- **Guía de pruebas:** Ver TESTING.md
- **Issues:** https://github.com/andresrubio2108207/Sistema-de-usuarios-con-Flask-y-MySQL/issues
