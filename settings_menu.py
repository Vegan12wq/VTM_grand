import pygame
import pygame_gui
from core import Core
from settings import change_setting

UI_THEME_COLORS = {
    "gothic": {
        "background": (40, 0, 0),
        "text": (255, 235, 230)
    },
    "dark": {
        "background": (30, 30, 30),
        "text": (235, 235, 255)
    },
    "light": {
        "background": (230, 230, 240),
        "text": (40, 40, 60)
    }
}


def settings_menu(screen):
    settings = Core().settings
    screen_size = screen.get_size()
    pygame.display.set_caption("Настройки")

    theme = settings.get("ui_theme", "gothic")
    colors = UI_THEME_COLORS.get(theme, UI_THEME_COLORS["gothic"])

    manager = pygame_gui.UIManager(screen_size)

    BG_COLOR = colors["background"]
    TEXT_COLOR = colors["text"]
    font = pygame.font.SysFont("timesnewroman", 48, bold=True)
    title_text = font.render("НАСТРОЙКИ", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen_size[0] // 2, 60))

    volume_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((220, 120), (360, 32)),
        start_value=settings.get("volume", 0.5) * 100,
        value_range=(0, 100),
        manager=manager
    )
    volume_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((80, 120), (120, 32)),
        text="Громкость:",
        manager=manager
    )

    language_drop = pygame_gui.elements.UIDropDownMenu(
        options_list=['Русский', 'English'],
        starting_option='Русский' if settings.get(
            "language", "ru") == "ru" else "English",
        relative_rect=pygame.Rect((220, 170), (200, 32)),
        manager=manager
    )
    lang_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((80, 170), (120, 32)),
        text="Язык:",
        manager=manager
    )

    fullscreen_switch = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((220, 220), (200, 32)),
        text="Вкл" if settings.get("fullscreen", False) else "Выкл",
        manager=manager
    )
    fullscreen_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((80, 220), (120, 32)),
        text="Полный экран:",
        manager=manager
    )

    text_speed_map = {"Медленно": "slow", "Средне": "medium", "Быстро": "fast"}
    rev_text_speed_map = {v: k for k, v in text_speed_map.items()}
    text_speed_drop = pygame_gui.elements.UIDropDownMenu(
        options_list=["Медленно", "Средне", "Быстро"],
        starting_option=rev_text_speed_map.get(
            settings.get("text_speed", "medium"), "Средне"),
        relative_rect=pygame.Rect((220, 270), (200, 32)),
        manager=manager
    )
    ts_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((80, 270), (120, 32)),
        text="Скорость текста:",
        manager=manager
    )

    subs_switch = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((220, 320), (200, 32)),
        text="Да" if settings.get("show_subtitles", True) else "Нет",
        manager=manager
    )
    subs_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((80, 320), (120, 32)),
        text="Субтитры:",
        manager=manager
    )

    theme_map = {"Готика": "gothic", "Тёмная": "dark", "Светлая": "light"}
    rev_theme_map = {v: k for k, v in theme_map.items()}
    theme_drop = pygame_gui.elements.UIDropDownMenu(
        options_list=["Готика", "Тёмная", "Светлая"],
        starting_option=rev_theme_map.get(
            settings.get("ui_theme", "gothic"), "Готика"),
        relative_rect=pygame.Rect((220, 370), (200, 32)),
        manager=manager
    )
    theme_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((80, 370), (120, 32)),
        text="Тема:",
        manager=manager
    )

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((screen_size[0]//2 - 80, 450), (160, 46)),
        text="Назад",
        manager=manager
    )

    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.USEREVENT:
                # --- Громкость ---
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == volume_slider:
                    vol = round(volume_slider.get_current_value() / 100, 2)
                    change_setting(settings, "volume", vol)
                # --- Язык ---
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == language_drop:
                    option = language_drop.selected_option
                    if isinstance(option, (tuple, list)):
                        option = option[0]
                    option = str(option)
                    lang = "ru" if option == "Русский" else "en"
                    change_setting(settings, "language", lang)
                    return "theme_changed"
                # --- Полный экран ---
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == fullscreen_switch:
                    fs = not settings.get("fullscreen", False)
                    change_setting(settings, "fullscreen", fs)
                    fullscreen_switch.set_text("Вкл" if fs else "Выкл")
                    return "toggle_fullscreen"
                # --- Скорость текста ---
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == text_speed_drop:
                    option = text_speed_drop.selected_option
                    if isinstance(option, (tuple, list)):
                        option = option[0]
                    option = str(option)
                    if option in text_speed_map:
                        speed = text_speed_map[option]
                        change_setting(settings, "text_speed", speed)
                # --- Субтитры ---
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == subs_switch:
                    val = not settings.get("show_subtitles", True)
                    change_setting(settings, "show_subtitles", val)
                    subs_switch.set_text("Да" if val else "Нет")
                # --- Тема ---
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == theme_drop:
                    option = theme_drop.selected_option
                    if isinstance(option, (tuple, list)):
                        option = option[0]
                    option = str(option)
                    if option in theme_map:
                        th = theme_map[option]
                        change_setting(settings, "ui_theme", th)
                        return "theme_changed"
                    else:
                        print(
                            f"WARNING: theme option {repr(option)} not in theme_map: {theme_map}")
                # --- Назад ---
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == back_btn:
                    return
            manager.process_events(event)

        manager.update(time_delta)
        screen.fill(BG_COLOR)
        screen.blit(title_text, title_rect)
        manager.draw_ui(screen)
        pygame.display.update()
