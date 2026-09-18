from flask import Flask, request, redirect, render_template, make_response, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# =========================================
# FLASK APPLICATION
# =========================================

app = Flask(__name__)

app.secret_key = "employee-management-secret-key"


# =========================================
# DATABASE CONNECTION
# =========================================

def get_database_connection():

    connection = sqlite3.connect("users.db")

    connection.row_factory = sqlite3.Row

    return connection


# =========================================
# CREATE DATABASE
# =========================================

def create_database():

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    # =====================================
    # USERS TABLE
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # =====================================
    # EMPLOYEES TABLE
    # =====================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL,
            joining_date TEXT NOT NULL,
            address TEXT
        )
    """)

    connection.commit()

    connection.close()

    print("=================================")
    print("Database ready")
    print("=================================")


# =========================================
# LOGIN CHECK
# =========================================

def login_required():

    return "user_id" in session


# =========================================
# THEME
# =========================================

@app.route("/set-theme/<theme>")
def set_theme(theme):

    if theme not in ["light", "dark"]:
        theme = "light"

    previous_page = request.referrer or "/"

    response = make_response(
        redirect(previous_page)
    )

    response.set_cookie(
        "theme",
        theme,
        max_age=60 * 60 * 24 * 365
    )

    return response


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    # User must login first

    if not login_required():
        return redirect("/login")

    theme = request.cookies.get(
        "theme",
        "light"
    )

    username = session.get("username")

    fullname = session.get("fullname")

    return render_template(
        "navbar.html",
        theme=theme,
        username=username,
        fullname=fullname
    )


# =========================================
# REGISTER PAGE
# =========================================

@app.route("/register", methods=["GET"])
def register_page():

    theme = request.cookies.get(
        "theme",
        "light"
    )

    return render_template(
        "register2.html",
        theme=theme
    )


# =========================================
# REGISTER USER
# =========================================

@app.route("/register", methods=["POST"])
def register():

    fullname = request.form.get(
        "fullname",
        ""
    ).strip()

    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    # =====================================
    # VALIDATION
    # =====================================

    if not fullname:

        return render_template(
            "register2.html",
            theme=request.cookies.get(
                "theme",
                "light"
            ),
            error="Full name is required."
        )

    if not username:

        return render_template(
            "register2.html",
            theme=request.cookies.get(
                "theme",
                "light"
            ),
            error="Username is required."
        )

    if not password:

        return render_template(
            "register2.html",
            theme=request.cookies.get(
                "theme",
                "light"
            ),
            error="Password is required."
        )

    # =====================================
    # HASH PASSWORD
    # =====================================

    hashed_password = generate_password_hash(
        password
    )

    # =====================================
    # INSERT USER
    # =====================================

    connection = get_database_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (
                fullname,
                username,
                password
            )
            VALUES (?, ?, ?)
        """,
        (
            fullname,
            username,
            hashed_password
        ))

        connection.commit()

    except sqlite3.IntegrityError:

        connection.close()

        return render_template(
            "register2.html",
            theme=request.cookies.get(
                "theme",
                "light"
            ),
            error="Username already exists."
        )

    connection.close()

    # Go to login page

    return redirect("/login")


# =========================================
# LOGIN PAGE
# =========================================

@app.route("/login", methods=["GET"])
def login_page():

    # If already logged in,
    # go directly to home

    if "user_id" in session:

        return redirect("/")

    theme = request.cookies.get(
        "theme",
        "light"
    )

    return render_template(
        "login.html",
        theme=theme
    )


# =========================================
# LOGIN USER
# =========================================

@app.route("/login", methods=["POST"])
def login():

    # =====================================
    # GET FORM VALUES
    # =====================================

    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    print("=================================")
    print("LOGIN ATTEMPT")
    print("Username:", username)
    print("=================================")

    # =====================================
    # VALIDATION
    # =====================================

    if not username or not password:

        return render_template(
            "login.html",
            theme=request.cookies.get(
                "theme",
                "light"
            ),
            error="Username and password are required."
        )

    # =====================================
    # FIND USER
    # =====================================

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            fullname,
            username,
            password
        FROM users
        WHERE username = ?
    """,
    (
        username,
    ))

    user = cursor.fetchone()

    connection.close()

    # =====================================
    # USER NOT FOUND
    # =====================================

    if user is None:

        print("User not found")

        return render_template(
            "login.html",
            theme=request.cookies.get(
                "theme",
                "light"
            ),
            error="Username or password is incorrect."
        )

    # =====================================
    # CHECK PASSWORD
    # =====================================

    password_correct = check_password_hash(
        user["password"],
        password
    )

    if not password_correct:

        print("Incorrect password")

        return render_template(
            "login.html",
            theme=request.cookies.get(
                "theme",
                "light"
            ),
            error="Username or password is incorrect."
        )

    # =====================================
    # LOGIN SUCCESS
    # =====================================

    print("Login successful!")
    print("User ID:", user["id"])
    print("Username:", user["username"])

    # Clear old session

    session.clear()

    # Store current user

    session["user_id"] = user["id"]

    session["username"] = user["username"]

    session["fullname"] = user["fullname"]

    # =====================================
    # REDIRECT TO HOME
    # =====================================

    return redirect("/")


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================
# ADD EMPLOYEE PAGE
# =========================================

@app.route("/add-employee", methods=["GET"])
def add_employee_page():

    if not login_required():

        return redirect("/login")

    theme = request.cookies.get(
        "theme",
        "light"
    )

    return render_template(
        "add-employee.html",
        theme=theme
    )


# =========================================
# ADD EMPLOYEE
# =========================================

@app.route("/add-employee", methods=["POST"])
def add_employee():

    if not login_required():

        return redirect("/login")

    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    department = request.form.get(
        "department",
        ""
    ).strip()

    salary = request.form.get(
        "salary",
        ""
    ).strip()

    joining_date = request.form.get(
        "joining_date",
        ""
    ).strip()

    address = request.form.get(
        "address",
        ""
    ).strip()

    if not name:
        return "Name is required!"

    if not email:
        return "Email is required!"

    if not phone:
        return "Phone is required!"

    if not department:
        return "Department is required!"

    if not salary:
        return "Salary is required!"

    if not joining_date:
        return "Joining date is required!"

    try:

        salary = int(salary)

    except ValueError:

        return "Salary must be a number!"

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO employees
        (
            name,
            email,
            phone,
            department,
            salary,
            joining_date,
            address
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        email,
        phone,
        department,
        salary,
        joining_date,
        address
    ))

    connection.commit()

    connection.close()

    return redirect("/employees")


# =========================================
# EMPLOYEES
# =========================================

@app.route("/employees")
def employees():

    if not login_required():

        return redirect("/login")

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        ORDER BY id DESC
    """)

    employees = cursor.fetchall()

    connection.close()

    theme = request.cookies.get(
        "theme",
        "light"
    )

    return render_template(
        "employees.html",
        employees=employees,
        theme=theme
    )


# =========================================
# SEARCH
# =========================================

@app.route("/search")
def search():

    if not login_required():

        return redirect("/login")

    search_text = request.args.get(
        "q",
        ""
    ).strip()

    connection = get_database_connection()

    cursor = connection.cursor()

    if search_text:

        search_value = f"%{search_text}%"

        cursor.execute("""
            SELECT *
            FROM employees
            WHERE
                name LIKE ?
                OR email LIKE ?
                OR phone LIKE ?
                OR department LIKE ?
            ORDER BY id DESC
        """,
        (
            search_value,
            search_value,
            search_value,
            search_value
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM employees
            ORDER BY id DESC
        """)

    employees = cursor.fetchall()

    connection.close()

    theme = request.cookies.get(
        "theme",
        "light"
    )

    return render_template(
        "employees.html",
        employees=employees,
        theme=theme,
        search_text=search_text
    )


# =========================================
# DELETE EMPLOYEE
# =========================================

@app.route("/delete-employee/<int:id>")
def delete_employee(id):

    if not login_required():

        return redirect("/login")

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = ?
    """,
    (
        id,
    ))

    connection.commit()

    connection.close()

    return redirect("/employees")


# =========================================
# EDIT EMPLOYEE PAGE
# =========================================

@app.route("/edit-employee/<int:id>")
def edit_employee_page(id):

    if not login_required():

        return redirect("/login")

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE id = ?
    """,
    (
        id,
    ))

    employee = cursor.fetchone()

    connection.close()

    if employee is None:

        return """
        <h2>Employee not found!</h2>

        <a href="/employees">
            Back to Employees
        </a>
        """

    theme = request.cookies.get(
        "theme",
        "light"
    )

    return render_template(
        "edit-employee.html",
        employee=employee,
        theme=theme
    )


# =========================================
# EDIT EMPLOYEE
# =========================================

@app.route(
    "/edit-employee/<int:id>",
    methods=["POST"]
)
def edit_employee(id):

    if not login_required():

        return redirect("/login")

    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    department = request.form.get(
        "department",
        ""
    ).strip()

    salary = request.form.get(
        "salary",
        ""
    ).strip()

    joining_date = request.form.get(
        "joining_date",
        ""
    ).strip()

    address = request.form.get(
        "address",
        ""
    ).strip()

    if not name:
        return "Name is required!"

    if not email:
        return "Email is required!"

    if not phone:
        return "Phone is required!"

    if not department:
        return "Department is required!"

    if not salary:
        return "Salary is required!"

    if not joining_date:
        return "Joining date is required!"

    try:

        salary = int(salary)

    except ValueError:

        return "Salary must be a number!"

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE employees
        SET
            name = ?,
            email = ?,
            phone = ?,
            department = ?,
            salary = ?,
            joining_date = ?,
            address = ?
        WHERE id = ?
    """,
    (
        name,
        email,
        phone,
        department,
        salary,
        joining_date,
        address,
        id
    ))

    connection.commit()

    connection.close()

    return redirect("/employees")


# =========================================
# START APPLICATION
# =========================================

if __name__ == "__main__":

    create_database()

    app.run(
        debug=True
    )

