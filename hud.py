import pygame
from resource_ui import ResourceUI

class MiniMap:
    def __init__(self, rect, camera):
        self.rect = pygame.Rect(rect)
        self.camera = camera

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        map_w, map_h = self.camera.map_width, self.camera.map_height
        screen_w, screen_h = screen.get_width(), screen.get_height()
        ratio_x = self.rect.width / map_w
        ratio_y = self.rect.height / map_h
        view_rect = pygame.Rect(
            self.rect.x + self.camera.x * ratio_x,
            self.rect.y + self.camera.y * ratio_y,
            screen_w * ratio_x,
            screen_h * ratio_y
        )
        pygame.draw.rect(screen, (200, 200, 200), view_rect, 2)

class ActionMenu:
    def __init__(self, font, position):
        self.options = []
        self.font = font
        self.position = position

    def set_options(self, options):
        self.options = options

    def draw(self, screen):
        for i, opt in enumerate(self.options):
            txt = self.font.render(opt, True, (255, 255, 255))
            screen.blit(txt, (self.position[0], self.position[1] + i * 30))

class HUDService:
    def __init__(self, screen, camera, map_width, map_height):
        font = pygame.font.SysFont("arial", 20, bold=True)
        self.resource_ui = ResourceUI(font, pos=(10, 10))
        self.minimap = MiniMap((screen.get_width() - 210, 10, 200, 200), camera)
        self.action_menu = ActionMenu(font, (10, screen.get_height() - 100))

    def set_actions(self, actions):
        self.action_menu.set_options(actions)

    def draw(self, screen):
        self.resource_ui.draw(screen)
        self.minimap.draw(screen)
        self.action_menu.draw(screen)
