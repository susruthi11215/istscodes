from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)


# =========================================
# DATABASE CONNECTION
# =========================================

def get_database_connection():

    connection = sqlite3.connect("users.db")

    connection.row_factory = sqlite3.Row

    return connection


# =========================================
# CREATE DATABASE AND TABLES
# =========================================

def create_database():

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            fullname TEXT NOT NULL,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    # EMPLOYEES TABLE
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

    print("Database and tables created successfully!")


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return render_template("navbar.html")


# =========================================
# REGISTER PAGE
# =========================================

@app.route("/register", methods=["GET"])
def register_page():

    return render_template("register2.html")


# =========================================
# REGISTER
# =========================================

@app.route("/register", methods=["POST"])
def register():

    fullname = request.form["fullname"]

    username = request.form["username"]

    password = request.form["password"]

    connection = sqlite3.connect("users.db")

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
        """, (
            fullname,
            username,
            password
        ))

        connection.commit()

    except sqlite3.IntegrityError:

        connection.close()

        return """
        <h2>Username already exists!</h2>

        <br>

        <a href="/register">
            Try Again
        </a>
        """

    connection.close()

    return redirect("/login")


# =========================================
# LOGIN PAGE
# =========================================

@app.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")


# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]

    password = request.form["password"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        password
    ))

    user = cursor.fetchone()

    connection.close()

    if user:

        return """
        <h2>Login successful!</h2>

        <p>
            Welcome, """ + username + """!
        </p>

        <br>

        <a href="/">
            Go to Home
        </a>
        """

    else:

        return """
        <h2>Login failed!</h2>

        <p>
            Username or password is incorrect.
        </p>

        <br>

        <a href="/login">
            Try Again
        </a>
        """


# =========================================
# ADD EMPLOYEE PAGE
# =========================================

@app.route("/add-employee", methods=["GET"])
def add_employee_page():

    return render_template("add-employee.html")


# =========================================
# ADD EMPLOYEE
# =========================================

@app.route("/add-employee", methods=["POST"])
def add_employee():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    department = request.form.get("department")
    salary = request.form.get("salary")
    joining_date = request.form.get("joining_date")
    address = request.form.get("address")

    print("=================================")
    print("ADDING EMPLOYEE")
    print("Name:", name)
    print("Email:", email)
    print("Phone:", phone)
    print("Department:", department)
    print("Salary:", salary)
    print("Joining Date:", joining_date)
    print("Address:", address)
    print("=================================")

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    try:

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
        """, (
            name,
            email,
            phone,
            department,
            salary,
            joining_date,
            address
        ))

        connection.commit()

        print("Employee inserted successfully!")
        print("New Employee ID:", cursor.lastrowid)

    except sqlite3.Error as error:

        connection.rollback()

        print("Database Error:", error)

        connection.close()

        return f"""
        <h2>Error adding employee</h2>

        <p>{error}</p>

        <br>

        <a href="/add-employee">
            Go Back
        </a>
        """

    connection.close()

    return redirect("/employees")


# =========================================
# EMPLOYEES LIST
# =========================================

@app.route("/employees")
def employees():

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        ORDER BY id DESC
    """)

    employees = cursor.fetchall()

    connection.close()

    return render_template(
        "employees.html",
        employees=employees
    )


# =========================================
# DELETE EMPLOYEE
# =========================================

@app.route("/delete-employee/<int:id>")
def delete_employee(id):

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (id,))

    connection.commit()

    connection.close()

    return redirect("/employees")


# =========================================
# EDIT EMPLOYEE - DISPLAY FORM
# =========================================

@app.route("/edit-employee/<int:id>")
def edit_employee_page(id):

    connection = get_database_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE id = ?
    """, (id,))

    employee = cursor.fetchone()

    connection.close()

    if employee is None:

        return """
        <h2>Employee not found!</h2>

        <br>

        <a href="/employees">
            Back to Employees
        </a>
        """

    return render_template(
        "edit-employee.html",
        employee=employee
    )


# =========================================
# EDIT EMPLOYEE - UPDATE
# =========================================

@app.route("/edit-employee/<int:id>", methods=["POST"])
def edit_employee(id):

    name = request.form["name"]

    email = request.form["email"]

    phone = request.form["phone"]

    department = request.form["department"]

    salary = request.form["salary"]

    joining_date = request.form["joining_date"]

    address = request.form["address"]

    connection = sqlite3.connect("users.db")

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
    """, (
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
# START FLASK SERVER
# =========================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)

