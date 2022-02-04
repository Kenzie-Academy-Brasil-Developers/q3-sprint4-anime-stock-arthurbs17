from flask import jsonify, request
from http import HTTPStatus
from psycopg2.errors import UniqueViolation, UndefinedColumn

from app.models.animes_models import Animes
from app.exc.wrong_key_received import WrongKeyReceived

def get_all_animes():
    animes = Animes.get_all_animes()

    return jsonify({"data":[Animes.serializer(anime) for anime in animes]}), HTTPStatus.OK

def add_anime():
    data = request.get_json()
    
    try:
        anime = Animes(**data)
        inserted_anime = anime.to_add_anime()
    except KeyError:
        error = WrongKeyReceived(data)
        return jsonify(error.message), HTTPStatus.UNPROCESSABLE_ENTITY
    except UniqueViolation:
        return jsonify({"error": "anime is already exists"}), HTTPStatus.UNPROCESSABLE_ENTITY
    
    return jsonify(Animes.serializer(inserted_anime)), HTTPStatus.OK

def get_specif_anime(id: int):
    
    try:
        anime = Animes.get_specific_anime(id)
        return jsonify({"data": [Animes.serializer(anime)]}), HTTPStatus.OK
    except TypeError:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND

def updated_anime(id: int):
    data = request.get_json()

    try:
        att_anime = Animes.updated_anime(id, data)
        return jsonify(Animes.serializer(att_anime)), HTTPStatus.OK
    except UndefinedColumn:
        error = WrongKeyReceived(data)
        return jsonify(error.message), HTTPStatus.UNPROCESSABLE_ENTITY
    except TypeError:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND