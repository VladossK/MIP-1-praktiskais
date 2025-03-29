import pygame
from collections import defaultdict, deque


class MainMenu:
    def __init__(self, screen, width, height, font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font

        # Кнопки для изменения длины массива
        self.minus_button = pygame.Rect(self.width // 2 - 150, 200, 50, 50)
        self.plus_button = pygame.Rect(self.width // 2 + 100, 200, 50, 50)
        self.array_length = 15

        # Переключатель алгоритма: True = minimax, False = alfa-beta
        self.algorithm_switch = ToggleSwitch((self.width // 2 - 100, 270, 200, 50), initial_state=True)

        # Переключатель того, кто начинает игру: True = Spēlētājs, False = Dators
        self.start_player_switch = ToggleSwitch((self.width // 2 - 100, 340, 200, 50), initial_state=True)

        # Кнопка "Sākt spēli"
        self.start_button = pygame.Rect(self.width // 2 - 100, 500, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.minus_button.collidepoint(pos):
                self.array_length = max(15, self.array_length - 1)
            elif self.plus_button.collidepoint(pos):
                self.array_length = min(25, self.array_length + 1)
            elif self.algorithm_switch.rect.collidepoint(pos):
                self.algorithm_switch.toggle()
            elif self.start_player_switch.rect.collidepoint(pos):
                self.start_player_switch.toggle()
            elif self.start_button.collidepoint(pos):
                return True  # сигнал на запуск игры
        return False

    def update(self):
        self.algorithm_switch.update()
        self.start_player_switch.update()

    def render(self):
        self.screen.fill((30, 30, 30))
        title_surface = self.font.render("Galvenā izvēlne", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 50))
        # Отрисовка изменения длины массива
        prompt_surface = self.font.render("Masīva garums:", True, (255, 255, 255))
        self.screen.blit(prompt_surface, (self.width // 2 - prompt_surface.get_width() // 2, 120))
        pygame.draw.rect(self.screen, (100, 100, 200), self.minus_button)
        minus_surface = self.font.render("-", True, (255, 255, 255))
        self.screen.blit(minus_surface,
                         (self.minus_button.x + (self.minus_button.width - minus_surface.get_width()) // 2,
                          self.minus_button.y + (self.minus_button.height - minus_surface.get_height()) // 2))
        pygame.draw.rect(self.screen, (100, 100, 200), self.plus_button)
        plus_surface = self.font.render("+", True, (255, 255, 255))
        self.screen.blit(plus_surface, (self.plus_button.x + (self.plus_button.width - plus_surface.get_width()) // 2,
                                        self.plus_button.y + (
                                                    self.plus_button.height - plus_surface.get_height()) // 2))
        length_surface = self.font.render(str(self.array_length), True, (255, 255, 255))
        self.screen.blit(length_surface, (self.width // 2 - length_surface.get_width() // 2,
                                          self.minus_button.y + (
                                                      self.minus_button.height - length_surface.get_height()) // 2))
        # Отрисовка переключателей
        self.algorithm_switch.render(self.screen, "alpha-beta", "minimax", self.font)
        self.start_player_switch.render(self.screen, "Spēlētājs", "Dators", self.font)
        # Кнопка "Sākt spēli"
        pygame.draw.rect(self.screen, (100, 100, 200), self.start_button)
        start_surface = self.font.render("Sākt spēli", True, (255, 255, 255))
        self.screen.blit(start_surface,
                         (self.start_button.x + (self.start_button.width - start_surface.get_width()) // 2,
                          self.start_button.y + (self.start_button.height - start_surface.get_height()) // 2))


class GameScreen:
    def __init__(self, screen, width, height, font, game_logic):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.game = game_logic  # Экземпляр Game из Logic.py

        # Для интерактивного перемещения чисел:
        self.dragging_index = None
        self.drag_start_x = 0
        self.drag_dx = 0
        self.drag_threshold = 30  # пиксели

    def get_number_rects(self):
        rects = []
        spacing = 20
        texts = []
        total_width = 0
        for num in self.game.game_state:
            text_surface = self.font.render(str(num), True, (255, 255, 255))
            texts.append(text_surface)
            total_width += text_surface.get_width() + spacing
        total_width -= spacing  # последний пробел не нужен

        # Если требуемая ширина больше экрана, вычисляем коэффициент масштабирования
        scale = 1.0
        if total_width > self.width:
            scale = self.width / total_width

        start_x = int((self.width - total_width * scale) // 2)
        y = self.height // 2
        current_x = start_x
        for text_surface in texts:
            # Используем оригинальную ширину для расчёта, но с учетом коэффициента масштабирования
            scaled_width = int(text_surface.get_width() * scale)
            rect = text_surface.get_rect(topleft=(current_x, y))
            rects.append(rect)
            current_x += scaled_width + int(spacing * scale)
        return rects

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка мыши
                mouse_x, mouse_y = event.pos
                rects = self.get_number_rects()
                for idx, rect in enumerate(rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.dragging_index = idx
                        self.drag_start_x = mouse_x
                        self.drag_dx = 0
                        break
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_index is not None:
                mouse_x, _ = event.pos
                self.drag_dx = mouse_x - self.drag_start_x
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging_index is not None:
                if self.drag_dx < -self.drag_threshold and self.dragging_index > 0:
                    self.merge_pair(self.dragging_index, "left")
                elif self.drag_dx > self.drag_threshold and self.dragging_index < len(self.game.game_state) - 1:
                    self.merge_pair(self.dragging_index, "right")
                # После хода игрока вызывается ход компьютера
                self.game.computer_move()
                self.dragging_index = None
                self.drag_dx = 0

    def merge_pair(self, index, direction):
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

    def update(self):
        pass

    def render(self):
        self.screen.fill((50, 50, 50))
        # Virsraksts
        title_surface = self.font.render("Spēles ekrāns", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 50))

        # Attēlo, kurš gājiens (spēlētājs/dators)
        turn_text = f"Gājiens: {'Spēlētājs' if self.game.current_turn == 'player' else 'Dators'}"
        turn_surface = self.font.render(turn_text, True, (255, 255, 255))
        self.screen.blit(turn_surface, (self.width // 2 - turn_surface.get_width() // 2, 10))

        # Attēlo masīvu ar skaitļiem
        rects = self.get_number_rects()
        for idx, rect in enumerate(rects):
            text_surface = self.font.render(str(self.game.game_state[idx]), True, (255, 255, 255))
            # Ja šis elements pieder pie apstrādājamās pāra (highlight), zīmē apmali
            if (hasattr(self.game, "highlight_pair_index") and
                    self.game.highlight_pair_index is not None and
                    (idx == self.game.highlight_pair_index or idx == self.game.highlight_pair_index + 1)):
                # Zīmē sarkanu apmali ap elementu
                pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(10, 10), 2)
            # Zīmē skaitļa tekstu
            if idx == self.dragging_index:
                moved_rect = rect.move(self.drag_dx, 0)
                self.screen.blit(text_surface, moved_rect)
            else:
                self.screen.blit(text_surface, rect)

        # Atrast masīva apakšējo robežu, lai komentārs tiktu novietots zem tā
        if rects:
            array_bottom = max(rect.bottom for rect in rects)
        else:
            array_bottom = self.height // 2

        # Attēlo datora gājiņa komentāru zem masīva
        if hasattr(self.game, "last_computer_move") and self.game.last_computer_move:
            import textwrap
            comment = self.game.last_computer_move
            wrapped_lines = textwrap.wrap(comment, width=40)  # pielāgo platumu pēc vajadzības
            y_comment = array_bottom + 20  # atstarpe zem masīva
            for line in wrapped_lines:
                comment_surface = self.font.render(line, True, (255, 255, 0))
                self.screen.blit(comment_surface, (self.width // 2 - comment_surface.get_width() // 2, y_comment))
                y_comment += comment_surface.get_height() + 5

        # Attēlo divus skaitītājus kreisajā apakšā (katrs atsevišķā rindā)
        margin = 20
        player_score_surface = self.font.render(f"Spēlētājs: {self.game.player_score}", True, (200, 200, 200))
        bank_score_surface = self.font.render(f"Banka: {self.game.bank_score}", True, (200, 200, 200))
        y_player = self.height - player_score_surface.get_height() - bank_score_surface.get_height() - margin
        y_bank = self.height - bank_score_surface.get_height() - margin
        self.screen.blit(player_score_surface, (margin, y_player))
        self.screen.blit(bank_score_surface, (margin, y_bank))


class EndScreen:
    def __init__(self, screen, width, height, font, game_logic):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.game = game_logic
        self.play_again_button = pygame.Rect(self.width // 2 - 100, 300, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.play_again_button.collidepoint(pos):
                return True
        return False

    def update(self):
        pass

    def render(self):
        self.screen.fill((30, 30, 30))
        end_surface = self.font.render("Spēle beigusies", True, (255, 255, 255))
        self.screen.blit(end_surface, (self.width // 2 - end_surface.get_width() // 2, 50))

        # Определяем победителя с учётом трёх вариантов: "Dators", "Spēlētājs", "Draw"
        result = self.game.terminal_eval({
            "player_score": self.game.player_score,
            "bank_score": self.game.bank_score
        })
        if result == 1:
            winner = "Spēlētājs" if self.game.max_player == "player" else "Dators"
        elif result == -1:
            winner = "Dators" if self.game.max_player == "player" else "Spēlētājs"
        else:
            winner = "Draw"

        winner_surface = self.font.render("Uzvar: " + winner, True, (255, 255, 255))
        self.screen.blit(winner_surface, (self.width // 2 - winner_surface.get_width() // 2, 150))

        pygame.draw.rect(self.screen, (200, 100, 100), self.play_again_button)
        replay_surface = self.font.render("Spēlēt vēlreiz", True, (255, 255, 255))
        self.screen.blit(replay_surface,
                         (self.play_again_button.x + (self.play_again_button.width - replay_surface.get_width()) // 2,
                          self.play_again_button.y + (
                                      self.play_again_button.height - replay_surface.get_height()) // 2))


class ToggleSwitch:
    def __init__(self, rect, initial_state=True, knob_width=40, knob_speed=10):
        self.rect = pygame.Rect(rect)
        self.state = initial_state
        self.knob_width = knob_width
        self.knob_speed = knob_speed
        self.knob_y = self.rect.y + 5
        if self.state:
            self.knob_x = self.rect.x + 5
        else:
            self.knob_x = self.rect.x + self.rect.width - self.knob_width - 5
        self.target_x = self.knob_x

    def toggle(self):
        self.state = not self.state
        if self.state:
            self.target_x = self.rect.x + 5
        else:
            self.target_x = self.rect.x + self.rect.width - self.knob_width - 5

    def update(self):
        if self.knob_x < self.target_x:
            self.knob_x += self.knob_speed
            if self.knob_x > self.target_x:
                self.knob_x = self.target_x
        elif self.knob_x > self.target_x:
            self.knob_x -= self.knob_speed
            if self.knob_x < self.target_x:
                self.knob_x = self.target_x

    def render(self, screen, left_label, right_label, font):
        pygame.draw.rect(screen, (80, 80, 80), self.rect, border_radius=25)
        knob_rect = pygame.Rect(self.knob_x, self.rect.y + 5, self.knob_width, self.rect.height - 10)
        pygame.draw.rect(screen, (200, 200, 200), knob_rect, border_radius=20)
        left_surface = font.render(left_label, True, (255, 255, 255))
        right_surface = font.render(right_label, True, (255, 255, 255))
        screen.blit(left_surface, (self.rect.x - left_surface.get_width() - 10,
                                   self.rect.y + (self.rect.height - left_surface.get_height()) // 2))
        screen.blit(right_surface, (self.rect.right + 10,
                                    self.rect.y + (self.rect.height - right_surface.get_height()) // 2))
