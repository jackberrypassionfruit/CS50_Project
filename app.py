import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from math import ceil, floor
from helpers import * # Right now, just apology() & login_required()
from mathgenerator import mathgen



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///omegaMath.db")


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
    """Show dashboard of student's progress"""
    if not session.get("name"):
        return redirect("/login")
    
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        """Register user"""

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        users = db.execute("SELECT * FROM users")

        if username in [user["username"] for user in users] or username == "":
            return apology("Username blank or already exists", 400)

        if password != confirmation or password == "":
            return apology("Passwords do not match or are blank", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["name"] = rows[0]["username"]

        # Showing up now, but wasn't before I made sure to log in user on registration
        flash(f"{session['name']} has been registered and logged in!")

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["name"] = rows[0]["username"]

        # Flashing!
        flash("Logged In!")

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

@app.route("/profile")
def profile():
    """ Shows current user's profile"""
    return render_template("profile.html")

@app.route("/activities")
def activities():
    return render_template("activities.html")


@app.route("/quadraticsEasyTest", methods=["GET", "POST"])
@login_required
def quadraticsEasyTest():
    if request.method == "POST":
        problems = [mathgen.genById(21), mathgen.genById(50)]
        
        coeffA = int(request.form.get("coeffA"))
        coeffB = int(request.form.get("coeffB"))
        coeffC = int(request.form.get("coeffC"))

        ans1 = int(request.form.get("ans1"))
        ans2 = int(request.form.get("ans2"))

        roots = []

        if int(coeffC == 0):
            roots = [0, -1 * coeffB / coeffA]
        elif int(coeffA) == 1:
            """ Easy mode
            Steps:
            1) Make a list of factors of C
            2) Check which pairs of factors multiply to C, make list of those pairs
            --- This is probably the hardest Part
            3) Test each pair of factors, which ones add to B. Return pair if True
            --- Unless C is negative, then test if they subtract to B
            --- If that's the case, then order will matter. Return the pair in that specific order
            --- If C is a perfect square this algorith should account for the factor_pairs having 2 of the square root in the last pair
            
            --- Stretch
            4) If still none True, test determinate for solutions, and return expected result (ex. 2 real, 1 real, 2 imaginary sol.)
            """
            
            # 1) 
            """ Check over each number from 1 to C to see if it's a factor, and make a list of them """
            factors_C = [x for x in range(1, abs(coeffC) + 1) if abs(coeffC) % x == 0]
            
            # 2)
            """ Factors list is ordered (6 ---> [1, 2, 3, 6]) so only need to check sets of converging outers ([1, 6] , [2, 3])"""
            iter = ceil(len(factors_C) / 2)
            factor_pairs = []
            for i in range(iter):
                factor_pairs.append([factors_C[i], factors_C[-i - 1]])
                
            # 3)
            op, flip = 1, 1 # to account for a negative C term, create variable named op to multiply by 2nd factor in pair check if they add to B, to simulate subtracting
                            # Flip also accounts for if C is positive AND B is negative, meaning both zeroes become negative in the end
            if coeffC < 0:
                op = -1
            elif coeffB < 0:
                flip = -1
                 
            
            for pair in factor_pairs:
                if flip * pair[0] + (flip * op * pair[1]) == coeffB:
                    # flash("Roots of the solution are: ")
                    # flash([flip * pair[0], flip * op * pair[1]])
                    roots = [-1 * flip * pair[0], -1 * flip * op * pair[1]] # -1 * because finding roots, not factored form
                elif flip * pair[1] + (flip * op * pair[0]) == coeffB:
                    # flash("Roots of the solution are: ")
                    # flash([flip * pair[1], flip * op * pair[0]])
                    roots = [-1 * flip * pair[1], -1 * flip * op * pair[0]]

            
            
        else:
            """ Hard mode"""
            pass

        if ans1 in roots and ans2 in roots:
            flash("Yup!")
        else:
            flash(f"Nah, answers are {roots}")
        
        return render_template("activities/quadraticsEasyTest.html", problems=problems)
    else:
        problems = [mathgen.genById(21), mathgen.genById(50)]

        return render_template("activities/quadraticsEasyTest.html", problems=problems)
    
@app.route("/quadraticsEasySolver", methods=["GET", "POST"])
@login_required
def quadraticsEasySolver():
    if request.method == "POST":
        pass
    else:
        problems = [mathgen.genById(21), mathgen.genById(50)]
        return render_template("activities/quadraticsEasySolver.html", problems=problems)

@app.route("/acMethod", methods=["GET", "POST"])
@login_required
def acMethod():
    if request.method == "POST":
        pass
    else:
        return render_template("activities/quadraticsHard.html")

@app.route("/SolverStudentEasy", methods=["GET", "POST"])
@login_required
def SolverStudentEasy():
    if request.method == "POST":

        return render_template("activities/SolverStudentEasy.html")
    else:
        return render_template("activities/SolverStudentEasy.html")


@app.route("/practiceQuiz")
@login_required
def practiceQuiz():
    if request.method == "POST":
        pass
    else:
        return render_template("practiceQuiz.html")