from flask import Blueprint

bp_animes = Blueprint("animes", __name__, url_prefix="/animes")

bp_animes.get("")