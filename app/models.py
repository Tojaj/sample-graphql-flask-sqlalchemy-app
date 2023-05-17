import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    SmallInteger,
    Numeric,
    text,
    ForeignKey,
)
from sqlalchemy.types import Date, BLOB, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base


class DictMixIn:
    """This MixIn converts model objects to JSON representation"""

    def to_dict(self):
        """This method is called when we use jsonify() from flask module
        when returing response on /graphql POST requests."""

        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


# Association tables (link tables)
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many

# film_actor = Table(
#     "film_actor",
#     Base.metadata,
#     Column("actor_id", ForeignKey('actor.actor_id'), primary_key=True, nullable=False),
#     Column("film_id", ForeignKey('film.film_id'), primary_key=True, nullable=False),
#     Column("last_update", nullable=False)
# )


# film_category = Table(
#     "film_category",
#     Base.metadata,
#     Column("film_id", ForeignKey('film.film_id'), primary_key=True, nullable=False),
#     Column("category_id", ForeignKey('category.category_id'), primary_key=True, nullable=False),
#     Column("last_update", nullable=False)
# )


# Types for SQLAlchemy: https://docs.sqlalchemy.org/en/20/core/types.html
# Clumns: https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column


class Actor(Base, DictMixIn):
    __tablename__ = "actor"

    actor_id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    last_update = Column(
        TIMESTAMP,
        nullable=False,
        server_default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
    )

    films = relationship("Film", secondary="film_actor", back_populates="actors")


class Language(Base, DictMixIn):
    __tablename__ = "language"

    language_id = Column(SmallInteger, primary_key=True)
    name = Column(String(20), nullable=False)
    last_update = Column(TIMESTAMP, nullable=False)


class Category(Base, DictMixIn):
    __tablename__ = "category"

    category_id = Column(SmallInteger, primary_key=True)
    name = Column(String(25), nullable=False)
    last_update = Column(TIMESTAMP, nullable=False)

    films = relationship("Film", secondary="film_category", back_populates="categories")


class Film(Base, DictMixIn):
    __tablename__ = "film"

    film_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String, default=None)
    release_year = Column(String(4), default=None)
    language_id = Column(SmallInteger, nullable=False)
    original_language_id = Column(SmallInteger, default=None)
    rental_duration = Column(SmallInteger, default=3, nullable=False)
    rental_rate = Column(Numeric(4, 2), default="4.99", nullable=False)
    length = Column(SmallInteger, default=None)
    replacement_cost = Column(Numeric(5, 2), default="19.99", nullable=False)
    rating = Column(String(10), default="G")
    special_features = Column(String(100), default=None)
    last_update = Column(TIMESTAMP, nullable=False)

    actors = relationship("Actor", secondary="film_actor", back_populates="films")
    categories = relationship(
        "Category", secondary="film_category", back_populates="films"
    )


# Association Objects


class FilmActor(Base, DictMixIn):
    __tablename__ = "film_actor"

    actor_id = Column(
        Integer, ForeignKey("actor.actor_id"), primary_key=True, nullable=False
    )
    film_id = Column(
        Integer, ForeignKey("film.film_id"), primary_key=True, nullable=False
    )
    last_update = Column(TIMESTAMP, nullable=False)


class FilmCategory(Base, DictMixIn):
    __tablename__ = "film_category"

    film_id = Column(
        Integer, ForeignKey("film.film_id"), primary_key=True, nullable=False
    )
    category_id = Column(
        SmallInteger,
        ForeignKey("category.category_id"),
        primary_key=True,
        nullable=False,
    )
    last_update = Column(TIMESTAMP, nullable=False)
