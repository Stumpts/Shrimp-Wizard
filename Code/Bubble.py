import pygame

# bubble to shoot at predators to stun them

class Bubble:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 500

        self.vx = 0
        self.vy = 0

        self.radius = 5
        self.alive = True

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt



    def draw(self, surface, camera_x, camera_y):
        pygame.draw.circle(surface, (0, 0, 255), (int(self.x - camera_x), int(self.y - camera_y)), self.radius)