# core.py
import pygame
from settings import load_settings
from game_state import GameState

class Core:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.settings = load_settings()
        self.state = GameState()

    @staticmethod
    def get():
        return Core()
