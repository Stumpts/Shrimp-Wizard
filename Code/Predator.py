import pygame

class Predator: 
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

        self.image = pygame.image.load("assets/Predator.png")
        self.image = pygame.transform.scale(self.image, (width, height))

        self.vx = 0
        self.vy = 0