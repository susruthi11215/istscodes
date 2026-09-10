from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)


# -----------------------------------
# Create Database and Table
# -----------------------------------

def create_database():

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


# -----------------------------------
# Home Page
# -----------------------------------

@app.route("/")
def home():

    return render_template("register2.html")


# -----------------------------------
# Registration Path
# -----------------------------------

@app.route("/register", methods=["POST"])
def register():

    fullname = request.form["fullname"]
    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (fullname, username, password)
            VALUES (?, ?, ?)
        """, (fullname, username, password))

        connection.commit()

    except sqlite3.IntegrityError:

        connection.close()

        return "Username already exists!"

    connection.close()

    return redirect("/login")


# -----------------------------------
# Login Page
# -----------------------------------

@app.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")


# -----------------------------------
# Login Path
# -----------------------------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    connection.close()

    if user:

        return "<h2>Login successful!</h2><p>Welcome, " + username + "!</p>"

    else:

        return "<h2>Login failed!</h2><p>Username or password is incorrect.</p>"


# -----------------------------------
# Start Server
# -----------------------------------

if __name__ == "__main__":

    create_database()

    app.run(debug=True)