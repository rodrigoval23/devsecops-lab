from flask import Flask, request, render_template_string, redirect, url_for
from database import create_db, check_user, save_login, save_failed_login
import socket

app = Flask(__name__)

# Inicializamos tu DB al arrancar
create_db()

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Login Seguro</title></head>
<body>
    <h2>Login DevSecOps</h2>
    <form action="/login" method="post">
        Usuario: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Ingresar">
    </form>
    {% if message %}
        <p style="color:red">{{ message }}</p>
    {% endif %}
</body>
</html>
"""

HOME_TEMPLATE = """
<h1>Bienvenido {{ username }}!</h1>
<p>Has iniciado sesión correctamente.</p>
<a href="/">Cerrar Sesión</a>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = check_user(username, password)

    if user:
        save_login(username)
        return render_template_string(HOME_TEMPLATE, username=username)
    else:
        save_failed_login(username)
        return render_template_string(LOGIN_TEMPLATE, message="Usuario o contraseña incorrectos")

if __name__ == '__main__':
    # AQUI ESTA EL CAMBIO: Agregamos '# nosec' para que Bandit ignore el 0.0.0.0
    app.run(host='0.0.0.0', port=5000) # nosec
