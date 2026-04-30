import pygame
import math
import random
from pathlib import Path

from Player import Player
from Predator import Predator
from Whirlpool import WhirlpoolManager
from Algae import Algae
from EndScene import end_loop

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "Assets"


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def game_loop(window, clock, draw_text):

    # object creation
    player = Player(0, 0, 100, 50, 200)  # x, y, width, height, speed
    whirlpool_manager = WhirlpoolManager()


    # score
    score = 0
    scoreFont = pygame.font.Font(None, 36)

    # entity lists
    bubbles = []
    predators = []
    algae = []



    # game loop
    running = True
    while running:

        # game clock
        dt = clock.tick(60) / 1000.0
        

        # camera lock
        cameraX = player.x - WINDOW_WIDTH // 2
        cameraY = player.y - WINDOW_HEIGHT // 2

        # mouse tracker
        rawMouseX, rawMouseY = pygame.mouse.get_pos()
        mouseX = rawMouseX + cameraX
        mouseY = rawMouseY + cameraY


        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            whirlpool_manager.handle_event(event, cameraX, cameraY)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    bubble = player.shoot(mouseX, mouseY)
                    bubbles.append(bubble)


        # score handling
        score += dt
        scoreText = scoreFont.render(f"Score: {score:.0f}", True, (255, 255, 255))

        # enemy spawning
        xRange = [(-100, 50), (1230, 1380)]
        yRange = [(-100, 50), (680, 820)]
        xMin, xMax = random.choice(xRange)
        yMin, yMax = random.choice(yRange)
        if len(predators) < 5:
            predators.append(Predator(random.randint(xMin, xMax) + cameraX,random.randint(yMin, yMax) + cameraY, player, 
                                    random.choice(["fish", "squid", "crab"])))
            



        # algae spawning

        algaeXRange = cameraX + WINDOW_WIDTH
        algaeYRange = cameraY + WINDOW_HEIGHT

        if len(algae) < 20:
            algae.append(Algae(random.randint(int(cameraX), int(algaeXRange)), random.randint(int(cameraY), int(algaeYRange))))


        # update
        player.handle_input(dt)
        whirlpool_manager.update(dt, player)
        for predator in predators:
            predator.update(dt)
        for bubble in bubbles:
            bubble.update(dt)


        # collisions
        for bubble in bubbles:
            for predator in predators:
                dx = predator.x - bubble.x
                dy = predator.y - bubble.y
                dist = (dx*dx + dy*dy) ** 0.5

                if dist < predator.width / 2:
                    predator.stun()
                    bubble.alive = False
                    break

        bubbles = [bubble for bubble in bubbles if bubble.alive]

        for predator in predators:
                dx = predator.x - player.x
                dy = predator.y - player.y
                dist = (dx*dx + dy*dy) ** 0.5

                if dist < player.width / 2:
                    running = False
                    end_loop(window, clock, draw_text, game_loop, score)


        for alga in algae:
                dx = alga.x - player.x
                dy = alga.y - player.y
                dist = (dx*dx + dy*dy) ** 0.5

                if dist < player.width / 2:
                    score += alga.pointValue
                    alga.alive = False

        #entity culling
        for predator in predators:
            if (
                predator.x < cameraX - 400 or predator.x > cameraX + WINDOW_WIDTH + 400 or # Left Edge and Right Edge
                predator.y < cameraY - 400 or predator.y > cameraY + WINDOW_HEIGHT + 400 # Top Edge and Bottom Edge
            
            ):
                
                predator.alive = False

        predators = [p for p in predators if p.alive]

        for alga in algae:
            if (
                alga.x < cameraX - 400 or alga.x > cameraX + WINDOW_WIDTH + 400 or # Left Edge and Right Edge
                alga.y < cameraY - 400 or alga.y > cameraY + WINDOW_HEIGHT + 400 # Top Edge and Bottom Edge
            
            ):
                
                alga.alive = False

        algae = [a for a in algae if a.alive]


        # draw
        window.fill((46, 110, 158))  # Background color
        window.blit(scoreText, (600, 20))
        whirlpool_manager.draw(window, cameraX, cameraY)
        player.draw(window, cameraX, cameraY)
        for predator in predators:
            predator.draw(window, cameraX, cameraY)
        for bubble in bubbles:
            bubble.draw(window, cameraX, cameraY)
        for alga in algae:
            alga.draw(window, cameraX, cameraY)



        pygame.display.update()