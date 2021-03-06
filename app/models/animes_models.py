from app.services.database_services import DatabaseConnector


class Animes(DatabaseConnector):
    animes_columns = DatabaseConnector.get_columns_names()

    def __init__(self, *args, **kwargs) -> None:
        self.anime = kwargs["anime"].title()
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]

    def to_add_anime(self):
        return super().to_add_anime(self.__dict__)

    @classmethod
    def get_all_animes(cls):
        return super().get_all_animes()
    
    @classmethod
    def serializer(cls, data: tuple, keys: list[str] = animes_columns):
        return super().serializer(data, keys)
    
    @classmethod
    def get_specific_anime(cls, id: int):
        return super().get_specific_anime(id)
    
    @classmethod
    def updated_anime(cls, id: int, payload: dict):
        return super().updated_anime(id, payload)
    
    @classmethod
    def delete_anime(cls, id: int):
        return super().delete_anime(id)