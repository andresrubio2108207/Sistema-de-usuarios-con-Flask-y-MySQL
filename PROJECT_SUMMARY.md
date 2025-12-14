# Sistema de Usuarios con Flask y MySQL
## Resumen del Proyecto

### 📊 Estadísticas del Proyecto

- **Archivos totales:** 19
- **Líneas de código Python:** ~350
- **Templates HTML:** 7
- **Archivos CSS:** 1
- **Scripts de utilidad:** 3
- **Documentación:** 3 archivos

### 🎯 Características Implementadas

#### 1. Autenticación y Autorización
- ✅ Registro de usuarios con validación completa
- ✅ Inicio de sesión seguro
- ✅ Cierre de sesión
- ✅ Dashboard privado (requiere autenticación)
- ✅ Decorador `@login_required` para proteger rutas

#### 2. Seguridad
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Validación de contraseña fuerte:
  - Mínimo 8 caracteres
  - Al menos una mayúscula
  - Al menos una minúscula
  - Al menos un número
- ✅ Validación de formato de email
- ✅ Tokens seguros para recuperación de contraseña
- ✅ Protección contra SQL injection
- ✅ Variables sensibles en .env
- ✅ Debug mode controlado por ambiente

#### 3. Recuperación de Contraseña
- ✅ Solicitud de recuperación por email
- ✅ Generación de tokens seguros con expiración (1 hora)
- ✅ Envío de email con instrucciones
- ✅ Formulario de restablecimiento
- ✅ Validación de tokens (uso único)

#### 4. Experiencia de Usuario
- ✅ Mensajes flash informativos
- ✅ Diseño responsive
- ✅ Interfaz moderna y limpia
- ✅ Navegación intuitiva
- ✅ Validación en frontend y backend

#### 5. Base de Datos
- ✅ Schema MySQL optimizado
- ✅ Tabla de usuarios con índices
- ✅ Tabla de tokens de recuperación
- ✅ Relaciones con foreign keys
- ✅ Timestamps automáticos

### 📂 Estructura de Archivos

```
Sistema-de-usuarios-con-Flask-y-MySQL/
│
├── app.py                      # Aplicación Flask principal (350 líneas)
├── config.py                   # Configuración centralizada
├── database.sql                # Schema de base de datos
├── requirements.txt            # Dependencias Python
│
├── templates/                  # Templates HTML Jinja2
│   ├── base.html              # Template base con navegación
│   ├── index.html             # Página de inicio
│   ├── register.html          # Formulario de registro
│   ├── login.html             # Formulario de login
│   ├── dashboard.html         # Panel de usuario
│   ├── forgot_password.html   # Solicitud de recuperación
│   └── reset_password.html    # Restablecimiento de contraseña
│
├── static/
│   └── css/
│       └── style.css          # Estilos CSS (200+ líneas)
│
├── setup.sh                   # Script de instalación (Linux/Mac)
├── setup.bat                  # Script de instalación (Windows)
├── validate.py                # Script de validación
│
├── .env.example               # Plantilla de variables de entorno
├── .gitignore                 # Archivos ignorados por Git
│
├── README.md                  # Documentación principal
├── QUICKSTART.md              # Guía de inicio rápido
└── TESTING.md                 # Guía de pruebas
```

### 🔧 Tecnologías Utilizadas

**Backend:**
- Flask 3.0.0 - Framework web
- Flask-MySQLdb 2.0.0 - Integración MySQL
- Flask-Mail 0.9.1 - Envío de emails
- bcrypt 4.1.2 - Hash de contraseñas
- python-dotenv 1.0.0 - Variables de entorno
- itsdangerous 2.1.2 - Tokens seguros
- Werkzeug 3.0.3 - Utilidades WSGI

**Frontend:**
- HTML5
- CSS3 (diseño responsive)
- Jinja2 templates

**Base de Datos:**
- MySQL 5.7+
- InnoDB engine
- UTF-8 Unicode

### 🔒 Características de Seguridad

1. **Protección de Contraseñas:**
   - Hash bcrypt con salt aleatorio
   - Nunca se almacenan en texto plano
   - Validación de fortaleza

2. **Protección de Sesiones:**
   - Secret key en variable de entorno
   - Session cookies con HttpOnly
   - Timeout automático

3. **Protección de Base de Datos:**
   - Consultas parametrizadas
   - Prevención de SQL injection
   - Índices para optimización

4. **Recuperación Segura:**
   - Tokens con expiración temporal
   - Uso único por token
   - Verificación de firma

5. **Configuración:**
   - Variables sensibles en .env
   - .env excluido del repositorio
   - Debug mode por variable de entorno

### 📈 Flujos de Usuario

#### Flujo de Registro
```
1. Usuario accede a /register
2. Completa formulario (username, email, password)
3. Sistema valida datos:
   - Formato de email
   - Fortaleza de contraseña
   - Unicidad de usuario/email
4. Sistema hashea contraseña
5. Guarda usuario en base de datos
6. Redirige a login con mensaje de éxito
```

#### Flujo de Login
```
1. Usuario accede a /login
2. Ingresa email y contraseña
3. Sistema busca usuario en BD
4. Verifica contraseña con bcrypt
5. Crea sesión
6. Redirige a dashboard
```

#### Flujo de Recuperación
```
1. Usuario accede a /forgot-password
2. Ingresa email
3. Sistema genera token seguro
4. Guarda token en BD con expiración
5. Envía email con enlace
6. Usuario hace clic en enlace
7. Ingresa nueva contraseña
8. Sistema valida token
9. Actualiza contraseña
10. Marca token como usado
```

### 🎨 Diseño UI/UX

**Paleta de Colores:**
- Primary: #3498db (Azul)
- Secondary: #2c3e50 (Gris oscuro)
- Success: #2ecc71 (Verde)
- Error: #e74c3c (Rojo)
- Background: #ecf0f1 (Gris claro)

**Características de Diseño:**
- Responsive (móvil, tablet, desktop)
- Cards con sombras suaves
- Transiciones CSS
- Formularios estilizados
- Mensajes flash con colores semánticos

### 📝 Validaciones Implementadas

**Email:**
- Formato RFC estándar
- Verificación de dominio
- Unicidad en base de datos

**Contraseña:**
- Longitud mínima: 8 caracteres
- Al menos una mayúscula [A-Z]
- Al menos una minúscula [a-z]
- Al menos un dígito [0-9]

**Nombre de Usuario:**
- Longitud mínima: 3 caracteres
- Unicidad en base de datos

### 🚀 Instalación y Despliegue

**Instalación Local:**
1. Ejecutar script de setup
2. Configurar MySQL
3. Crear archivo .env
4. Ejecutar aplicación

**Requisitos del Sistema:**
- Python 3.8+
- MySQL 5.7+
- 100MB espacio en disco
- 512MB RAM mínimo

### 📊 Métricas de Código

**Python (app.py):**
- Rutas: 9
- Funciones auxiliares: 4
- Líneas: ~350
- Decoradores: 2

**Templates:**
- Base template: 1
- Páginas: 6
- Líneas HTML total: ~400

**CSS:**
- Selectores: ~80
- Media queries: 1
- Líneas: ~200

### ✅ Testing y Validación

**Pruebas Incluidas:**
- Validación de sintaxis Python
- Validación de importaciones
- Pruebas de funciones de validación
- Pruebas de bcrypt
- Pruebas de generación de tokens
- Verificación de estructura de archivos

**Herramientas de Validación:**
- `validate.py` - Validación automática del sistema
- CodeQL - Análisis de seguridad
- GitHub Advisory Database - Vulnerabilidades

### 📚 Documentación

**README.md (Principal):**
- Descripción completa del proyecto
- Instrucciones de instalación
- Configuración detallada
- Solución de problemas
- Estructura del proyecto

**QUICKSTART.md:**
- Guía de inicio rápido
- Instalación en 5 minutos
- Comandos esenciales

**TESTING.md:**
- Casos de prueba detallados
- Pruebas manuales
- Verificación de seguridad
- Checklist de validación

### 🎓 Mejores Prácticas Implementadas

1. **Separación de Configuración:** Variables en config.py
2. **DRY (Don't Repeat Yourself):** Template base con herencia
3. **Seguridad por Defecto:** Todos los datos validados
4. **Principio de Mínimo Privilegio:** Acceso restringido
5. **Documentación Clara:** README, comentarios en código
6. **Gestión de Dependencias:** requirements.txt versionado
7. **Control de Versiones:** .gitignore apropiado
8. **Logging y Debugging:** Mensajes informativos

### 🔄 Ciclo de Vida de la Sesión

```
Login → Session Created → Session Active → Logout → Session Cleared
         │                 │                │
         └─────────────────┴────────────────┘
              Session Data Stored in Flask Session
```

### 💾 Esquema de Base de Datos

**Tabla: users**
- id (PK, AUTO_INCREMENT)
- username (UNIQUE, NOT NULL)
- email (UNIQUE, NOT NULL, INDEX)
- password (NOT NULL, hashed)
- created_at (TIMESTAMP)

**Tabla: password_reset_tokens**
- id (PK, AUTO_INCREMENT)
- user_id (FK → users.id)
- token (UNIQUE, NOT NULL, INDEX)
- created_at (TIMESTAMP)
- expires_at (TIMESTAMP)
- used (BOOLEAN)

### 🌟 Destacados del Proyecto

✨ **Sistema Completo:** Todas las funcionalidades de gestión de usuarios
🔐 **Seguridad Robusta:** Múltiples capas de protección
🎨 **Diseño Profesional:** UI moderna y responsive
📖 **Documentación Exhaustiva:** Guías completas
🚀 **Fácil Instalación:** Scripts automáticos
✅ **Código Limpio:** Siguiendo mejores prácticas
🧪 **Validado:** Sin vulnerabilidades conocidas

### 🎯 Casos de Uso

Este sistema es ideal para:
- Aplicaciones web que requieren autenticación
- Proyectos educativos de Flask
- Base para sistemas más complejos
- Prototipos rápidos con autenticación
- Aprendizaje de mejores prácticas de seguridad

### 📞 Soporte y Contribución

- **Issues:** GitHub Issues
- **Pull Requests:** Bienvenidos
- **Documentación:** Ver archivos .md
- **Validación:** Ejecutar `python validate.py`

---

**Versión:** 1.0.0  
**Fecha:** Diciembre 2024  
**Autor:** Andrés Rubio  
**Licencia:** MIT
