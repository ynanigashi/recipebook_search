from flask import redirect, render_template, session
from functools import wraps
import pandas as pd


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


ALLOWED_EXTENSIONS = ('xls', 'xlsx')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

label_table = {
    "本のタイトル": 'book_title',
    "料理名": 'recipe',
    "作者": 'author',
    "区分": 'category',
    "カロリー": 'calorie',
    "カロリー単位": 'calorie_unit',
    "調理法・調理器具": 'tool',
    "主材料": 'ingredients',
    "検索": 'keywords',
}

def extract_tables_from_xlsx(excel):
    recipes = []
    df = pd.read_excel(excel, sheet_name='data', index_col=1)

    df.rename(columns=label_table, inplace=True)
    # for k, v in label_table.items():
    #     df.rename(columns={k: v}, inplace=True)
    
    for name, row in df.iterrows():
        recipe = {}
        ingredients = []
        for k, v in row.items():
            if k == 'keywords': continue
            if "主材料" in k:
                if v in ['', '-', 'ー', '―', '‐']:
                    continue
                ingredients.append(v)
            recipe[k] = v
        recipe['name'] = name
        recipe['ingredients'] = ingredients
        recipes.append(recipe)

    return recipes