import pygame
from pathlib import Path

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "Assets"

def end_loop(window, clock, draw_text, game_loop, score):


    background = pygame.image.load(_ASSETS_DIR / "game_over_screen.png").convert()
    background = pygame.transform.scale(background, (1280, 720))


    while True:
        
        window.blit(background, (0, 0))

        mouse = pygame.mouse.get_pos()

       
        restart_button = pygame.Rect(510, 400, 200, 60)
        quit_button = pygame.Rect(510, 500, 200, 60)

        
        restart_color = (138, 208, 255) if restart_button.collidepoint(mouse) else (39, 169, 255)
        quit_color = (255, 167, 92) if quit_button.collidepoint(mouse) else (255, 127, 39)

        pygame.draw.rect(window, restart_color, restart_button)
        pygame.draw.rect(window, quit_color, quit_button)

        draw_text(f"YOUR SCORE: {int(score)}", 470, 310)

        draw_text("RESTART", 515, 410)
        draw_text("QUIT", 560, 510)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    game_loop(window, clock, draw_text)
                if quit_button.collidepoint(event.pos):
                    pygame.quit()

        pygame.display.flip()
        clock.tick(60)