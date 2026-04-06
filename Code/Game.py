import pygame
from Player import Player
from Whirlpool import WhirlpoolManager

pygame.init()


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shrimp Wizard")
clock = pygame.time.Clock()

player = Player(0, 0, 100, 50, 200)  # x, y, width, height, speed
whirlpool_manager = WhirlpoolManager()

running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds


    cameraX = player.x - WINDOW_WIDTH // 2
    cameraY = player.y - WINDOW_HEIGHT // 2


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        whirlpool_manager.handle_event(event, cameraX, cameraY)

    # update
    player.handle_input(dt)
    whirlpool_manager.update(dt, player)

    # draw
    window.fill((46, 110, 158))  # Background color
    whirlpool_manager.draw(window, cameraX, cameraY)
    player.draw(window, cameraX, cameraY)
    pygame.display.update()

pygame.quit()