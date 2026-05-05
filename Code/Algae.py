import pygame
from pathlib import Path



_ASSETS_DIR = Path(__file__).resolve().parent.parent / "Assets"


class Algae:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.pointValue = 50
        self.alive = True

        self.image = pygame.image.load(_ASSETS_DIR / "algae.png")
        self.image = pygame.transform.scale(self.image, (30, 30))






    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float):
        surface.blit(self.image, (self.x - camera_x, self.y - camera_y))