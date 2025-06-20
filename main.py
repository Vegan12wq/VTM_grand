
import pygame
from game_manager import run_game

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    run_game(screen)
