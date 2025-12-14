# Sistema de Usuarios con Flask y MySQL

Sistema completo de gestión de usuarios web desarrollado con Flask y MySQL. Incluye registro, inicio de sesión, recuperación de contraseña por correo, validación de datos y dashboard privado con sesiones seguras y contraseñas hasheadas.

## 🚀 Características

- ✅ **Registro de usuarios** con validación de email y contraseña
- 🔐 **Contraseñas hasheadas** con bcrypt para máxima seguridad
- 🔑 **Inicio de sesión** seguro con verificación de credenciales
- 📊 **Dashboard privado** accesible solo para usuarios autenticados
- 🚪 **Cierre de sesión** con limpieza de sesión
- 📧 **Recuperación de contraseña** vía correo con tokens seguros
- ✨ **Mensajes flash** para notificaciones de error y éxito
- 🎨 **Templates HTML** con diseño moderno y responsive
- 🎨 **CSS estilizado** con paleta de colores profesional
- 🔒 **Variables sensibles** en archivo .env
- 📝 **Validaciones robustas** de datos en frontend y backend

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/andresrubio2108207/Sistema-de-usuarios-con-Flask-y-MySQL.git
cd Sistema-de-usuarios-con-Flask-y-MySQL
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

Inicia sesión en MySQL y ejecuta el script de base de datos:

```bash
mysql -u root -p < database.sql
```

O manualmente:

```sql
CREATE DATABASE IF NOT EXISTS flask_users_db;
USE flask_users_db;
-- Ejecutar el resto del script database.sql
```

### 5. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus valores:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=flask_users_db

# Flask Configuration
SECRET_KEY=genera-una-clave-secreta-aleatoria-aqui
FLASK_ENV=development

# Email Configuration (para recuperación de contraseña)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=tu-email@gmail.com
```

**Nota sobre el email:** Para Gmail, necesitas generar una "Contraseña de aplicación" en tu cuenta de Google. Ve a: Configuración de Google → Seguridad → Verificación en dos pasos → Contraseñas de aplicaciones.

### 6. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
Sistema-de-usuarios-con-Flask-y-MySQL/
│
├── app.py                  # Aplicación principal Flask
├── config.py              # Configuración de la aplicación
├── database.sql           # Script de base de datos
├── requirements.txt       # Dependencias del proyecto
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Archivos ignorados por git
├── README.md             # Este archivo
│
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página de inicio
│   ├── register.html     # Formulario de registro
│   ├── login.html        # Formulario de login
│   ├── dashboard.html    # Panel de usuario
│   ├── forgot_password.html    # Solicitud de recuperación
│   └── reset_password.html     # Restablecer contraseña
│
└── static/               # Archivos estáticos
    └── css/
        └── style.css     # Estilos CSS
```

## 🔒 Seguridad

- **Contraseñas hasheadas:** Utiliza bcrypt para hash seguro de contraseñas
- **Validación de contraseñas:** Mínimo 8 caracteres, incluye mayúsculas, minúsculas y números
- **Tokens seguros:** Utiliza URLSafeTimedSerializer para tokens de recuperación
- **Sesiones seguras:** Flask sessions con SECRET_KEY
- **Protección de rutas:** Decorador @login_required para rutas privadas
- **Variables sensibles:** Almacenadas en .env (no en control de versiones)

## 📝 Validaciones

### Email
- Formato válido de correo electrónico
- Verificación de unicidad en la base de datos

### Contraseña
- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un número

### Nombre de usuario
- Mínimo 3 caracteres
- Verificación de unicidad en la base de datos

## 🌐 Rutas de la Aplicación

- `/` - Página de inicio
- `/register` - Registro de nuevo usuario
- `/login` - Inicio de sesión
- `/dashboard` - Panel de control (requiere autenticación)
- `/logout` - Cerrar sesión
- `/forgot-password` - Solicitar recuperación de contraseña
- `/reset-password/<token>` - Restablecer contraseña con token

## 💡 Uso

1. **Registrarse:** Crea una cuenta con un email válido y una contraseña segura
2. **Iniciar sesión:** Accede con tus credenciales
3. **Dashboard:** Visualiza tu información y gestiona tu cuenta
4. **Recuperar contraseña:** Si olvidas tu contraseña, solicita un enlace de recuperación
5. **Cerrar sesión:** Sal de forma segura del sistema

## 🐛 Solución de Problemas

### Error de conexión a MySQL
- Verifica que MySQL esté ejecutándose
- Comprueba las credenciales en el archivo `.env`
- Asegúrate de que la base de datos `flask_users_db` exista

### Error al enviar emails
- Verifica la configuración SMTP en `.env`
- Para Gmail, usa una contraseña de aplicación
- Comprueba que la verificación en dos pasos esté activada

### Error "SECRET_KEY not set"
- Asegúrate de que el archivo `.env` existe y contiene SECRET_KEY
- Genera una clave segura: `python -c "import secrets; print(secrets.token_hex(32))"`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

Andrés Rubio

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un issue en el repositorio.
