import pygame
from resource_ui import ResourceUI
import os
import sys
from core import Core
from camera_service import CameraService
from hud import HUDService

WIDTH, HEIGHT = 1200, 900
TILE_WIDTH, TILE_HEIGHT = 48, 24
COLUMNS, ROWS = 50, 50

TREES = [(5, 5), (7, 7), (10, 12), (20, 20), (35, 41)]
STRONGPOINTS = [(12, 8), (27, 35), (42, 10)]
CITIES = {"camarilla": (8, 44), "sabbat": (44, 8)}

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_texture(name):
    return pygame.image.load(resource_path(f"textures/{name}")).convert_alpha()

def texas_map_loop(screen):
    pygame.display.set_caption("Осада Техаса — Карта 50x50")
    clock = pygame.time.Clock()
    soil_tile = load_texture("soil_tile_48x24.png")
    camera = CameraService(0, 0, speed=32, map_width=COLUMNS*TILE_WIDTH, map_height=ROWS*TILE_HEIGHT,
                           screen_width=WIDTH, screen_height=HEIGHT, margin=100)
    font = pygame.font.SysFont("arial", 24, bold=True)
    # res_ui = ResourceUI(font)
    hud = HUDService(screen, camera, COLUMNS*TILE_WIDTH, ROWS*TILE_HEIGHT)
    selected = None
    running = True
    dragging = False
    last_mouse = (0, 0)

    def cart_to_iso(x, y):
        iso_x = (x - y) * TILE_WIDTH // 2
        iso_y = (x + y) * TILE_HEIGHT // 2
        return iso_x, iso_y

    def world_to_screen(wx, wy):
        return wx - camera.x + WIDTH // 2, wy - camera.y + 60

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                last_mouse = event.pos
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                camera.x -= dx
                camera.y -= dy
                last_mouse = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = event.pos
                # (оставь обработку выбора клетки по своему шаблону)

        screen.fill((30, 0, 0))

        # Рисуем карту
        for y in range(ROWS):
            for x in range(COLUMNS):
                iso_x, iso_y = cart_to_iso(x, y)
                sx, sy = world_to_screen(iso_x, iso_y)
                rect = soil_tile.get_rect(center=(sx, sy + TILE_HEIGHT // 2))
                screen.blit(soil_tile, rect)

        # Деревья
        for tx, ty in TREES:
            iso_x, iso_y = cart_to_iso(tx, ty)
            sx, sy = world_to_screen(iso_x, iso_y)
            pygame.draw.circle(screen, (0, 180, 0),
                               (sx, sy + TILE_HEIGHT//2), 13)
            screen.blit(font.render("T", True, (0, 60, 0)), (sx - 8, sy + 2))

        # Опорные точки
        for tx, ty in STRONGPOINTS:
            iso_x, iso_y = cart_to_iso(tx, ty)
            sx, sy = world_to_screen(iso_x, iso_y)
            pygame.draw.rect(screen, (255, 190, 0), (sx - 12, sy + 3, 25, 14))
            screen.blit(font.render("O", True, (120, 60, 0)), (sx - 7, sy + 3))

        # Города
        for label, (tx, ty) in CITIES.items():
            iso_x, iso_y = cart_to_iso(tx, ty)
            sx, sy = world_to_screen(iso_x, iso_y)
            color = (120, 120, 255) if label == "camarilla" else (200, 40, 40)
            pygame.draw.circle(screen, color, (sx, sy + TILE_HEIGHT//2), 19)
            txt = font.render(
                "C" if label == "camarilla" else "S", True, (255, 255, 255))
            screen.blit(txt, (sx - 10, sy - 2))
            screen.blit(
                font.render(label.capitalize(), True, color),
                (sx + 20, sy - 10)
            )

        hud.draw(screen)
        pygame.display.flip()
        clock.tick(60)