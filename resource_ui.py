# vtm_game/resource_ui.py
import pygame
from core import Core

class ResourceUI:
    def __init__(self, font, pos=(10,10), spacing=30,
                 col_blood=(200,0,0), col_money=(255,215,0)):
        self.font       = font
        self.pos_blood  = pos
        self.pos_money  = (pos[0], pos[1] + spacing)
        self.col_blood  = col_blood
        self.col_money  = col_money

    def draw(self, screen):
        state = Core.get().state
        b_surf = self.font.render(f"Blood: {state.blood}", True, self.col_blood)
        m_surf = self.font.render(f"Money: {state.money}", True, self.col_money)
        screen.blit(b_surf, self.pos_blood)
        screen.blit(m_surf, self.pos_money)
