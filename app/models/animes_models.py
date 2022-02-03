from app.services.database_services import DatabaseConnector

class Animes(DatabaseConnector):
    def __init__(self, *args, **kwargs) -> None:
        self.anime = kwargs["anime"]
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]

    