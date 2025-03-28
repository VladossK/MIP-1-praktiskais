import pygame
import sys


class GUI:
    """
    Класс GUI управляет игровым окном с помощью pygame и обеспечивает три экрана:
      - Главное меню (здесь можно задать параметры игры),
      - Игровой экран,
      - Экран завершения игры.
    """

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Spēle: Minimax / Alfa-Beta")
        self.clock = pygame.time.Clock()
        self.running = True

        # Состояние игры: "menu" - главное меню, "game" - игровой экран, "end" - экран завершения
        self.state = "menu"

        # Инициализация шрифта для отображения текста
        self.font = pygame.font.SysFont(None, 48)

        # Кнопки главного меню
        self.start_button = pygame.Rect(self.width // 2 - 100, 400, 200, 50)
        self.minus_button = pygame.Rect(self.width // 2 - 150, 200, 50, 50)
        self.plus_button = pygame.Rect(self.width // 2 + 100, 200, 50, 50)
        # Кнопка переключателя алгоритма (без текста внутри)
        self.algorithm_button = pygame.Rect(self.width // 2 - 100, 270, 200, 50)
        # Кнопка на экране завершения игры
        self.play_again_button = pygame.Rect(self.width // 2 - 100, 300, 200, 50)

        # Параметр длины массива (от 15 до 25)
        self.array_length = 15

        # Параметры переключателя алгоритма:
        # Если True, выбираем Minimax; если False, выбираем Alfa-Beta.
        self.algorithm_toggle = True
        # Для анимации переключателя создаём переменные для положения "ползунка"
        self.algorithm_knob_width = 40
        self.algorithm_knob_y = self.algorithm_button.y + 5
        self.algorithm_knob_x = self.algorithm_button.x + 5 if self.algorithm_toggle else self.algorithm_button.x + self.algorithm_button.width - self.algorithm_knob_width - 5
        self.algorithm_knob_target_x = self.algorithm_knob_x
        self.algorithm_knob_speed = 10  # пикселей за кадр

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # ограничение FPS до 60
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.state == "menu":
                    # Кнопки изменения длины массива
                    if self.minus_button.collidepoint(pos):
                        self.array_length = max(15, self.array_length - 1)
                    elif self.plus_button.collidepoint(pos):
                        self.array_length = min(25, self.array_length + 1)
                    # Переключатель алгоритма
                    elif self.algorithm_button.collidepoint(pos):
                        self.algorithm_toggle = not self.algorithm_toggle
                        if self.algorithm_toggle:
                            self.algorithm_knob_target_x = self.algorithm_button.x + 5
                        else:
                            self.algorithm_knob_target_x = self.algorithm_button.x + self.algorithm_button.width - self.algorithm_knob_width - 5
                    # Кнопка "Sākt spēli"
                    elif self.start_button.collidepoint(pos):
                        self.state = "game"
                        # Здесь можно передать параметры в основной код (logic.py)
                        # Например: game.choose_length(self.array_length)
                        # И: game.set_algorithm(1) если self.algorithm_toggle True, иначе game.set_algorithm(2)
                elif self.state == "end":
                    if self.play_again_button.collidepoint(pos):
                        self.state = "menu"
            elif event.type == pygame.KEYDOWN:
                if self.state == "game" and event.key == pygame.K_ESCAPE:
                    self.state = "end"

    def update(self):
        # Анимация ползунка переключателя алгоритма
        if self.algorithm_knob_x < self.algorithm_knob_target_x:
            self.algorithm_knob_x += self.algorithm_knob_speed
            if self.algorithm_knob_x > self.algorithm_knob_target_x:
                self.algorithm_knob_x = self.algorithm_knob_target_x
        elif self.algorithm_knob_x > self.algorithm_knob_target_x:
            self.algorithm_knob_x -= self.algorithm_knob_speed
            if self.algorithm_knob_x < self.algorithm_knob_target_x:
                self.algorithm_knob_x = self.algorithm_knob_target_x

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
        # Заголовок главного меню
        title_text = self.font.render("Galvenā izvēlne", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 50))

        # Отображение выбора длины массива
        prompt_text = self.font.render("Masīva garums:", True, (255, 255, 255))
        self.screen.blit(prompt_text, (self.width // 2 - prompt_text.get_width() // 2, 120))

        # Кнопка "минус"
        pygame.draw.rect(self.screen, (100, 100, 200), self.minus_button)
        minus_text = self.font.render("-", True, (255, 255, 255))
        self.screen.blit(minus_text, (
            self.minus_button.x + (self.minus_button.width - minus_text.get_width()) // 2,
            self.minus_button.y + (self.minus_button.height - minus_text.get_height()) // 2))

        # Кнопка "плюс"
        pygame.draw.rect(self.screen, (100, 100, 200), self.plus_button)
        plus_text = self.font.render("+", True, (255, 255, 255))
        self.screen.blit(plus_text, (
            self.plus_button.x + (self.plus_button.width - plus_text.get_width()) // 2,
            self.plus_button.y + (self.plus_button.height - plus_text.get_height()) // 2))

        # Отображение текущего значения длины массива между кнопками
        value_text = self.font.render(str(self.array_length), True, (255, 255, 255))
        value_x = self.width // 2 - value_text.get_width() // 2
        value_y = self.minus_button.y + (self.minus_button.height - value_text.get_height()) // 2
        self.screen.blit(value_text, (value_x, value_y))

        # Отрисовка переключателя алгоритма (без текста внутри)
        pygame.draw.rect(self.screen, (80, 80, 80), self.algorithm_button, border_radius=25)
        # Отрисовка ползунка переключателя
        knob_rect = pygame.Rect(self.algorithm_knob_x, self.algorithm_button.y + 5, self.algorithm_knob_width,
                                self.algorithm_button.height - 10)
        pygame.draw.rect(self.screen, (200, 200, 200), knob_rect, border_radius=20)
        # Отрисовка подписей по краям переключателя:
        left_label = self.font.render("alpha-beta", True, (255, 255, 255))
        right_label = self.font.render("minimax", True, (255, 255, 255))
        self.screen.blit(left_label, (self.algorithm_button.x - left_label.get_width() - 10,
                                      self.algorithm_button.y + (
                                                  self.algorithm_button.height - left_label.get_height()) // 2))
        self.screen.blit(right_label, (self.algorithm_button.right + 10,
                                       self.algorithm_button.y + (
                                                   self.algorithm_button.height - right_label.get_height()) // 2))

        # Кнопка "Sākt spēli"
        pygame.draw.rect(self.screen, (100, 100, 200), self.start_button)
        button_text = self.font.render("Sākt spēli", True, (255, 255, 255))
        self.screen.blit(button_text, (
            self.start_button.x + (self.start_button.width - button_text.get_width()) // 2,
            self.start_button.y + (self.start_button.height - button_text.get_height()) // 2))

    def render_game(self):
        self.screen.fill((50, 50, 50))
        title_text = self.font.render("Spēles ekrāns", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))
        # Здесь можно добавить отрисовку игрового поля, счета и других элементов

    def render_end(self):
        self.screen.fill((30, 30, 30))
        title_text = self.font.render("Spēle beigusies", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))
        pygame.draw.rect(self.screen, (200, 100, 100), self.play_again_button)
        button_text = self.font.render("Spēlēt vēlreiz", True, (255, 255, 255))
        self.screen.blit(button_text, (
            self.play_again_button.x + (self.play_again_button.width - button_text.get_width()) // 2,
            self.play_again_button.y + (self.play_again_button.height - button_text.get_height()) // 2))









