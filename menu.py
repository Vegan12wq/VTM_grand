# menu.py
import pygame
import os
import pygame_gui
from core import Core
from settings import change_setting

def main_menu(screen):
    import mission_menu

    while True:
        settings = Core.get().settings
        lang = settings.get("language", "ru")
        UI_THEME_COLORS = {
            "gothic": {
                "background": (40, 0, 0),
                "panel": (10, 0, 0),
                "title": (255, 225, 70),
                "title_shadow": (30, 0, 0),
                "text": (255, 235, 230),
                "version": (130, 90, 80),
                "overlay": (8, 0, 0, 220),
            },
            "dark": {
                "background": (30, 30, 30),
                "panel": (16, 16, 16),
                "title": (230, 230, 255),
                "title_shadow": (10, 10, 16),
                "text": (235, 235, 255),
                "version": (90, 130, 120),
                "overlay": (16, 16, 16, 210),
            },
            "light": {
                "background": (230, 230, 240),
                "panel": (255, 255, 255),
                "title": (45, 60, 150),
                "title_shadow": (190, 190, 210),
                "text": (40, 40, 60),
                "version": (120, 120, 180),
                "overlay": (230, 230, 255, 220),
            }
        }
        colors = UI_THEME_COLORS.get(settings.get("ui_theme", "gothic"), UI_THEME_COLORS["gothic"])
        LANGUAGES = {
            "ru": {
                "new_game": "Новая игра",
                "load_game": "Загрузить",
                "settings": "Настройки",
                "about": "О игре",
                "exit": "Выход",
                "language": "Язык: Русский",
                "version": "Версия: v0.2",
                "fullscreen": "Полноэкранный режим"
            },
            "en": {
                "new_game": "New Game",
                "load_game": "Load Game",
                "settings": "Settings",
                "about": "About",
                "exit": "Exit",
                "language": "Language: English",
                "version": "Version: v0.2",
                "fullscreen": "Fullscreen"
            }
        }
        pygame.display.set_caption("VTM Чёрное Солнце — Главное меню")
        manager = pygame_gui.UIManager(screen.get_size())

        MUSIC_FILE = "mainmenu.ogg"
        if os.path.exists(MUSIC_FILE):
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.set_volume(settings.get("volume", 0.5))
            pygame.mixer.music.play(-1)

        w, h = screen.get_size()
        btn_w = 320
        btn_h = 56
        gap = 18
        base_y = h // 2 - (btn_h * 4 + gap * 3) // 2 + 60

        buttons = {}
        button_order = ["new_game", "load_game", "settings",
                        "about", "language", "fullscreen", "exit"]
        for i, key in enumerate(button_order):
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (w//2 - btn_w//2, base_y + i * (btn_h + gap)), (btn_w, btn_h)),
                text=LANGUAGES[lang][key],
                manager=manager,
                object_id=f'#btn_{key}'
            )
            buttons[key] = btn

        title_font = pygame.font.SysFont("timesnewroman", 64, bold=True)
        title_text = title_font.render(
            "VTM Чёрное Солнце", True, colors["title"])
        title_shadow = title_font.render(
            "VTM Чёрное Солнце", True, colors["title_shadow"])

        show_about = False

        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        key = None
                        for k, btn in buttons.items():
                            if event.ui_element == btn:
                                key = k
                                break
                        if key == "new_game":
                            import mission_menu
                            mission = mission_menu.mission_select_menu(screen)
                            if mission == "menu":
                                break
                            if mission == "exit" or mission is None:
                                return "exit"
                            return ("start_mission", mission)
                        elif key == "exit":
                            return "exit"
                        elif key == "settings":
                            import settings_menu as settings_menu
                            result = settings_menu.settings_menu(screen)
                            if result == "toggle_fullscreen":
                                return "toggle_fullscreen"
                            elif result == "theme_changed":
                                running = False
                                break
                        elif key == "about":
                            show_about = True
                        elif key == "language":
                            new_lang = "en" if lang == "ru" else "ru"
                            change_setting(settings, "language", new_lang)
                            running = False
                            break
                        elif key == "fullscreen":
                            return "toggle_fullscreen"
                manager.process_events(event)

            manager.update(time_delta)
            screen.fill(colors["background"])
            title_rect = title_text.get_rect(center=(w//2, 80))
            pygame.draw.rect(
                screen, colors["panel"],
                (title_rect.left-20, title_rect.top-10,
                 title_rect.width+40, title_rect.height+20),
                border_radius=24
            )
            screen.blit(title_shadow, (title_rect.x+3, title_rect.y+4))
            screen.blit(title_text, title_rect)
            ver_font = pygame.font.SysFont("arial", 26)
            ver_text = ver_font.render(
                LANGUAGES[lang]["version"], True, colors["version"])
            screen.blit(ver_text, (24, h - 44))
            manager.draw_ui(screen)

            if show_about:
                overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                overlay.fill(colors["overlay"])
                screen.blit(overlay, (0, 0))
                about_lines = [
                    "Vampire: The Masquerade Grand Strategy",
                    "",
                    "Автор кода: Дмитрий",
                    "Художник: (ваше имя)",
                    "",
                    "Pygame, стиль — Gothic",
                    "",
                    LANGUAGES[lang]["exit"] + ": Esc / ЛКМ"
                ]
                font = pygame.font.SysFont("timesnewroman", 32)
                for i, line in enumerate(about_lines):
                    txt = font.render(line, True, colors["text"])
                    rect = txt.get_rect(
                        center=(w // 2, 180 + i * 38))
                    screen.blit(txt, rect)
            pygame.display.update()

            if show_about:
                for event in pygame.event.get():
                    if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                        show_about = False

            if not running:
                break
