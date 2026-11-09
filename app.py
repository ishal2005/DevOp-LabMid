
from flask import Flask, render_template, request, redirect, flash
from urllib.parse import urlparse
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-dev-key")

DB_PATH = os.environ.get("DB_PATH", "submissions.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reg_no TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL
            )
        """)


def valid_url(url):
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and "." in parsed.hostname
            and not any(c.isspace() for c in url)
        )
    except ValueError:
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        reg_no = request.form.get("reg_no", "").strip()
        title = request.form.get("title", "").strip()
        url = request.form.get("url", "").strip()

        if not all([name, title, url]):
            flash("All fields are required!", "error")

        elif not valid_url(url):
            flash("Invalid submission URL!", "error")

        else:
            with get_db() as conn:
                conn.execute(
                    """INSERT INTO submissions
                    (name, reg_no, title, url)
                    VALUES (?, ?, ?, ?)""",
                    (name, reg_no, title, url)
                )

            flash("Assignment submitted successfully!", "success")
            return redirect("/")

    with get_db() as conn:
        submissions = conn.execute(
            "SELECT * FROM submissions ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "index.html",
        submissions=submissions
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
