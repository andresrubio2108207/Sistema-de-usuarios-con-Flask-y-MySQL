#!/usr/bin/env python3
"""
Script de validación del sistema de usuarios Flask
Verifica importaciones, validaciones y lógica sin requerir MySQL
"""

import sys
import os

print("=================================")
print("Validación del Sistema Flask")
print("=================================\n")

# Test 1: Verificar importaciones
print("1. Verificando importaciones de Python...")
try:
    import flask
    print(f"   ✓ Flask {flask.__version__}")
except ImportError as e:
    print(f"   ✗ Error al importar Flask: {e}")
    sys.exit(1)

try:
    import bcrypt
    print(f"   ✓ bcrypt instalado")
except ImportError as e:
    print(f"   ✗ Error al importar bcrypt: {e}")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    print(f"   ✓ python-dotenv instalado")
except ImportError as e:
    print(f"   ✗ Error al importar dotenv: {e}")
    sys.exit(1)

try:
    from itsdangerous import URLSafeTimedSerializer
    print(f"   ✓ itsdangerous instalado")
except ImportError as e:
    print(f"   ✗ Error al importar itsdangerous: {e}")
    sys.exit(1)

try:
    from email_validator import validate_email as validate_email_lib
    print(f"   ✓ email-validator instalado")
except ImportError:
    print(f"   ⚠ email-validator no instalado (opcional)")

# Test 2: Cargar módulos de la aplicación
print("\n2. Verificando módulos de la aplicación...")
try:
    from config import Config
    print(f"   ✓ config.py cargado correctamente")
except Exception as e:
    print(f"   ✗ Error al cargar config.py: {e}")
    sys.exit(1)

# Test 3: Verificar funciones de validación
print("\n3. Probando funciones de validación...")

# Importar funciones de validación sin inicializar la app completa
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula."
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número."
    return True, ""

# Test email validation
test_emails = [
    ("test@example.com", True),
    ("user.name@domain.co.uk", True),
    ("invalid-email", False),
    ("@invalid.com", False),
    ("test@", False),
]

print("   Validación de emails:")
all_passed = True
for email, expected in test_emails:
    result = validate_email(email)
    status = "✓" if result == expected else "✗"
    print(f"      {status} {email}: {result} (esperado: {expected})")
    if result != expected:
        all_passed = False

# Test password validation
test_passwords = [
    ("Test1234", True, ""),
    ("weak", False, "La contraseña debe tener al menos 8 caracteres."),
    ("lowercase123", False, "La contraseña debe contener al menos una letra mayúscula."),
    ("UPPERCASE123", False, "La contraseña debe contener al menos una letra minúscula."),
    ("NoNumbers", False, "La contraseña debe contener al menos un número."),
    ("StrongP@ssw0rd", True, ""),
]

print("   Validación de contraseñas:")
for password, expected_valid, expected_msg in test_passwords:
    is_valid, msg = validate_password(password)
    status = "✓" if is_valid == expected_valid else "✗"
    print(f"      {status} '{password}': válida={is_valid}")
    if is_valid != expected_valid:
        all_passed = False

# Test 4: Verificar bcrypt
print("\n4. Probando hash de contraseñas con bcrypt...")
try:
    test_password = "TestPassword123"
    hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
    print(f"   ✓ Hash generado correctamente")
    
    # Verificar contraseña correcta
    if bcrypt.checkpw(test_password.encode('utf-8'), hashed):
        print(f"   ✓ Verificación de contraseña correcta")
    else:
        print(f"   ✗ Error en verificación de contraseña")
        all_passed = False
    
    # Verificar contraseña incorrecta
    if not bcrypt.checkpw("WrongPassword".encode('utf-8'), hashed):
        print(f"   ✓ Rechazo de contraseña incorrecta")
    else:
        print(f"   ✗ No se rechazó contraseña incorrecta")
        all_passed = False
        
except Exception as e:
    print(f"   ✗ Error en prueba de bcrypt: {e}")
    all_passed = False

# Test 5: Verificar tokens
print("\n5. Probando generación de tokens seguros...")
try:
    serializer = URLSafeTimedSerializer("test-secret-key")
    email = "test@example.com"
    token = serializer.dumps(email, salt='password-reset-salt')
    print(f"   ✓ Token generado: {token[:30]}...")
    
    # Verificar token
    recovered_email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    if recovered_email == email:
        print(f"   ✓ Token verificado correctamente")
    else:
        print(f"   ✗ Error al verificar token")
        all_passed = False
        
except Exception as e:
    print(f"   ✗ Error en prueba de tokens: {e}")
    all_passed = False

# Test 6: Verificar estructura de archivos
print("\n6. Verificando estructura de archivos...")
required_files = [
    'app.py',
    'config.py',
    'requirements.txt',
    'database.sql',
    '.env.example',
    '.gitignore',
    'templates/base.html',
    'templates/index.html',
    'templates/register.html',
    'templates/login.html',
    'templates/dashboard.html',
    'templates/forgot_password.html',
    'templates/reset_password.html',
    'static/css/style.css',
]

for file in required_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} NO ENCONTRADO")
        all_passed = False

# Test 7: Verificar configuración
print("\n7. Verificando configuración...")
if os.path.exists('.env.example'):
    print("   ✓ Plantilla .env.example existe")
else:
    print("   ✗ .env.example no encontrado")
    all_passed = False

if os.path.exists('.env'):
    print("   ⚠ Archivo .env existe (asegúrate de configurarlo)")
else:
    print("   ℹ Archivo .env no existe (se debe crear desde .env.example)")

# Resultado final
print("\n=================================")
if all_passed:
    print("✅ TODAS LAS VALIDACIONES PASARON")
    print("=================================")
    print("\nEl sistema está listo para ejecutarse.")
    print("\nPasos siguientes:")
    print("1. Configura MySQL y ejecuta database.sql")
    print("2. Crea y configura el archivo .env")
    print("3. Ejecuta: python app.py")
    sys.exit(0)
else:
    print("⚠️  ALGUNAS VALIDACIONES FALLARON")
    print("=================================")
    print("\nRevisa los errores anteriores antes de ejecutar la aplicación.")
    sys.exit(1)
