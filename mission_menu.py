import pygame
import pygame_gui
from core import Core
from texas_map import texas_map_loop

MISSIONS = [
    {
        "id": "texas_siege",
        "title": "Осада Техаса",
        "desc": "Гранд-стратегия о войне за Техас. Только для теста.",
    }
]


def mission_select_menu(screen):
    settings = Core().settings
    theme = settings.get("ui_theme", "gothic")
    THEME_COLORS = {
        "gothic": {"bg": (40, 0, 0), "text": (255, 235, 230)},
        "dark": {"bg": (30, 30, 30), "text": (235, 235, 255)},
        "light": {"bg": (230, 230, 240), "text": (40, 40, 60)},
    }
    colors = THEME_COLORS.get(theme, THEME_COLORS["gothic"])

    manager = pygame_gui.UIManager(screen.get_size())
    pygame.display.set_caption("Выбор миссии")

    font = pygame.font.SysFont("timesnewroman", 40, bold=True)
    title_text = font.render("ВЫБЕРИ МИССИЮ", True, colors["text"])
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 70))

    btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (screen.get_width() // 2 - 180, 180), (360, 60)),
        text=f"{MISSIONS[0]['title']}: {MISSIONS[0]['desc']}",
        manager=manager,
        object_id=f"#mission_{MISSIONS[0]['id']}",
    )

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (screen.get_width() // 2 - 180, 270), (170, 46)),
        text="В главное меню",
        manager=manager,
    )

    exit_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (screen.get_width() // 2 + 10, 270), (170, 46)),
        text="Выход",
        manager=manager,
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn:
                        texas_map_loop(screen)
                        continue  # После выхода с карты — вернуться к выбору миссии
                    if event.ui_element == back_btn:
                        return "menu"
                    if event.ui_element == exit_btn:
                        return "exit"
            manager.process_events(event)
        manager.update(time_delta)
        screen.fill(colors["bg"])
        screen.blit(title_text, title_rect)
        manager.draw_ui(screen)
        pygame.display.update()
