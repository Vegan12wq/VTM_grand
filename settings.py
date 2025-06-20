import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "volume": 0.5,              # Громкость (0.0–1.0)
    "language": "ru",           # Язык интерфейса
    "fullscreen": False,        # Полноэкранный режим
    "text_speed": "medium",     # Скорость текста
    "show_subtitles": True,     # Показывать субтитры
    "ui_theme": "gothic"        # Тема (gothic, dark, light)
}


def load_settings():
    """Загружает настройки из файла, дополняет их дефолтами при необходимости."""
    data = {}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
        except Exception as e:
            print("Ошибка загрузки settings.json:", e)
            data = {}
    # Автодополнение недостающих ключей
    for key, value in DEFAULT_SETTINGS.items():
        if key not in data:
            data[key] = value
    return data


def save_settings(settings):
    """Сохраняет настройки в файл settings.json."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def change_setting(settings, key, value):
    """Меняет настройку, сохраняет изменения, автоматически применяет известные параметры."""
    if key in DEFAULT_SETTINGS:
        settings[key] = value
        save_settings(settings)
        # Применить изменения "на лету"
        if key == "volume":
            try:
                import pygame
                pygame.mixer.music.set_volume(settings.get("volume", 0.5))
            except Exception:
                pass
        if key == "fullscreen":
            try:
                import pygame
                screen = pygame.display.get_surface()
                if value:
                    pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode((800, 600))
            except Exception:
                pass
    else:
        print(f"❌ Нет такой настройки: {key}")
