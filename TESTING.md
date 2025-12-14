# Guía de Pruebas del Sistema de Usuarios Flask

Esta guía describe cómo probar manualmente todas las funcionalidades del sistema.

## Requisitos Previos

1. MySQL instalado y ejecutándose
2. Base de datos creada (ejecutar `database.sql`)
3. Archivo `.env` configurado con credenciales correctas
4. Dependencias instaladas (`pip install -r requirements.txt`)

## Iniciar la Aplicación

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Ejecutar aplicación
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## Pruebas Manuales

### 1. Página de Inicio
- **URL:** http://localhost:5000
- **Verificar:**
  - ✓ La página carga correctamente
  - ✓ Se muestra el menú de navegación
  - ✓ Se muestran las 4 tarjetas de características
  - ✓ Botones "Crear Cuenta" y "Iniciar Sesión" funcionan

### 2. Registro de Usuario

#### Test 2.1: Registro Exitoso
- **URL:** http://localhost:5000/register
- **Pasos:**
  1. Llenar el formulario con datos válidos:
     - Usuario: `testuser`
     - Email: `test@example.com`
     - Contraseña: `Test1234`
     - Confirmar: `Test1234`
  2. Hacer clic en "Registrarse"
- **Resultado esperado:**
  - ✓ Mensaje flash de éxito: "¡Registro exitoso! Ahora puedes iniciar sesión."
  - ✓ Redirige a la página de login

#### Test 2.2: Validación de Email
- **Pasos:**
  1. Intentar registrar con email inválido: `invalid-email`
- **Resultado esperado:**
  - ✗ Mensaje de error: "El formato del email no es válido."

#### Test 2.3: Validación de Contraseña
- **Pasos:**
  1. Intentar registrar con contraseña débil: `weak`
- **Resultado esperado:**
  - ✗ Mensaje de error: "La contraseña debe tener al menos 8 caracteres."

- **Pasos:**
  2. Intentar registrar con contraseña sin mayúsculas: `lowercase123`
- **Resultado esperado:**
  - ✗ Mensaje de error: "La contraseña debe contener al menos una letra mayúscula."

- **Pasos:**
  3. Intentar registrar con contraseña sin minúsculas: `UPPERCASE123`
- **Resultado esperado:**
  - ✗ Mensaje de error: "La contraseña debe contener al menos una letra minúscula."

- **Pasos:**
  4. Intentar registrar con contraseña sin números: `NoNumbers`
- **Resultado esperado:**
  - ✗ Mensaje de error: "La contraseña debe contener al menos un número."

#### Test 2.4: Contraseñas No Coinciden
- **Pasos:**
  1. Ingresar contraseña: `Test1234`
  2. Confirmar con: `Test4321`
- **Resultado esperado:**
  - ✗ Mensaje de error: "Las contraseñas no coinciden."

#### Test 2.5: Email Duplicado
- **Pasos:**
  1. Intentar registrar con un email ya existente
- **Resultado esperado:**
  - ✗ Mensaje de error: "El email o nombre de usuario ya está registrado."

### 3. Inicio de Sesión

#### Test 3.1: Login Exitoso
- **URL:** http://localhost:5000/login
- **Pasos:**
  1. Ingresar credenciales correctas:
     - Email: `test@example.com`
     - Contraseña: `Test1234`
  2. Hacer clic en "Iniciar Sesión"
- **Resultado esperado:**
  - ✓ Mensaje flash: "¡Bienvenido, testuser!"
  - ✓ Redirige al dashboard
  - ✓ Menú muestra "Dashboard" y "Cerrar Sesión"

#### Test 3.2: Login con Credenciales Incorrectas
- **Pasos:**
  1. Ingresar contraseña incorrecta
- **Resultado esperado:**
  - ✗ Mensaje de error: "Email o contraseña incorrectos."
  - ✗ No se inicia sesión

### 4. Dashboard (Área Privada)

#### Test 4.1: Acceso Autenticado
- **URL:** http://localhost:5000/dashboard
- **Requisito:** Usuario debe estar logueado
- **Verificar:**
  - ✓ Muestra nombre de usuario en el título
  - ✓ Muestra información del usuario (username y email)
  - ✓ Muestra las características de seguridad
  - ✓ Botón "Cerrar Sesión" funciona

#### Test 4.2: Acceso No Autenticado
- **Pasos:**
  1. Cerrar sesión o usar ventana privada
  2. Intentar acceder a http://localhost:5000/dashboard
- **Resultado esperado:**
  - ✗ Mensaje: "Por favor inicia sesión para acceder a esta página."
  - ✓ Redirige a la página de login

### 5. Cierre de Sesión

#### Test 5.1: Logout
- **URL:** http://localhost:5000/logout
- **Requisito:** Usuario debe estar logueado
- **Pasos:**
  1. Hacer clic en "Cerrar Sesión"
- **Resultado esperado:**
  - ✓ Mensaje: "Hasta pronto, testuser!"
  - ✓ Redirige a la página de inicio
  - ✓ Menú muestra "Iniciar Sesión" y "Registrarse"
  - ✓ No se puede acceder al dashboard

### 6. Recuperación de Contraseña

#### Test 6.1: Solicitar Recuperación
- **URL:** http://localhost:5000/forgot-password
- **Pasos:**
  1. Ingresar email registrado: `test@example.com`
  2. Hacer clic en "Enviar Instrucciones"
- **Resultado esperado:**
  - ✓ Mensaje: "Se ha enviado un email con instrucciones..."
  - ✓ Se envía email con token (verificar en bandeja de entrada)
  - ✓ Redirige a la página de login

#### Test 6.2: Restablecer Contraseña con Token
- **URL:** http://localhost:5000/reset-password/<token>
- **Requisito:** Token válido del email
- **Pasos:**
  1. Hacer clic en el enlace del email
  2. Ingresar nueva contraseña: `NewPass123`
  3. Confirmar contraseña: `NewPass123`
  4. Hacer clic en "Actualizar Contraseña"
- **Resultado esperado:**
  - ✓ Mensaje: "¡Contraseña actualizada exitosamente!"
  - ✓ Redirige a login
  - ✓ Puede iniciar sesión con la nueva contraseña

#### Test 6.3: Token Inválido o Expirado
- **Pasos:**
  1. Intentar usar un token ya utilizado o expirado
- **Resultado esperado:**
  - ✗ Mensaje: "El enlace de recuperación es inválido o ha expirado."
  - ✓ Redirige a página de solicitud de recuperación

### 7. Seguridad

#### Test 7.1: Protección de Contraseñas
- **Verificar en la base de datos:**
  ```sql
  SELECT password FROM users LIMIT 1;
  ```
- **Resultado esperado:**
  - ✓ La contraseña está hasheada (no es texto plano)
  - ✓ Comienza con `$2b$` (bcrypt)

#### Test 7.2: Variables de Entorno
- **Verificar:**
  - ✓ Archivo `.env` no está en el repositorio (está en `.gitignore`)
  - ✓ Las credenciales están en `.env`, no en el código

#### Test 7.3: Validación de Sesión
- **Pasos:**
  1. Abrir consola del navegador
  2. Ejecutar: `document.cookie`
- **Verificar:**
  - ✓ La cookie de sesión está presente
  - ✓ Es una cookie HttpOnly (no accesible desde JavaScript)

## Pruebas de Interfaz

### Test de Diseño Responsive
- **Pasos:**
  1. Abrir la aplicación en diferentes tamaños de pantalla:
     - Desktop (1920x1080)
     - Tablet (768x1024)
     - Mobile (375x667)
- **Verificar:**
  - ✓ El diseño se adapta correctamente
  - ✓ El menú de navegación es usable
  - ✓ Los formularios son accesibles

### Test de Mensajes Flash
- **Verificar en diferentes acciones:**
  - ✓ Los mensajes aparecen en la parte superior
  - ✓ Los mensajes de éxito son verdes
  - ✓ Los mensajes de error son rojos
  - ✓ Los mensajes son legibles y claros

## Casos de Prueba SQL

Para verificar la integridad de la base de datos:

```sql
-- Verificar que los usuarios se crean correctamente
SELECT id, username, email, created_at FROM users;

-- Verificar índices para optimización
SHOW INDEX FROM users;

-- Verificar tokens de recuperación
SELECT id, user_id, token, created_at, expires_at, used 
FROM password_reset_tokens;

-- Verificar que las contraseñas están hasheadas
SELECT LENGTH(password) as password_length FROM users LIMIT 1;
-- Debe ser > 50 caracteres (bcrypt hash)
```

## Checklist de Validación Final

Antes de considerar el sistema completamente funcional, verificar:

- [ ] Todos los formularios validan correctamente
- [ ] Los mensajes flash se muestran apropiadamente
- [ ] El sistema de autenticación funciona
- [ ] Las contraseñas están hasheadas
- [ ] El dashboard es accesible solo para usuarios autenticados
- [ ] La recuperación de contraseña funciona
- [ ] Los emails se envían correctamente
- [ ] El diseño es responsive
- [ ] No hay errores en la consola del navegador
- [ ] No hay errores en los logs del servidor
- [ ] Las variables sensibles están en `.env`
- [ ] La base de datos tiene los índices correctos

## Solución de Problemas Comunes

### Error de Conexión a MySQL
```
Error: Can't connect to MySQL server
Solución: Verificar que MySQL está ejecutándose y las credenciales en .env son correctas
```

### Error al Enviar Email
```
Error: SMTPAuthenticationError
Solución: Verificar credenciales SMTP en .env. Para Gmail, usar contraseña de aplicación
```

### Error: Module not found
```
Error: ModuleNotFoundError: No module named 'flask'
Solución: Activar el entorno virtual e instalar dependencias
```

## Conclusión

Este sistema implementa un flujo completo de gestión de usuarios con todas las mejores prácticas de seguridad. Cada característica ha sido diseñada para ser robusta, segura y fácil de usar.
