import pygame
from GameScene import game_loop
from pathlib import Path


pygame.init()

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "Assets"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shrimp Wizard")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 60)

background = pygame.image.load(_ASSETS_DIR / "title_screen.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    window.blit(img, (x, y))

def main_menu():
    while True:
        
        window.blit(background, (0, 0))

        mouse = pygame.mouse.get_pos()

        
        start_button = pygame.Rect(510, 400, 200, 60)
        quit_button = pygame.Rect(510, 500, 200, 60)

        
        start_color = (138, 208, 255) if start_button.collidepoint(mouse) else (39, 169, 255)
        quit_color = (255, 167, 92) if quit_button.collidepoint(mouse) else (255, 127, 39)

        pygame.draw.rect(window, start_color, start_button)
        pygame.draw.rect(window, quit_color, quit_button)


        draw_text("START", 540, 410)
        draw_text("QUIT", 560, 510)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_loop(window, clock, draw_text)
                if quit_button.collidepoint(event.pos):
                    pygame.quit()

        pygame.display.flip()
        clock.tick(60)

main_menu()