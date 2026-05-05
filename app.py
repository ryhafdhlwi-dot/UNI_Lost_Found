from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "uni_lost_found_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        gate = request.form["gate"]
        image = request.files["image"]

        image_name = image.filename
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
        image.save(image_path)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                gate TEXT NOT NULL,
                image TEXT NOT NULL
            )
        """)

        cursor.execute("""
            INSERT INTO reports (category, description, gate, image)
            VALUES (?, ?, ?, ?)
        """, (category, description, gate, image_name))

        conn.commit()
        conn.close()

        return redirect("/database")

    return render_template("report.html")


@app.route("/database")
def database():
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            gate TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT * FROM reports ORDER BY id DESC")
    reports = cursor.fetchall()

    conn.close()

    return render_template("database.html", reports=reports)


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    keyword = ""

    if request.method == "POST":
        keyword = request.form["keyword"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM reports
            WHERE category LIKE ?
            OR description LIKE ?
            OR gate LIKE ?
            ORDER BY id DESC
        """, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

        results = cursor.fetchall()
        conn.close()

    return render_template("search.html", results=results, keyword=keyword)


@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE category='Electronics'")
    electronics = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE category='Cards'")
    cards = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE category='Books'")
    books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE category='Personal'")
    personal = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE category='Other'")
    other = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        electronics=electronics,
        cards=cards,
        books=books,
        personal=personal,
        other=other
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin"] = username
            return redirect("/dashboard")
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)