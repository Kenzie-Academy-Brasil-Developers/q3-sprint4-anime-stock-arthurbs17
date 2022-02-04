class WrongKeyReceived(Exception):
    
    correct_keys = ["anime", "released_date", "seasons"]

    def __init__(self, data: dict) -> None:
        self.message = {
            "available_keys": self.correct_keys,
            "wrong_keys": self.wrong_key(data)
        }

    @classmethod
    def wrong_key(cls, data: dict) -> list:
        return [key for key in data.keys() if key not in cls.correct_keys]