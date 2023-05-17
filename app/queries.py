from sqlalchemy import select

from app.database import db_session
from app.models import Film, Actor, Category


def listFilms_resolver(obj, info):
    try:
        result = db_session.scalars(select(Film).order_by(Film.film_id))
        films = result.all()
        payload = {"success": True, "data": films}
    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


def searchFilms_resolver(obj, info, title):
    try:
        result = db_session.scalars(
            select(Film)
            .where(Film.title.contains(title, autoescape=True))
            .order_by(Film.film_id)
        )
        films = result.all()
        payload = {"success": True, "data": films}
    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


def getFilm_resolver(obj, info, film_id):
    try:
        result = db_session.scalars(select(Film).where(Film.film_id == film_id))
        film = result.one_or_none()
        payload = {"success": True, "data": film}
    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload
