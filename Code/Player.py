import pygame

class Player:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

        self.image = pygame.image.load("assets/shrimp.png")
        self.image = pygame.transform.scale(self.image, (width, height))

        self.vx = 0
        self.vy = 0

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0

        if keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_s]:
            move_y += 1
        if keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_d]:
            move_x += 1

        if move_x != 0 and move_y != 0:
            move_x = 0.7071
            move_y= 0.7071

        self.vx += move_x * self.speed * dt
        self.vy += move_y * self.speed * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vx = 0.9
        self.vy= 0.9

    def draw(self, window, camera_x, camera_y):
        window.blit(self.image, (self.x - camera_x, self.y - camera_y))