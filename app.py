from flask import Flask, render_template, request, redirect, session
import os
from werkzeug.utils import secure_filename

from database import (
    create_table,
    add_report,
    get_all_reports,
    search_reports,
    count_all_reports,
    count_by_category
)

app = Flask(__name__)
app.secret_key = "uni_lost_found_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

create_table()


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

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        image_name = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
        image.save(image_path)

        add_report(category, description, gate, image_name)

        return redirect("/database")

    return render_template("report.html")


@app.route("/database")
def database():
    if "admin" not in session:
        return redirect("/login")

    reports = get_all_reports()
    return render_template("database.html", reports=reports)


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    keyword = ""

    if request.method == "POST":
        keyword = request.form["keyword"]
        results = search_reports(keyword)

    return render_template("search.html", results=results, keyword=keyword)


@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/login")

    total = count_all_reports()
    electronics = count_by_category("Electronics")
    cards = count_by_category("Cards")
    books = count_by_category("Books")
    personal = count_by_category("Personal")
    other = count_by_category("Other")

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