import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from math import ceil


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///solver.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/math")
def math():
    return render_template("math.html")

@app.route("/solver", methods=["GET", "POST"])
def solver():
    if request.method == "POST":
        coeffA = int(request.form.get("coeffA"))
        coeffB = int(request.form.get("coeffB"))
        coeffC = int(request.form.get("coeffC"))
        if int(coeffA) == 1:
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
            
            # 1) check over each number from 1 to C to see if it's a factor, and make a list of them
            factors_C = [x for x in range(1, abs(coeffC) + 1) if abs(coeffC) % x == 0]
            
            # 2)
            """ Factors list is ordered (6 ---> [1, 2, 3, 6]) so only need to check sets of converging outers ([1, 6] , [2, 3])"""
            iter = ceil(len(factors_C) / 2)
            factor_pairs = []
            for i in range(iter):
                factor_pairs.append([factors_C[i], factors_C[-i - 1]])
                
            # 3)
            op = 1 # to account for a negative B term, create variable to multiply by 2nd factor in pair check if they add to B, to simulate subtracting
            flip = 1 # This one also for account if C is positive AND B negative, meaning both zeroes become negative in the end
            if coeffC < 0:
                op = -1
            elif coeffB < 0:
                flip = -1
                 
            
            for pair in factor_pairs:
                if flip * pair[0] + (flip * op * pair[1]) == coeffB:
                    flash("Roots of the solution are: ")
                    flash([flip * pair[0], flip * op * pair[1]])
                elif flip * pair[1] + (flip * op * pair[0]) == coeffB:
                    flash("Roots of the solution are: ")
                    flash([flip * pair[1], flip * op * pair[0]])
            
        else:
            """ Hard mode"""
            pass
        
        return render_template("solver.html")
    else:
        return render_template("solver.html")