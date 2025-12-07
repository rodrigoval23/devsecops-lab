import sqlite3
import socket
import datetime

# --- Crear base de datos y tablas ---
def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Tabla de inicios de sesión correctos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            login_time TEXT NOT NULL,
            hostname TEXT,
            ip_local TEXT
        )
    ''')

    # Tabla de intentos fallidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS failed_logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            attempt_time TEXT NOT NULL,
            hostname TEXT,
            ip_local TEXT
        )
    ''')

    # Crear usuario por defecto
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '1234'))

    conn.commit()
    conn.close()


# --- Verificar usuario ---
def check_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    conn.close()
    return result


# --- Guardar login exitoso ---
def save_login(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('INSERT INTO logins (username, login_time, hostname, ip_local) VALUES (?, ?, ?, ?)',
                   (username, time_now, hostname, ip_local))

    conn.commit()
    conn.close()


# --- Guardar intento fallido ---
def save_failed_login(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('INSERT INTO failed_logins (username, attempt_time, hostname, ip_local) VALUES (?, ?, ?, ?)',
                   (username, time_now, hostname, ip_local))

    conn.commit()
    conn.close()