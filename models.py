from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

"""
Tables
"""
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)

    def __repr__(self):
        return f'id: {self.id}, user name: {self.username}, cash: {self.cash}'

class RelationRecipeIngredient(Base):
    __tablename__ = 'relation_recipe_ingredient'
    recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)


class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    recipes = relationship(
        "Recipe",
        secondary=RelationRecipeIngredient.__tablename__,
        back_populates="ingredients"
    )


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    author_id = Column(Integer, ForeignKey('author.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    ingredients = relationship(
        "Ingredient",
        secondary=RelationRecipeIngredient.__tablename__,
        back_populates="recipes"
    )


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    recipes = relationship("Recipe", backref="book")


class Author(Base):
    # author of recipe (but not author of book)
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    recipes = relationship("Recipe", backref="author")


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    recipes = relationship("Recipe", backref="category")


class IngredientKeyword(Base):
    __tablename__ = 'ingredient_keyword'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    keyword = Column(String, index=True)