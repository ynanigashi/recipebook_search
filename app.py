import os

from flask import Flask
from flask import render_template
from flask import redirect
from flask import flash
from flask import request
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology
from helpers import login_required
from helpers import allowed_file
from helpers import extract_tables_from_xlsx
from db import get_user_by_name
from db import register_tables
from db import get_user_by_id
from db import update_password
from db import get_recipes_by_ing_ids
from db import get_recipes_by_keyword
from db import get_recipes_by_book_title
from db import get_recipes_by_book_id
from db import get_recipes_by_author_name
from db import get_recipes_by_author_id
from db import get_categories
from db import get_ingredients
from db import get_recipe_by_id

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
    # get db data
    categories = get_categories()
    ingredients = get_ingredients()
    
    # get query parameter
    recipes = []
    recipe = {}
    req = request.args
    query_word = req.get('q')
    query_type = req.get('t')
    query_id = req.get('id')

    # change str to int
    try:
        ings = [int(i) for i in req.getlist('ings')]
    except ValueError as e:
        # alart invalid value
        flash('ingredients are invalid', 'danger')
        print(f'error:{e}')
        ings = []

    try:
        cats = [int(i) for i in req.getlist('cats')]
    except ValueError as e:
        # alart invalid value
        flash('category value is invalid', 'danger')
        print(f'error:{e}')
        cats = []

    # get recipes data
    if query_type == 'ingredients':
        recipes = get_recipes_by_ing_ids(ings, cats)
    elif query_type == 'recipe_name':
        recipes = get_recipes_by_keyword(query_word)
    elif query_type == 'recipe_id':
        recipe = get_recipe_by_id(query_id)
    elif query_type == 'book_title':
        recipes = get_recipes_by_book_title(query_word)
    elif query_type == 'book_id':
        recipes = get_recipes_by_book_id(query_id)
    elif query_type == 'author_name':
        recipes = get_recipes_by_author_name(query_word)
    elif query_type == 'author_id':
        recipes = get_recipes_by_author_id(query_id)

    return render_template('search.html',
                            query_type=query_type,
                            ings=ingredients,
                            selected_ings=ings,
                            cats=categories,
                            selected_cats=cats,
                            query_word=query_word,
                            recipes=recipes,
                            recipe=recipe 
                            )


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('must provide username', 'danger')
            return render_template('login.html')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('must provide password', 'danger')
            return render_template('login.html')

        # Query database by username
        user = get_user_by_name(request.form.get('username'))
        # Ensure username exists and password is correct
        if not user or not check_password_hash(user['hash'], request.form.get("password")):
            flash('invalid user name or password', 'danger')
            return render_template('login.html')

        # Remember which user has logged in
        session["user_id"] = user['id']

        # Redirect user to home page
        flash('login succeed', 'success')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == 'POST':
        # check request
        if 'file' not in request.files:
            return apology('not file part')
        file = request.files['file']
        
        # check file is posted
        if file.filename == '':
            flash('file is required', "danger")
            return render_template('upload.html')
        
        # register file data
        if file and allowed_file(file.filename):
            recipes = extract_tables_from_xlsx(file.stream.read())
            try:
                register_tables(recipes)
            except Exception as e:
                flash('file is invalid', 'danger')
                print(e)
            else:
                flash(f'{file.filename} is registerd', "success")
        else:
            flash('file is invalid', "danger")
        return render_template('upload.html')
    else:
        return render_template('upload.html')


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

        # get current pw hash
        user = get_user_by_id(user_id)
        if not user:
            flash('invalid user', 'danger')
            return render_template('changepw.html') 

        # Ensure password is correct
        if not check_password_hash(user['hash'], current_pw):
            flash('invalid password', 'danger')
            return render_template('changepw.html')

        # check new passwords
        if not password:
            flash('new password is required', 'danger')
            return render_template('changepw.html')
        if not confirmation:
            flash('nconfirm password is required', 'danger')
            return render_template('changepw.html')
        elif password != confirmation:
            flash('confirm password is not match', 'danger')
            return render_template('changepw.html')

        # update password
        update_password(user['id'], generate_password_hash(password))

        # Redirect user to home page
        flash('password has changed', 'success')
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