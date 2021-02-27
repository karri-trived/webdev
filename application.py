import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from cs50 import SQL
app = Flask(__name__)

#Ensurethat templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
# Configure session to use filesystem instead of signed cookies
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#connect to register database
db = SQL("sqlite:///register.db")

SPORTS = [
    "Dodgeball",
    "Flag Football",
    "Soccer",
    "Volleyball",
    "Basket Ball",
    "Cricket",
]

@app.route("/")
@login_required
def index():
    username=request.form.get("username")
    SPORt = db.execute("SELECT age FROM users WHERE username = username")
    AGe = db.execute("SELECT regsport FROM users WHERE username = username")
    return render_template("index.html",AGE=AGe,SPORT=SPORt,username=username)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]
        
        # Redirect user to home page
        username=request.form.get("username")
        AGe = db.execute("SELECT age FROM users WHERE username = ?",request.form.get("username"))
        SPORt = db.execute("SELECT regsport FROM users WHERE username = ?",request.form.get("username"))
        return render_template("index.html",AGE=AGe,SPORT=SPORt,username=username)

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

@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
            #Ensure age was submitted
        elif not request.form.get("Age"):
            return apology("must provide age",403)
            #Ensure email was submitted
        elif not request.form.get("e-mail"):
            return apology("must provide mail id",403)
        elif not request.form.get("sport"):
            return apology("must provide sport",403)
        # Query database for username
        db.execute("INSERT INTO users (hash,username,age,email,regsport) VALUES(?,?,?,?,?)",generate_password_hash(request.form.get("password")),request.form.get("username"),request.form.get("Age"),request.form.get("e-mail"),request.form.get("sport"))
                
        return render_template("succes.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html",sports=SPORTS)
@app.route("/Participants")
def participants():
    dic = db.execute("SELECT username FROM users")
    return render_template("registrants.html",dicts=dic)
