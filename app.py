
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key
app.secret_key = os.environ.get("SECRET_KEY")

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
       password=os.environ.get("MYSQLPASSWORD", ""),
        database="auth_db",
        port=3306
        
    )

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Registration
@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        flash("Email already registered!")
        return redirect(url_for("home"))

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hashed_password)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Registration successful! You can now login.")

    return redirect(url_for("home"))


# Login
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user["password"], password):

        return f"""
        <h1>Welcome, {user['name']}!</h1>
        <p>Login successful.</p>
        <a href="/">Logout</a>
        """

    else:
        flash("Invalid email or password!")
        return redirect(url_for("home"))


# Run application locally
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 9000)),
        debug=False
    )
