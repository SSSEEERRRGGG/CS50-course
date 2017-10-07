from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
                                                                        # configure application
app = Flask(__name__)
                                                                        # ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
                                                                        # custom filter
app.jinja_env.filters["usd"] = usd
                                                                        # configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
                                                                        # configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
                                                                        # select each symbol owned by the user and it's amount
    portfolio_symbols = db.execute("SELECT shares, symbol FROM portfolio WHERE id=:id", id=session["user_id"])

    total_cash = 0                                                      # create a temporary variable to store TOTAL worth ( cash + share)

    for portfolio_symbol in portfolio_symbols:                          # update each symbol prices and total
        symbol = portfolio_symbol["symbol"]
        shares = portfolio_symbol["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        total_cash += total
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol", \
                    price=usd(stock["price"]), total=usd(total), id=session["user_id"], symbol=symbol)
                                                                        # update user's cash in portfolio
    updated_cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    total_cash += updated_cash[0]["cash"]                               # update total cash -> cash + shares worth
                                                                        # print portfolio in index homepage
    updated_portfolio = db.execute("SELECT * from portfolio WHERE id=:id", id=session["user_id"])

    return render_template("index.html", stocks=updated_portfolio, cash=usd(updated_cash[0]["cash"]), total= usd(total_cash) )

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stock = lookup(request.form.get("symbol"))                      # ensure proper symbol
        if not stock:
            return apology("Invalid Symbol")

        try:                                                            # ensure proper number of shares
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")
                                                                        # select user's cash
        money = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
                                                                        # check if enough money to buy
        if not money or float(money[0]["cash"]) < stock["price"] * shares:
            return apology("Not enough money")
                                                                        # update history
        db.execute("INSERT INTO histories (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)", \
                    symbol=stock["symbol"], shares=shares, price=usd(stock["price"]), id=session["user_id"])
                                                                        # update user cash
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", \
                    id=session["user_id"], purchase=stock["price"] * float(shares))
                                                                        # Select user shares of that symbol
        user_shares = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol", \
                           id=session["user_id"], symbol=stock["symbol"])
                                                                        # if user doesn't has shares of that symbol, create new stock object
        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) \
                        VALUES(:name, :shares, :price, :total, :symbol, :id)", \
                        name=stock["name"], shares=shares, price=usd(stock["price"]), \
                        total=usd(shares * stock["price"]), symbol=stock["symbol"], id=session["user_id"])

        else:                                                           # Else increment the shares count
            shares_total = user_shares[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", \
                        shares=shares_total, id=session["user_id"], symbol=stock["symbol"])

                                                                        # return to index
        return redirect(url_for("index"))

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    histories = db.execute("SELECT * from histories WHERE id=:id", id=session["user_id"])
    return render_template("history.html", histories=histories)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()                                                     # forget any user_id

    if request.method == "POST":                                        # if user reached route via POST (as by submitting a form via POST)

        if not request.form.get("username"):                            # ensure username was submitted
            return apology("must provide username")

        elif not request.form.get("password"):                          # ensure password was submitted
            return apology("must provide password")
                                                                        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
                                                                        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        session["user_id"] = rows[0]["id"]                              # remember which user has logged in

        return redirect(url_for("index"))                               # redirect user to home page

    else:                                                               # else if user reached route via GET (as by clicking a link or via redirect)
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""
    session.clear()                                                     # forget any user_id
    return redirect(url_for("login"))                                   # redirect user to login form

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))

        if not rows:
            return apology("Invalid Symbol")

        return render_template("quotedalready.html", stock=rows)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":

        if not request.form.get("username"):                            # ensure username was submitted
            return apology("Must provide username")

        elif not request.form.get("password"):                          # ensure password was submitted
            return apology("Must provide password")
                                                                        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("passwordagain"):
            return apology("password doesn't match")
                                                                        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
                             username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

        if not result:
            return apology("Username already exist")

        session["user_id"] = result                                     # remember which user has logged in

        return redirect(url_for("index"))                               # redirect user to home page

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        stock = lookup(request.form.get("symbol"))                      # ensure proper symbol
        if not stock:
            return apology("Invalid Symbol")

        try:                                                            # ensure proper number of shares
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")
                                                                        # select the symbol shares of that user
        user_shares = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol", \
                                 id=session["user_id"], symbol=stock["symbol"])
                                                                        # check if enough shares to sell
        if not user_shares or int(user_shares[0]["shares"]) < shares:
            return apology("Not enough shares")
                                                                        # update history of a sell
        db.execute("INSERT INTO histories (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)", \
                    symbol=stock["symbol"], shares=-shares, price=usd(stock["price"]), id=session["user_id"])
                                                                        # update user cash (increase)
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id", \
                    id=session["user_id"], purchase=stock["price"] * float(shares))

        shares_total = user_shares[0]["shares"] - shares                # decrement the shares count

        if shares_total == 0:                                           # if after decrement is zero, delete shares from portfolio
            db.execute("DELETE FROM portfolio WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], symbol=stock["symbol"])
        else:                                                           # otherwise, update portfolio shares count
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", \
                    shares=shares_total, id=session["user_id"], symbol=stock["symbol"])

        return redirect(url_for("index"))                               # return to index