import pygame
import sys

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Display Array")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Пример массива чисел
game_state = [3, 7, 1, 9, 2, 8, 4]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((50, 50, 50))

    # Преобразуем массив в строку без скобок, числа разделены пробелом
    text_str = " ".join(map(str, game_state))
    text_surface = font.render(text_str, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)