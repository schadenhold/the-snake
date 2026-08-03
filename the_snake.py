from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для всех игровых объектов.

    Описывает объект в игре.

    Attributes:
        position: позиция на экране.
        body_color: цвет объекта.
    """

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для реализации собственной отрисовки дочерними классами."""
        raise NotImplementedError(
            'Необходимо реализовать метод draw в дочернем классе!'
        )


class Apple(GameObject):
    """Дочерний класс яблоко со случайной позицией."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(None)

    def randomize_position(self, game_object):
        """Генерирует случайную позицию, не пересекающуюся с телом змейки."""
        # Если game_object None, то проверка не нужна
        forbidden_positions = game_object.positions if game_object else []
        random_position = (
                (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        )
        if random_position not in forbidden_positions:
            self.position = random_position

    def draw(self):
        """Метод отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс змейки с учетом направления движения."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Возвращает координаты головы."""
        if self.positions:
            return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            horizontal, vertical = self.direction
            next_horizontal, next_vertical = self.next_direction
            # проверка на запрет в противоположное движение
            if horizontal != -next_horizontal or vertical != -next_vertical:
                self.direction = self.next_direction

    def move(self):
        """Метод движения змейки."""
        self.update_direction()

        # Распаковка позиции головы
        horizontal_head, vertical_head = self.get_head_position()

        # Распаковка направления
        horizontal_direction, vertical_direction = self.direction

        # Новая позиция головы с учетом прохода границы экрана
        new_head_position = (
            (horizontal_head + horizontal_direction * GRID_SIZE) % SCREEN_WIDTH,
            (vertical_head + vertical_direction * GRID_SIZE) % SCREEN_HEIGHT
        )

        # Добавляем новую голову
        self.positions.insert(0, new_head_position)

        # Если длина превышает нужную, удаляем хвост
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Исходное состояние змейки."""
        self.length = 1
        self.positions = [(SCREEN_CENTER_X, SCREEN_CENTER_Y)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки нажатий стрелок на клавиатуре."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def check_collision(game_object):
    """Проверяет столкновение змейки с собой."""
    if not game_object.positions:
        return True
    head = game_object.get_head_position()
    return head in game_object.positions[1:]


def check_eatable_collision(snake, eatable_object):
    """Проверяет, съела ли змейка яблоко."""
    head = snake.get_head_position()
    return head == eatable_object.position


def main():
    """Основная функция инициализации игры."""
    # Инициализация PyGame:
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Основная логика игры.
        handle_keys(snake)
        snake.move()

        # Проверка столкновения с яблоком
        if check_eatable_collision(snake, apple):
            snake.length += 1
            apple.randomize_position(snake)

        # Проверка столкновения змейки с собой
        elif check_collision(snake):
            snake.reset()
            apple.randomize_position(snake)
            continue

        # Отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очищаем экран

        # Отрисовка игровых объектов
        apple.draw()
        snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
