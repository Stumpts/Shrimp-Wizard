import pygame

class Player:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    #def draw(self, window, camera_x, camera_y):        # locked draw
        #pygame.draw.rect( window, (255, 255, 255), (self.x - camera_x, self.y - camera_y, self.width, self.height))

    def draw(self, window):                              # unlocked draw
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y, self.width, self.height))