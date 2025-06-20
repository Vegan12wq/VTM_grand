# game_state.py

class GameState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.init_state()
        return cls._instance

    def init_state(self):
        self.money = 1000
        self.blood = 20
        # Тут можно добавить и другие параметры (ход, карта и т.п.)

    def save(self):
        return {"money": self.money, "blood": self.blood}

    def load(self, data):
        self.money = data.get("money", 1000)
        self.blood = data.get("blood", 20)
