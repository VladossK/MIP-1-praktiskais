import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Template")

# Clock to control frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Buttons
player_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
computer_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
minimax_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
alphabeta_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

# Game state variables
running = True

# Game loop
while running:
    # --- Ask for sequence length ---
    input_active = True
    input_text = ""
    sequence_length = None

    while input_active:
        screen.fill(WHITE)
        prompt = font.render("Enter sequence length (15-25):", True, BLACK)
        input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
        pygame.draw.rect(screen, GRAY, input_box)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        val = int(input_text)
                        if 15 <= val <= 25:
                            sequence_length = val
                            input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # --- First menu ---
    player_first = None
    while player_first is None:
        screen.fill(WHITE)
        text = font.render("Who will start?", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, RED, player_button)
        pygame.draw.rect(screen, BLUE, computer_button)
        screen.blit(font.render("Player", True, WHITE), (player_button.x + 50, player_button.y + 10))
        screen.blit(font.render("Computer", True, WHITE), (computer_button.x + 30, computer_button.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_button.collidepoint(event.pos):
                    player_first = True
                elif computer_button.collidepoint(event.pos):
                    player_first = False

    # --- Algorithm menu ---
    algorithm = None
    while algorithm is None:
        screen.fill(WHITE)
        text = font.render("Which algorithm will be used?", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, GREEN, minimax_button)
        pygame.draw.rect(screen, BLUE, alphabeta_button)
        screen.blit(font.render("Minimax", True, WHITE), (minimax_button.x + 50, minimax_button.y + 10))
        screen.blit(font.render("Alpha-Beta", True, WHITE), (alphabeta_button.x + 30, alphabeta_button.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if minimax_button.collidepoint(event.pos):
                    algorithm = "minimax"
                elif alphabeta_button.collidepoint(event.pos):
                    algorithm = "alphabeta"

    # --- Start Game ---
    sequence = [random.randint(0, 9) for _ in range(sequence_length)]
    score = 0
    bank = 0
    winner_text = ""
    turn_player = player_first

    game_over = False
    while not game_over:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if winner_text and play_again_button.collidepoint(event.pos):
                    game_over = True  # Break to restart full loop
                elif turn_player and len(sequence) > 1 and not winner_text:
                    mouse_x, mouse_y = event.pos
                    spacing = 30
                    offset_x = 50
                    for i in range(len(sequence) - 1):
                        rect = pygame.Rect(offset_x + i * spacing, HEIGHT // 2, spacing * 2, 40)
                        if rect.collidepoint(mouse_x, mouse_y):
                            a, b = sequence[i], sequence[i + 1]
                            total = a + b
                            if total > 7:
                                sequence[i:i+2] = [total]
                                score += 1
                            elif total < 7:
                                sequence[i:i+2] = [abs(a - b)]
                                score -= 1
                            else:
                                sequence[i:i+2] = [a * 2]
                                bank += 1
                            turn_player = False
                            break

        if not turn_player and len(sequence) > 1 and not winner_text:
            i = random.randint(0, len(sequence) - 2)
            a, b = sequence[i], sequence[i + 1]
            total = a + b
            if total > 7:
                sequence[i:i+2] = [total]
                score += 1
            elif total < 7:
                sequence[i:i+2] = [abs(a - b)]
                score -= 1
            else:
                sequence[i:i+2] = [a * 2]
                bank += 1
            turn_player = True

        # Display
        starter_text = "Player starts" if player_first else "Computer starts"
        screen.blit(font.render(f"{starter_text} | Algorithm: {algorithm}", True, BLACK), (20, 20))
        screen.blit(font.render(f"Score: {score} | Bank: {bank}", True, BLACK), (20, 60))

        spacing = 30
        offset_x = 50
        for i, num in enumerate(sequence):
            rect = pygame.Rect(offset_x + i * spacing, HEIGHT // 2, 25, 40)
            pygame.draw.rect(screen, GRAY, rect)
            screen.blit(font.render(str(num), True, BLACK), (rect.x + 5, rect.y + 5))

        if len(sequence) == 1 and not winner_text:
            if bank > 0:
                if score % 2 == 0:
                    winner_text = "Player wins" if player_first else "Computer wins"
                else:
                    winner_text = "Computer wins" if player_first else "Player wins"
            else:
                winner_text = "Draw"

        if winner_text:
            screen.blit(font.render(f"Game Over: {winner_text}", True, RED), (WIDTH // 2 - 100, HEIGHT - 150))
            pygame.draw.rect(screen, GREEN, play_again_button)
            screen.blit(font.render("Play Again", True, WHITE), (play_again_button.x + 40, play_again_button.y + 10))

        pygame.display.flip()

pygame.quit()