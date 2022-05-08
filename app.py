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
import random

def strToFrac(string):
    ls = string.split("/")
    string = int(ls[0]) / int(ls[1])
    return string


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

        user_id = int(session["user_id"])

        # Showing up now, but wasn't before I made sure to log in user on registration
        flash(f"{session['name']} has been registered and logged in!")

        # start to populate the math_activities database for this user. 
        db.execute("INSERT INTO math_activities (user_id, title, id, correct, attempted) values (?, ?, 0, 0, 0)", user_id, "Practice - Easier")
        db.execute("INSERT INTO math_activities (user_id, title, id, correct, attempted) values (?, ?, 0, 0, 0)", user_id, "Test - Easier")
        db.execute("INSERT INTO math_activities (user_id, title, id, correct, attempted) values (?, ?, 0, 0, 0)", user_id, "Practice - Harder")
        db.execute("INSERT INTO math_activities (user_id, title, id, correct, attempted) values (?, ?, 0, 0, 0)", user_id, "Test - Harder")

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

    user_no = int(session["user_id"])

    rows = db.execute("SELECT * FROM math_activities WHERE user_id = ?", user_no)

    return render_template("profile.html", rows=rows)

@app.route("/activities")
def activities():
    return render_template("activities.html")


@app.route("/quadraticsEasyTest", methods=["GET", "POST"])
@login_required
def quadraticsEasyTest():

    list1 = [-5,-4,-3,-2,-1, 1, 2, 3, 4, 5, 6]
    rootP = int(random.choice(list1))
    rootQ = int(random.choice(list1))

    p = int(-1 * rootP)
    q = int(-1 * rootQ)

    coeffB = int(p + q)
    coeffC = int(p * q)

    if request.method == "POST":

        user_no = int(session["user_id"])

        ans1 = -int(request.form.get("first_solution"))
        ans2 = -int(request.form.get("second_solution"))

        if ((ans1 + ans2 == coeffB) and (ans1 * ans2 == coeffC)):
            flash("That's correct! Well done!")
            db.execute("UPDATE math_activities SET attempted = (attempted + 1) WHERE user_id = ? AND title = ?", user_no, "Test - Easier")
            db.execute("UPDATE math_activities SET correct = (correct + 1) WHERE user_id = ? AND title = ?", user_no, "Test - Easier")

        else:
            flash("That's not quite correct! Have another go!")
            db.execute("UPDATE math_activities SET attempted = (attempted + 1) WHERE user_id = ? AND title = ?", user_no, "Test - Easier")

        return render_template("activities/quadraticsEasyTest.html", coeffB=coeffB, coeffC=coeffC)
    else:
        return render_template("activities/quadraticsEasyTest.html", coeffB=coeffB, coeffC=coeffC)
    
@app.route("/quadraticsEasySolver", methods=["GET", "POST"])
@login_required
def quadraticsEasySolver():
    if request.method == "POST":
        pass
    else:
        problems = [mathgen.genById(21), mathgen.genById(50)]
        return render_template("activities/quadraticsEasySolver.html", problems=problems, coeffB=coeffB, coeffC=coeffC)

@app.route("/teacherSolverHard", methods=["GET", "POST"])
@login_required
def teacherSolverHard():
    if request.method == "POST":
        pass
    else:
        return render_template("activities/teacherSolverHard.html")
    
@app.route("/studentSolverHard", methods=["GET", "POST"])
@login_required
def studentSolverHard():
    if request.method == "POST":
        pass
    else:
        return render_template("activities/studentSolverHard.html")

@app.route("/SolverStudentEasy", methods=["GET", "POST"])
@login_required
def SolverStudentEasy():
    if request.method == "POST":
        user_no = int(session["user_id"])
        ans1 = int(request.form.get("first_solution"))
        ans2 = int(request.form.get("second_solution"))

        db.execute("UPDATE math_activities SET attempted = (attempted + 1) WHERE user_id = ? AND title = ?", user_no, "Practice - Easier")
        db.execute("UPDATE math_activities SET correct = (correct + 1) WHERE user_id = ? AND title = ?", user_no, "Practice - Easier")

        return render_template("activities/SolverStudentEasy.html")
    else:

        list1 = [-5,-4,-3,-2,-1, 1, 2, 3, 4, 5, 6]
        rootP = random.choice(list1)
        rootQ = random.choice(list1)

        p = -1 * rootP;
        q = -1 * rootQ;

        coeffB = p + q;
        coeffC = p * q;

        return render_template("activities/SolverStudentEasy.html", p=p, q=q)

@app.route("/studentTestHard", methods=["GET", "POST"])
@login_required
def studentTestHard():
    if request.method == "POST":
        factCoeffA = int(request.form.get("factCoeffA"))
        factCoeffB = int(request.form.get("factCoeffB"))
        factCoeffC = int(request.form.get("factCoeffC"))
        factCoeffD = int(request.form.get("factCoeffD"))

        standCoeffA = int(request.form.get("standCoeffA"))
        standCoeffB = int(request.form.get("standCoeffB"))
        standCoeffC = int(request.form.get("standCoeffC"))

        ans1 = -1 * factCoeffB / factCoeffA
        ans2 = -1 * factCoeffD / factCoeffC

        guess1 = request.form.get("guess1")
        guess2 = request.form.get("guess2")

        if guess1 and guess2 is not "":
            if "/" in guess1:
                guess1 = strToFrac(guess1)
            guess1 = float(guess1)

            if "/" in guess2:
                guess2 = strToFrac(guess2)
            guess2 = float(guess2)

            ans1 = round(ans1, 4)
            ans2 = round(ans2, 4)

            guess1 = round(guess1, 4)
            guess2 = round(guess2, 4)

            user_no = int(session["user_id"])


            if ans1 == guess1:
                if ans2 == guess2:
                    flash(f"{standCoeffA}x^2 + {standCoeffB}x + {standCoeffC} = 0 ---> x = {ans1}, {ans2} ---> Good job! (+1 Point)")
                    
                    db.execute("UPDATE math_activities SET attempted = (attempted + 1) WHERE user_id = ? AND title = ?", user_no, "Test - Harder")
                    db.execute("UPDATE math_activities SET correct = (correct + 1) WHERE user_id = ?  AND title = ?", user_no, "Test - Harder")

            elif ans1 == guess2:
                if ans2 == guess1:
                    flash(f"{standCoeffA}x^2 + {standCoeffB}x + {standCoeffC} = 0 ---> x = {ans1}, {ans2} ---> Good job! (+1 Point)")
                    
                    db.execute("UPDATE math_activities SET attempted = (attempted + 1) WHERE user_id = ? AND title = ?", user_no, "Test - Harder")
                    db.execute("UPDATE math_activities SET correct = (correct + 1) WHERE user_id = ?  AND title = ?", user_no, "Test - Harder")

            else:
                    flash(f"{standCoeffA}x^2 + {standCoeffB}x + {standCoeffC} = 0 ---> x = {ans1}, {ans2} ---> Not Quite")
                    db.execute("UPDATE math_activities SET attempted = (attempted + 1) WHERE user_id = ? AND title = ?", user_no, "Test - Harder")


        factCoeffA = random.randint(-8, 8)
        if factCoeffA == 0:
            factCoeffA += 1
        factCoeffB = random.randint(-8, 8)
        if factCoeffB == 0:
            factCoeffB += 1
        factCoeffC = random.randint(-8, 8)
        if factCoeffC == 0:
            factCoeffC += 1
        factCoeffD = random.randint(-8, 8)
        if factCoeffD == 0:
            factCoeffD += 1

        standCoeffA = factCoeffA * factCoeffC
        standCoeffC = factCoeffB * factCoeffD
        standCoeffB = factCoeffA * factCoeffD + factCoeffB * factCoeffC

        factCoeff = [factCoeffA, factCoeffB, factCoeffC, factCoeffD]
        standCoeff = [standCoeffA, standCoeffB, standCoeffC]

        return render_template("/activities/studentTestHard.html", factCoeff=factCoeff, standCoeff=standCoeff)
    else:

        factCoeffA = random.randint(-8, 8)
        if factCoeffA == 0:
            factCoeffA += 1
        factCoeffB = random.randint(-8, 8)
        if factCoeffB == 0:
            factCoeffB += 1
        factCoeffC = random.randint(-8, 8)
        if factCoeffC == 0:
            factCoeffC += 1
        factCoeffD = random.randint(-8, 8)
        if factCoeffD == 0:
            factCoeffD += 1

        standCoeffA = factCoeffA * factCoeffC
        standCoeffC = factCoeffB * factCoeffD
        standCoeffB = factCoeffA * factCoeffD + factCoeffB * factCoeffC

        factCoeff = [factCoeffA, factCoeffB, factCoeffC, factCoeffD]
        standCoeff = [standCoeffA, standCoeffB, standCoeffC]


        return render_template("/activities/studentTestHard.html", factCoeff=factCoeff, standCoeff=standCoeff)


@app.route("/practiceQuiz")
@login_required
def practiceQuiz():
    if request.method == "POST":
        pass
    else:
        return render_template("practiceQuiz.html")