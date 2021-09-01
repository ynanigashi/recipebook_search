import os

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql.expression import select
from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy.orm import Session as orm_session

from models import Base
from models import Users
from models import Ingredient
from models import Book
from models import Author
from models import Category
from models import Recipe
from models import RelationRecipeIngredient


# create engine
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite+pysqlite:///recipe_search.db'
DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

engine = create_engine(DATABASE_URL, future=True, echo=True)

# initialize data bases 
def init_db():
    try:
        Base.metadata.drop_all(engine)
    except Exception as e:
        print('drop error! but continue')

    Base.metadata.create_all(engine)
    print('create_all is done')

# register user
def register_user(username, password):
    # check username
    if not username:
        raise Exception('User name is required.')
    # check passwords
    if not password:
        raise Exception('password is required.')

    with orm_session(engine) as ss:
        """Register user"""
        # check username is already in used
        users = ss.query(Users)
        for user in users:
            if user.name == username:
                raise Exception("The user name is already in used.")

        user = Users();
        user.name = username
        user.hash = generate_password_hash(password)
        ss.add(user)
        ss.commit()
        print(f'User registered id: {user.id}')

def get_user_by_name(username):
    stmt = select(Users).where(Users.name == username)
    with orm_session(engine) as ss:
        user = ss.execute(stmt).first()
    # username is invalid then user is None
    if not user: return user

    # username is valid then user is tapple
    user, = user
    return user.to_dict()

def register_tables(recipe_dicts):
    # create ingredients books authors category set
    ingredients, books, authors, categories = set(), set(), set(), set()
    for recipe_dict in recipe_dicts:
        for ingredient in recipe_dict['ingredients']:
            ingredients.add(ingredient)
        books.add(recipe_dict['book_title'])
        authors.add(recipe_dict['author'])
        categories.add(recipe_dict['category'])
    print(f'len of indredients: {len(ingredients)}')
    print(f'len of books: {len(books)}')
    print(f'len of authors: {len(authors)}')
    print(f'len of categories: {len(categories)}')

    # prepare ingredient instance
    ingredient_dict = {}
    for ingredient_name in ingredients:
        ingredient = Ingredient(name = ingredient_name)
        ingredient_dict[ingredient_name] = ingredient
        
    # prepare book instance
    book_dict = {}
    for book_name in books:
        book = Book(name = book_name)
        book_dict[book_name] = book
    
    # prepare author instance
    author_dict = {}
    for author_name in authors:
        author = Author(name = author_name)
        author_dict[author_name] = author

    # prepare author instance
    category_dict = {}
    for category_name in categories:
        category = Category(name = category_name)
        category_dict[category_name] = category

    # prepare recipe instance
    for recipe_dict in recipe_dicts:
        recipe_dict['instance'] = Recipe(name = recipe_dict['name'])

    # register data
    with orm_session(engine) as ss:
        result = ss.execute(delete(Recipe))
        result = ss.execute(delete(Ingredient))
        result = ss.execute(delete(RelationRecipeIngredient))
        result = ss.execute(delete(Book))
        result = ss.execute(delete(Author))
        result = ss.execute(delete(Category))
        ss.commit()

        for ingredient in ingredient_dict.values():
            ss.add(ingredient)
        
        for book in book_dict.values():
            ss.add(book)
        
        for author in author_dict.values():
            ss.add(author)
        
        for category in category_dict.values():
            ss.add(category)

        ss.commit()

        for recipe_dict in recipe_dicts:
            recipe = recipe_dict['instance']
            book_name = recipe_dict['book_title']
            author_name = recipe_dict['author']
            category_name = recipe_dict['category']

            for ingredient_name in recipe_dict['ingredients']:
                # print(ingredient_name)
                recipe.ingredients.append(ingredient_dict[ingredient_name])
            recipe.book_id = book_dict[book_name].id
            recipe.author_id = author_dict[author_name].id
            recipe.category_id = category_dict[category_name].id
            ss.add(recipe)

        ss.commit()