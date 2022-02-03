from flask import Blueprint
from app.controllers import animes_controllers

bp_animes = Blueprint("animes", __name__, url_prefix="/animes")

bp_animes.get("")(animes_controllers.get_all_animes)
bp_animes.post("")(animes_controllers.add_anime)