import os

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql.expression import select
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session as orm_session

from models import Base
from models import Users

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
            if user.username == username:
                raise Exception("The user name is already in used.")

        user = Users();
        user.username = username
        user.hash = generate_password_hash(password)
        ss.add(user)
        ss.commit()
        print(f'User registered id: {user.id}')