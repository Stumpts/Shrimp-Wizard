import pygame

class Algae:
    def __init__(self, x, y, width, height, speed, pointValue):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.pointValue = pointValue

        self.image = pygame.image.load("assets/Algae.png")
        self.image = pygame.transform.scale(self.image, (width, height))

        self.vx = 0
        self.vy = 0