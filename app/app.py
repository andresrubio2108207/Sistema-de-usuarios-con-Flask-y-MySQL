from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re

from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

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
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            flash("El usuario no existe", "danger")
            return redirect(url_for("login"))

        if not check_password_hash(user["password"], password):
            flash("Contraseña incorrecta", "danger")
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

        if not username or not email or not password:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("La contraseña debe tener mínimo 8 caracteres", "danger")
            return redirect(url_for("register"))

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            flash("Email inválido", "danger")
            return redirect(url_for("register"))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            flash("El correo ya está registrado", "warning")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
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

@app.route("/forgetpass")
def forgetpass():
    return render_template("forgetpass.html")

@app.route("/test-db")
def test_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DATABASE()")
    db = cursor.fetchone()
    cursor.close()
    return f"Conectado a la BD: {db}"

if __name__ == "__main__":
    app.run(debug=True)
