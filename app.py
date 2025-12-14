from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import bcrypt
import re
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from config import Config
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
mysql = MySQL(app)
mail = Mail(app)

# Serializer for generating secure tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula."
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número."
    return True, ""


def send_password_reset_email(email, token):
    """Send password reset email"""
    try:
        reset_url = url_for('reset_password', token=token, _external=True)
        msg = Message(
            'Recuperación de Contraseña',
            recipients=[email]
        )
        msg.body = f'''Hola,

Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para continuar:

{reset_url}

Este enlace es válido por 1 hora.

Si no solicitaste este cambio, ignora este correo.

Saludos,
El equipo de Flask User System
'''
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('El nombre de usuario debe tener al menos 3 caracteres.', 'error')
            return render_template('register.html')
        
        if not validate_email(email):
            flash('El formato del email no es válido.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')
        
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('register.html')
        
        # Check if user already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash('El email o nombre de usuario ya está registrado.', 'error')
            cur.close()
            return render_template('register.html')
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert user
        try:
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            mysql.connection.commit()
            cur.close()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            cur.close()
            flash('Error al registrar el usuario. Por favor intenta de nuevo.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email y contraseña son obligatorios.', 'error')
            return render_template('login.html')
        
        # Get user from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Login successful
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            flash(f'¡Bienvenido, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard (private)"""
    return render_template('dashboard.html', username=session.get('username'))


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    username = session.get('username')
    session.clear()
    flash(f'Hasta pronto, {username}!', 'success')
    return redirect(url_for('index'))


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Request password reset"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Por favor ingresa tu email.', 'error')
            return render_template('forgot_password.html')
        
        # Check if user exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if user:
            # Generate secure token
            token = serializer.dumps(email, salt='password-reset-salt')
            
            # Store token in database
            expires_at = datetime.now() + timedelta(hours=1)
            try:
                cur.execute(
                    "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
                    (user['id'], token, expires_at)
                )
                mysql.connection.commit()
                
                # Send email
                if send_password_reset_email(email, token):
                    flash('Se ha enviado un email con instrucciones para restablecer tu contraseña.', 'success')
                else:
                    flash('Error al enviar el email. Por favor verifica la configuración del servidor de correo.', 'error')
            except Exception as e:
                mysql.connection.rollback()
                flash('Error al procesar la solicitud. Por favor intenta de nuevo.', 'error')
        else:
            # Don't reveal if email exists or not (security best practice)
            flash('Si el email existe en nuestra base de datos, recibirás un correo con instrucciones.', 'success')
        
        cur.close()
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    try:
        # Verify token (expires after 1 hour)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        flash('El enlace de recuperación es inválido o ha expirado.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not password or not confirm_password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('reset_password.html', token=token)
        
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('reset_password.html', token=token)
        
        # Check if token is valid and not used
        cur = mysql.connection.cursor()
        cur.execute(
            """SELECT rt.id, rt.user_id, rt.used 
               FROM password_reset_tokens rt 
               WHERE rt.token = %s AND rt.expires_at > NOW() AND rt.used = FALSE""",
            (token,)
        )
        token_record = cur.fetchone()
        
        if not token_record:
            flash('El enlace de recuperación es inválido o ha expirado.', 'error')
            cur.close()
            return redirect(url_for('forgot_password'))
        
        # Hash new password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            # Update password
            cur.execute(
                "UPDATE users SET password = %s WHERE id = %s",
                (hashed_password, token_record['user_id'])
            )
            # Mark token as used
            cur.execute(
                "UPDATE password_reset_tokens SET used = TRUE WHERE id = %s",
                (token_record['id'],)
            )
            mysql.connection.commit()
            cur.close()
            flash('¡Contraseña actualizada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            cur.close()
            flash('Error al actualizar la contraseña. Por favor intenta de nuevo.', 'error')
            return render_template('reset_password.html', token=token)
    
    return render_template('reset_password.html', token=token)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
