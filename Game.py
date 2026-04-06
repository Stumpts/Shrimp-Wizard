import pygame
from Player import Player

pygame.init()

windowWidth = 1280
windowHeight = 720
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Shrimp Wizard")

player = Player(0, 0, 10, 10, 10)

running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.handle_input()

    cameraX = player.x - windowWidth // 2
    cameraY = player.y - windowHeight // 2

    window.fill((46, 110, 158))
    #player.draw(window, cameraX, cameraY) # camera locked
    player.draw(window) # camera locked  # camera unlocked

    pygame.display.update()

pygame.quit()