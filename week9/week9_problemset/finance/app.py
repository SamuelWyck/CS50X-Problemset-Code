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
    user_stocks = db.execute("SELECT stock_symbol, shares, price FROM user_stocks WHERE user_id = ?", session["user_id"])
    for stock in user_stocks:
        stock["price"] = lookup(stock["stock_symbol"])["price"]

    for stock in user_stocks:
        stock["total_value"] = float(stock["price"]) * float(stock["shares"])


    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = float(cash[0]["cash"])

    user_assets = {"cash": cash, "grand_total": float(cash)}
    for stock in user_stocks:
        user_assets["grand_total"] += float(stock["total_value"])

    user_assets["cash"], user_assets["grand_total"] = usd(user_assets["cash"]), usd(user_assets["grand_total"])
    for stock in user_stocks:
        stock["price"] = usd(stock["price"])
        stock["total_value"] = usd(stock["total_value"])

    return render_template("index.html", user_stocks=user_stocks, user_assets=user_assets)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        #user input checking
        symbol, shares = request.form.get("symbol"), request.form.get("shares")
        if not symbol:
            return apology("Missing stock symbol.")
        if not lookup(symbol):
            return apology("Invalid stock symbol.")
        try:
            shares = int(shares)
        except ValueError:
            return apology("Must enter a number for shares.")
        if shares <= 0:
            return apology("Must enter a positive number for shares")

        #check price against balance
        price = float(lookup(symbol)["price"]) * float(shares)
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        balance = int(balance[0]["cash"])
        if balance - price < 0:
            return apology("Cannot afford that number of shares.")
        new_balance = float(balance) - price

        stock_check = db.execute("SELECT shares, price FROM user_stocks WHERE stock_symbol = ? AND user_id = ?", symbol.upper(), session["user_id"])
        if not stock_check:
            db.execute("INSERT INTO user_stocks (user_id, stock_symbol, shares, price, timestamp) VALUES(?, ?, ?, ?, datetime())",
            session["user_id"], symbol.upper(), shares, price)

        else:
            new_shares = shares + int(stock_check[0]["shares"])
            new_price = price + float(stock_check[0]["price"])

            db.execute("UPDATE user_stocks SET shares = ? WHERE user_id = ? AND stock_symbol = ?", new_shares, session["user_id"], symbol.upper())
            db.execute("UPDATE user_stocks SET price = ? WHERE user_id = ? AND stock_symbol = ?", new_price, session["user_id"], symbol.upper())
            db.execute("UPDATE user_stocks SET timestamp = datetime() WHERE user_id = ? AND stock_symbol = ?", session["user_id"], symbol.upper())
                            #CREATE TABLE user_transactions (user_id INTEGER NOT NULL, type TEXT NOT NULL, stock_symbol TEXT NOT NULL,
                            # price REAL NOT NULL, shares TEXT NOT NULL, timestamp TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))
        db.execute("INSERT INTO user_transactions (user_id, type, stock_symbol, price, shares, timestamp) VALUES(?, 'purchase', ?, ?, ?, datetime())",
        session["user_id"], symbol.upper(), price, shares)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, session["user_id"])

    else:
        return render_template("buy.html")

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT type, stock_symbol, price, shares, timestamp FROM user_transactions WHERE user_id = ?", session["user_id"])

    for transaction in transactions:
        transaction["price"] = usd(transaction["price"])

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
            return apology("Missing stock symbol.")

        results = lookup(symbol)
        if not results:
            return apology("Invalid stock symbol.")
        results["price"] = usd(results["price"])

        return render_template("quoted.html", results=results)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username, password, confirmation = request.form.get("username"), request.form.get("password"), request.form.get("confirmation")

        if not username:
            return apology("Missing username.")
        if not password:
            return apology("Missing password.")
        if password != confirmation:
            return apology("Password and confirmation do not match.")

        password = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)
        except ValueError:
            return apology("Username already exists.")

    else:
        return render_template("register.html")

    return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol, shares = request.form.get("symbol"), request.form.get("shares")
        if not symbol:
            return apology("Missing stock symbol.")
        if not lookup(symbol):
            return apology("Stock symbol does not exist.")
        if not shares:
            return apology("Missing shares.")
        try:
            shares = int(shares)
        except ValueError:
            return apology("Shares must be a number.")
        if shares < 0:
            return apology("Shares must be a positive number.")

        user_stock = db.execute("SELECT shares, price FROM user_stocks WHERE user_id = ? AND stock_symbol = ?", session["user_id"], symbol.upper())
        if not user_stock:
            return apology("You do not own any shares of that stock")
        user_shares = int(user_stock[0]["shares"])
        user_price = float(user_stock[0]["price"])
        if user_shares < shares:
            return apology("You do not own that number of shares of that stock.")

        stock_price = lookup(symbol)["price"]
        stock_price = stock_price * float(shares)

        if user_shares - shares == 0:
            db.execute("DELETE FROM user_stocks WHERE stock_symbol = ? AND user_id = ?", symbol.upper(), session["user_id"])

        elif user_shares - shares > 0:
            user_shares = user_shares - shares
            user_price = user_price - stock_price

            db.execute("UPDATE user_stocks SET shares = ? WHERE stock_symbol = ? AND user_id = ?", user_shares, symbol.upper(), session["user_id"])
            db.execute("UPDATE user_stocks SET price = ? WHERE stock_symbol = ? AND user_id = ?", user_price, symbol.upper(), session["user_id"])
            db.execute("UPDATE user_stocks SET timestamp = datetime() WHERE user_id = ? AND stock_symbol = ?", session["user_id"], symbol.upper())


        db.execute("INSERT INTO user_transactions (user_id, type, stock_symbol, price, shares, timestamp) VALUES(?, 'sale', ?, ?, ?, datetime())",
        session["user_id"], symbol.upper(), stock_price, shares)

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = float(user_cash[0]["cash"])
        user_cash += stock_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, session["user_id"])

    else:
        stocks = db.execute("SELECT stock_symbol FROM user_stocks WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)

    return redirect("/")


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        cash_amount = request.form.get("deposit")
        if not cash_amount:
            return apology("Missing deposit amount.")
        try:
            cash_amount = float(cash_amount)
        except ValueError:
            return apology("Deposit amount must be a number.")
        if cash_amount < 0:
            return apology("Deposit amount must be a positive number.")

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = float(user_cash[0]["cash"])

        user_cash += cash_amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, session["user_id"])

    else:
        return render_template("deposit.html")

    return redirect("/")
