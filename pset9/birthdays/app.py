import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        # Get form data
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validate input
        if not name or not month or not day:
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            return redirect("/")

        if not (1 <= month <= 12) or not (1 <= day <= 31):
            return redirect("/")

        # Insert the user's entry into the database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        # Redirect to homepage after adding entry
        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        # Query all birthdays from the database
        birthdays = db.execute("SELECT * FROM birthdays")

        # Pass birthdays to the template for rendering
        return render_template("index.html", birthdays=birthdays)

