import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :id GROUP BY symbol HAVING total_shares > 0", id=user_id)

    holdings = []
    total = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        total_value = quote["price"] * stock["total_shares"]
        total += total_value
        holdings.append({
            "symbol": stock["symbol"],
            "shares": stock["total_shares"],
            "price": quote["price"],
            "total": total_value
        })

    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)[0]["cash"]
    grand_total = cash + total

    return render_template("index.html", holdings=holdings, cash=cash, total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("missing symbol or shares")

        if not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be positive integer")

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")

        shares = int(shares)
        user_id = session["user_id"]
        price = stock["price"]
        total_cost = price * shares

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)[0]["cash"]
        if cash < total_cost:
            return apology("can't afford")

        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id",
                   cost=total_cost, id=user_id)

        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, type)
            VALUES (:user_id, :symbol, :shares, :price, 'BUY')
        """, user_id=user_id, symbol=stock["symbol"], shares=shares, price=price)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, shares, price, type, timestamp FROM transactions WHERE user_id = :id ORDER BY timestamp DESC", id=user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if password != confirmation:
            return apology("passwords do not match")

        hash_pw = generate_password_hash(password)

        # Check for duplicate username
        existing = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if existing:
            return apology("username already taken")

        # Insert new user
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=username, hash=hash_pw)

        # Get the new user's id
        rows = db.execute("SELECT id FROM users WHERE username = :username", username=username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("missing symbol or shares")

        if not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be positive integer")

        shares = int(shares)
        owned = db.execute("SELECT SUM(shares) as total FROM transactions WHERE user_id = :id AND symbol = :symbol",
                           id=user_id, symbol=symbol)[0]["total"]

        if owned is None or owned < shares:
            return apology("too many shares")

        price = lookup(symbol)["price"]
        revenue = price * shares

        db.execute("UPDATE users SET cash = cash + :revenue WHERE id = :id",
                   revenue=revenue, id=user_id)

        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, type)
            VALUES (:user_id, :symbol, :shares, :price, 'SELL')
        """, user_id=user_id, symbol=symbol, shares=-shares, price=price)

        return redirect("/")
    else:
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols])
