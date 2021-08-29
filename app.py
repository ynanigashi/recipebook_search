import os

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology
from helpers import login_required
from models import Users
from db import engine
from db import orm_session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use secret_key
if not os.environ.get("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY not set")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["SESSION_TYPE"] = "memcached"

@app.route("/")
@login_required
def index():
    user_id = session.get("user_id")
    return f'loged in user_id is {user_id}'


@app.route("/login", methods=["GET", "POST"])
def login():
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

        with orm_session(engine) as ss:
            # Query database for username
            user = ss.query(Users).filter(Users.username == request.form.get('username')).first()
            
            # Ensure username exists and password is correct
            if user == None or not check_password_hash(user.hash, request.form.get("password")):
                return apology("invalid username and/or password", 403)

            # Remember which user has logged in
            session["user_id"] = user.id

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


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    if request.method == "POST":
        user_id = session.get("user_id")

        # get form data
        current_pw = request.form.get("current_pw")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure password was submitted
        if not current_pw:
            return apology("must provide password", 400)

        with orm_session(engine) as ss:
            # get current pw hash
            hash = ss.query(Users).filter(Users.id==user_id).first().hash

            # Ensure password is correct
            if not check_password_hash(hash, current_pw):
                return apology("invalid password", 400)

            # check new passwords
            if not password:
                return apology("new password is required.", 400)
            if not confirmation:
                return apology("Confirmation password is required.", 400)
            elif password != confirmation:
                return apology("Confirmation password do not match.", 400)

            """Update password"""
            hash = generate_password_hash(password)
            user = ss.query(Users).filter(Users.id==user_id).first()
            user.hash = hash
            ss.commit()

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("changepw.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)