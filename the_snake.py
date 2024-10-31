from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, содержащий общие атрибуты игровых объектов."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        """Метод инициализирует базовые атрибуты объекта (позиция и цвет)."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод, который предназначен для переопределения в
        дочерних классах. Этот метод должен определять, как объект будет
        отрисовываться на экране.
        """
        pass


class Snake(GameObject):
    """Класс, описывающий змейку и наследующийся от GameObject."""

    def __init__(self, length=1, positions=None, direction=RIGHT,
                 next_direction=None, body_color=SNAKE_COLOR, last=None):
        """Метод инициализирует начальное состояние змейки."""
        super().__init__(body_color)
        self.length = length
        if positions is None:
            self.positions = [self.position]
        else:
            self.positions = positions.copy()
            self.positions.append(self.position)
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.last = last

    def update_direction(self):
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод обновляет позицию змейки, добавляя новую голову и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        current_head = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (current_head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (current_head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head in self.positions[2:]:
            self.reset()
            return
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает в начальное состояние после столкновения с собой."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


class Apple(GameObject):
    """Класс, описывающий яблоко и наследующийся от GameObject."""

    def __init__(self, body_color=APPLE_COLOR):
        """Метод задаёт цвет яблока и устанавливает его начальную позицию."""
        super().__init__(body_color)
        self.body_color = body_color

    def randomize_position(self):
        """Метод устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """
    Функция обрабатывает нажатия клавиш, чтобы изменить направление
    движения змейки.
    """
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


def main():
    """
    Запускает основной игровой цикл игры.
    Функция инициализирует игровое окружение, объекты змейки и яблока
    и запускает основной игровой цикл. В ходе цикла обрабатываются нажатия
    клавиш, обновляется направление и положение змейки, проверяется, не съела
    ли змейка яблоко и не столкнулась ли сама с собой, а также происходит
    перерисовка экрана.
    Игровой цикл продолжается до тех пор, пока игрок не выйдет из игры.
    """
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        snake.move()
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
