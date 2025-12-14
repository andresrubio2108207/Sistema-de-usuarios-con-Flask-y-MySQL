from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os, re, secrets

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

# Configuración MySQL
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Configuración Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASS")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("EMAIL_USER")

mysql = MySQL(app)
mail = Mail(app)

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Rutas
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for("login"))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if not user or not check_password_hash(user["password"], password):
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for("login"))

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash(f"Bienvenido {user['username']}", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("La contraseña debe tener mínimo 8 caracteres", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for("register"))

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            flash("Email inválido", "danger")
            return redirect(url_for("register"))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            cursor.close()
            flash("El correo ya está registrado", "warning")
            return redirect(url_for("register"))

        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            cursor.close()
            flash("El nombre de usuario ya está en uso", "warning")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",
            (username, email, password_hash)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Registro exitoso, ahora inicia sesión", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("login"))

@app.route("/forgetpass", methods=["GET", "POST"])
def forgetpass():
    if request.method == "POST":
        email = request.form.get("email")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            flash("El correo no está registrado", "danger")
            return redirect(url_for("forgetpass"))

        token = secrets.token_urlsafe(16)
        cursor.execute("UPDATE users SET password_reset_token=%s WHERE email=%s", (token, email))
        mysql.connection.commit()
        cursor.close()

        reset_link = url_for("reset_password", token=token, _external=True)
        msg = Message(
            subject="Recuperar contraseña",
            recipients=[email],
            body=f"Hola {email}, haz clic en este enlace para cambiar tu contraseña:\n{reset_link}"
        )
        mail.send(msg)

        flash("Se envió un correo con instrucciones para cambiar la contraseña", "success")
        return redirect(url_for("login"))

    return render_template("forgetpass.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, email FROM users WHERE password_reset_token=%s", (token,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        flash("Token inválido o expirado", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not password or not confirm_password:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(request.url)

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(request.url)

        if len(password) < 8:
            flash("La contraseña debe tener mínimo 8 caracteres", "danger")
            return redirect(request.url)

        password_hash = generate_password_hash(password)
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE users SET password=%s, password_reset_token=NULL WHERE id=%s",
            (password_hash, user["id"])
        )
        mysql.connection.commit()
        cursor.close()

        flash("Contraseña cambiada correctamente", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html")

@app.route("/test-db")
def test_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DATABASE()")
    db = cursor.fetchone()
    cursor.close()
    return f"Conectado a la BD: {db}"

if __name__ == "__main__":
    app.run(debug=True)
