import pygame
import sys
from Logic import Game
from Screen import MainMenu, GameScreen, EndScreen

class GUI:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Spēle: Minimax / Alfa-Beta")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 48)

        self.game = Game()

        self.menu = MainMenu(self.screen, self.width, self.height, self.font)
        self.game_screen = GameScreen(self.screen, self.width, self.height, self.font, self.game)
        self.end_screen = EndScreen(self.screen, self.width, self.height, self.font, self.game)

        self.state = "menu"

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                if self.state == "menu":
                    started = self.menu.handle_event(event)
                    if started:
                        self.game.choose_length(self.menu.array_length)
                        # Выбор алгоритма: 1 - minimax, 2 - alfa-beta
                        self.game.set_algorithm(1 if self.menu.algorithm_switch.state else 2)
                        self.game.generate_numbers(self.menu.array_length)
                        if self.menu.start_player_switch.state:
                            self.game.max_player = "player"
                            self.game.current_turn = "player"
                        else:
                            self.game.max_player = "computer"
                            self.game.current_turn = "computer"
                        self.state = "game"
                elif self.state == "game":
                    self.game_screen.handle_event(event)
                elif self.state == "end":
                    restart = self.end_screen.handle_event(event)
                    if restart:
                        self.game.reset_game()
                        self.state = "menu"

    def update(self):
        if self.state == "menu":
            self.menu.update()
        elif self.state == "game":
            # Если текущий ход - "computer", выполняем его действие и переключаем ход на "player"
            if self.game.current_turn == "computer" and len(self.game.game_state) > 1:
                self.game.computer_move()
                self.game.current_turn = "player"
            self.game_screen.update()
            if len(self.game.game_state) <= 1:
                self.state = "end"
        elif self.state == "end":
            self.end_screen.update()

    def render(self):
        if self.state == "menu":
            self.menu.render()
        elif self.state == "game":
            self.game_screen.render()
        elif self.state == "end":
            self.end_screen.render()
        pygame.display.flip()

if __name__ == "__main__":
    gui = GUI()
    gui.run()















