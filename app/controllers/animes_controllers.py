from flask import jsonify, request
from http import HTTPStatus
from app.models.animes_models import Animes

def get_all_animes():
    animes = Animes.get_all_animes()

    return jsonify([Animes.serializer(anime) for anime in animes]), HTTPStatus.OK

def add_anime():
    data = request.get_json()

    anime = Animes(**data)

    inserted_anime = anime.to_add_anime()

    return Animes.serializer(inserted_anime), HTTPStatus.OK