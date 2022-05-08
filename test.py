import os
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from math import ceil, floor
from helpers import * # Right now, just apology() & login_required()


# alpha = random.randint(-10, 10)
# beta = random.randint(-10, 10)

# a = 1
# b = -alpha + -beta
# c = -alpha * - beta
# print(a, b, c)


def strToFrac(string):
    ls = string.split("/")
    ans = int(ls[0]) / int(ls[1])
    return ans

print(strToFrac("1/6"))