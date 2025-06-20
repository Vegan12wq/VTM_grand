import json
import os

SAVE_PATH = "savegame.json"


def save_game(data):
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print("Игра сохранена.")


def load_game():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            data = json.load(f)
        print("Сохранение загружено.")
        return data
    else:
        print("Сохранение не найдено.")
        return None
