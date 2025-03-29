import pygame
import sys
import random
from Logic import Game

class GUI:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Spēle: Minimax / Alfa-Beta")
        self.clock = pygame.time.Clock()
        self.running = True

        # Spēles stāvokļi: "menu", "game", "end"
        self.state = "menu"
        self.font = pygame.font.SysFont(None, 48)

        # Menu pogas un pārslēdzēji
        self.start_button = pygame.Rect(self.width // 2 - 100, 500, 200, 50)
        self.minus_button = pygame.Rect(self.width // 2 - 150, 200, 50, 50)
        self.plus_button = pygame.Rect(self.width // 2 + 100, 200, 50, 50)
        self.algorithm_button = pygame.Rect(self.width // 2 - 100, 270, 200, 50)
        self.start_player_button = pygame.Rect(self.width // 2 - 100, 340, 200, 50)
        self.play_again_button = pygame.Rect(self.width // 2 - 100, 300, 200, 50)

        self.array_length = 15
        self.algorithm_toggle = True  # True - minimax, False - alfa-beta
        self.algorithm_knob_width = 40
        self.algorithm_knob_y = self.algorithm_button.y + 5
        self.algorithm_knob_x = (self.algorithm_button.x + 5) if self.algorithm_toggle else (self.algorithm_button.x + self.algorithm_button.width - self.algorithm_knob_width - 5)
        self.algorithm_knob_target_x = self.algorithm_knob_x
        self.algorithm_knob_speed = 10

        # Pārslēdzējs, kurš sāk spēli: True - Spēlētājs, False - Dators
        self.start_player_toggle = True
        self.start_player_knob_width = 40
        self.start_player_knob_y = self.start_player_button.y + 5
        self.start_player_knob_x = (self.start_player_button.x + 5) if self.start_player_toggle else (self.start_player_button.x + self.start_player_button.width - self.start_player_knob_width - 5)
        self.start_player_knob_target_x = self.start_player_knob_x
        self.start_player_knob_speed = 10

        # Inicializējam spēles objektu (no Logic.py)
        self.game = Game()

        # Interaktīvai spēlei: uztveram, kurš no masīva elementiem tiek pārvietots
        self.dragging_index = None
        self.drag_start_x = 0
        self.drag_dx = 0
        self.drag_threshold = 30  # pikseļi

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Ierobežo FPS līdz 60
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.state == "menu":
                    if self.minus_button.collidepoint(pos):
                        self.array_length = max(15, self.array_length - 1)
                    elif self.plus_button.collidepoint(pos):
                        self.array_length = min(25, self.array_length + 1)
                    elif self.algorithm_button.collidepoint(pos):
                        self.algorithm_toggle = not self.algorithm_toggle
                        if self.algorithm_toggle:
                            self.algorithm_knob_target_x = self.algorithm_button.x + 5
                        else:
                            self.algorithm_knob_target_x = self.algorithm_button.x + self.algorithm_button.width - self.algorithm_knob_width - 5
                    elif self.start_player_button.collidepoint(pos):
                        self.start_player_toggle = not self.start_player_toggle
                        if self.start_player_toggle:
                            self.start_player_knob_target_x = self.start_player_button.x + 5
                        else:
                            self.start_player_knob_target_x = self.start_player_button.x + self.start_player_button.width - self.start_player_knob_width - 5
                    elif self.start_button.collidepoint(pos):
                        # Sākam spēli, nododot izvēlētos parametrus Game objektam
                        self.state = "game"
                        self.game.choose_length(self.array_length)
                        self.game.set_algorithm(1 if self.algorithm_toggle else 2)
                        self.game.generate_numbers(self.array_length)
                        # Iestata, kurš sāk spēli, pēc pārslēdzēja vērtības:
                        if self.start_player_toggle:
                            self.game.max_player = "player"
                            self.game.current_turn = "player"
                        else:
                            self.game.max_player = "computer"
                            self.game.current_turn = "computer"
                    # Spēles stāvoklī pārbaudam, vai lietotājs sāk vilkt skaitli
                elif self.state == "game":
                    if event.button == 1:  # kreisais klikšķis
                        mouse_x, mouse_y = event.pos
                        number_rects = self.get_number_rects()
                        for idx, rect in enumerate(number_rects):
                            if rect.collidepoint(mouse_x, mouse_y):
                                self.dragging_index = idx
                                self.drag_start_x = mouse_x
                                self.drag_dx = 0
                                break

                elif self.state == "end":
                    if self.play_again_button.collidepoint(pos):
                        # Resetē spēles datus un atgriežas uz menu
                        self.game.reset_game()
                        self.state = "menu"

            elif event.type == pygame.MOUSEMOTION:
                if self.state == "game" and self.dragging_index is not None:
                    mouse_x, _ = event.pos
                    self.drag_dx = mouse_x - self.drag_start_x

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.state == "game" and event.button == 1 and self.dragging_index is not None:
                    # Ja vilkšana pietiekami liela, apvieno ar kreiso vai labo blakus esošo elementu
                    if self.drag_dx < -self.drag_threshold and self.dragging_index > 0:
                        self.merge_pair(self.dragging_index, "left")
                        self.game.computer_move()
                    elif self.drag_dx > self.drag_threshold and self.dragging_index < len(self.game.game_state) - 1:
                        self.merge_pair(self.dragging_index, "right")
                        self.game.computer_move()
                    self.dragging_index = None
                    self.drag_dx = 0

    def update(self):
        # Animācija pārslēdzēju slīdņiem menu
        if self.algorithm_knob_x < self.algorithm_knob_target_x:
            self.algorithm_knob_x += self.algorithm_knob_speed
            if self.algorithm_knob_x > self.algorithm_knob_target_x:
                self.algorithm_knob_x = self.algorithm_knob_target_x
        elif self.algorithm_knob_x > self.algorithm_knob_target_x:
            self.algorithm_knob_x -= self.algorithm_knob_speed
            if self.algorithm_knob_x < self.algorithm_knob_target_x:
                self.algorithm_knob_x = self.algorithm_knob_target_x

        if self.start_player_knob_x < self.start_player_knob_target_x:
            self.start_player_knob_x += self.start_player_knob_speed
            if self.start_player_knob_x > self.start_player_knob_target_x:
                self.start_player_knob_x = self.start_player_knob_target_x
        elif self.start_player_knob_x > self.start_player_knob_target_x:
            self.start_player_knob_x -= self.start_player_knob_speed
            if self.start_player_knob_x < self.start_player_knob_target_x:
                self.start_player_knob_x = self.start_player_knob_target_x

        # Spēles loģika spēles stāvoklī "game"
        if self.state == "game":
            # Ja masīvs ir garāks par vienu, spēle turpinās; citādi – beidzas
            if len(self.game.game_state) <= 1:
                self.state = "end"

    def render(self):
        if self.state == "menu":
            self.render_menu()
        elif self.state == "game":
            self.render_game()
        elif self.state == "end":
            self.render_end()
        pygame.display.flip()

    def render_menu(self):
        self.screen.fill((30, 30, 30))
        title_text = self.font.render("Galvenā izvēlne", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # Masīva garums
        prompt_text = self.font.render("Masīva garums:", True, (255, 255, 255))
        self.screen.blit(prompt_text, (self.width // 2 - prompt_text.get_width() // 2, 120))
        pygame.draw.rect(self.screen, (100, 100, 200), self.minus_button)
        minus_text = self.font.render("-", True, (255, 255, 255))
        self.screen.blit(minus_text, (self.minus_button.x + (self.minus_button.width - minus_text.get_width()) // 2,
                                       self.minus_button.y + (self.minus_button.height - minus_text.get_height()) // 2))
        pygame.draw.rect(self.screen, (100, 100, 200), self.plus_button)
        plus_text = self.font.render("+", True, (255, 255, 255))
        self.screen.blit(plus_text, (self.plus_button.x + (self.plus_button.width - plus_text.get_width()) // 2,
                                      self.plus_button.y + (self.plus_button.height - plus_text.get_height()) // 2))
        value_text = self.font.render(str(self.array_length), True, (255, 255, 255))
        value_x = self.width // 2 - value_text.get_width() // 2
        value_y = self.minus_button.y + (self.minus_button.height - value_text.get_height()) // 2
        self.screen.blit(value_text, (value_x, value_y))

        # Algoritma pārslēdzējs
        pygame.draw.rect(self.screen, (80, 80, 80), self.algorithm_button, border_radius=25)
        alg_knob_rect = pygame.Rect(self.algorithm_knob_x, self.algorithm_button.y + 5, self.algorithm_knob_width, self.algorithm_button.height - 10)
        pygame.draw.rect(self.screen, (200, 200, 200), alg_knob_rect, border_radius=20)
        left_label = self.font.render("alpha-beta", True, (255, 255, 255))
        right_label = self.font.render("minimax", True, (255, 255, 255))
        self.screen.blit(left_label, (self.algorithm_button.x - left_label.get_width() - 10,
                                      self.algorithm_button.y + (self.algorithm_button.height - left_label.get_height()) // 2))
        self.screen.blit(right_label, (self.algorithm_button.right + 10,
                                       self.algorithm_button.y + (self.algorithm_button.height - right_label.get_height()) // 2))

        # Spēles sākuma pārslēdzējs
        pygame.draw.rect(self.screen, (80, 80, 80), self.start_player_button, border_radius=25)
        sp_knob_rect = pygame.Rect(self.start_player_knob_x, self.start_player_button.y + 5, self.start_player_knob_width, self.start_player_button.height - 10)
        pygame.draw.rect(self.screen, (200, 200, 200), sp_knob_rect, border_radius=20)
        left_label2 = self.font.render("Spēlētājs", True, (255, 255, 255))
        right_label2 = self.font.render("Dators", True, (255, 255, 255))
        self.screen.blit(left_label2, (self.start_player_button.x - left_label2.get_width() - 10,
                                       self.start_player_button.y + (self.start_player_button.height - left_label2.get_height()) // 2))
        self.screen.blit(right_label2, (self.start_player_button.right + 10,
                                        self.start_player_button.y + (self.start_player_button.height - right_label2.get_height()) // 2))

        # Sākt spēli poga
        pygame.draw.rect(self.screen, (100, 100, 200), self.start_button)
        start_text = self.font.render("Sākt spēli", True, (255, 255, 255))
        self.screen.blit(start_text, (self.start_button.x + (self.start_button.width - start_text.get_width()) // 2,
                                      self.start_button.y + (self.start_button.height - start_text.get_height()) // 2))

    def get_number_rects(self):
        """
        Aprēķina katra skaitļa taisnstūrus, lai tie tiktu atveidoti horizontāli pa ekrāna centru
        ar atstarpi starp tiem.
        """
        rects = []
        spacing = 20
        texts = []
        total_width = 0
        for num in self.game.game_state:
            text_surface = self.font.render(str(num), True, (255, 255, 255))
            texts.append(text_surface)
            total_width += text_surface.get_width() + spacing
        total_width -= spacing  # pēdējā atstarpe nav nepieciešama
        start_x = (self.width - total_width) // 2
        y = self.height // 2
        current_x = start_x
        for text_surface in texts:
            rect = text_surface.get_rect(topleft=(current_x, y))
            rects.append(rect)
            current_x += text_surface.get_width() + spacing
        return rects

    def merge_pair(self, index, direction):
        """
        Apvieno divus blakus esošus skaitļus pēc noteikumiem:
         - Ja summa > 7: rezultāts 1
         - Ja summa < 7: rezultāts 3
         - Ja summa == 7: rezultāts 2
        """
        if direction == "left" and index > 0:
            a = self.game.game_state[index - 1]
            b = self.game.game_state[index]
            s = a + b
            new_val = 1 if s > 7 else 3 if s < 7 else 2
            self.game.game_state.pop(index)
            self.game.game_state[index - 1] = new_val
        elif direction == "right" and index < len(self.game.game_state) - 1:
            a = self.game.game_state[index]
            b = self.game.game_state[index + 1]
            s = a + b
            new_val = 1 if s > 7 else 3 if s < 7 else 2
            self.game.game_state[index] = new_val
            self.game.game_state.pop(index + 1)
        print("Atjaunotais masīvs:", self.game.game_state)

    def render_game(self):
        self.screen.fill((50, 50, 50))
        title_text = self.font.render("Spēles ekrāns", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))
        number_rects = self.get_number_rects()
        for idx, rect in enumerate(number_rects):
            text_surface = self.font.render(str(self.game.game_state[idx]), True, (255, 255, 255))
            # Ja šis skaitlis tiek pārvietots, pielāgo tā pozīciju
            if idx == self.dragging_index:
                moved_rect = rect.move(self.drag_dx, 0)
                self.screen.blit(text_surface, moved_rect)
            else:
                self.screen.blit(text_surface, rect)
        # Parādām arī rezultātus (punktus)
        score_text = self.font.render(f"Spēlētājs: {self.game.player_score}  Banka: {self.game.bank_score}", True, (200, 200, 200))
        self.screen.blit(score_text, (50, 250))

    def render_end(self):
        self.screen.fill((30, 30, 30))
        end_text = self.font.render("Spēle beigusies", True, (255, 255, 255))
        self.screen.blit(end_text, (self.width // 2 - end_text.get_width() // 2, 50))
        # Aprēķina uzvarētāju, izmantojot terminal_eval funkciju no Game
        result = self.game.terminal_eval({
            "player_score": self.game.player_score,
            "bank_score": self.game.bank_score
        })
        if result == 1:
            winner = self.game.max_player
        elif result == -1:
            winner = "player" if self.game.max_player == "computer" else "computer"
        else:
            winner = "Neizšķirts"
        winner_text = self.font.render("Uzvar: " + winner, True, (255, 255, 255))
        self.screen.blit(winner_text, (self.width // 2 - winner_text.get_width() // 2, 150))
        pygame.draw.rect(self.screen, (200, 100, 100), self.play_again_button)
        replay_text = self.font.render("Spēlēt vēlreiz", True, (255, 255, 255))
        self.screen.blit(replay_text, (self.play_again_button.x + (self.play_again_button.width - replay_text.get_width()) // 2,
                                       self.play_again_button.y + (self.play_again_button.height - replay_text.get_height()) // 2))

if __name__ == "__main__":
    gui = GUI()
    gui.run()















