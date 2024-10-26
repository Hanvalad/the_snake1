import pygame
import random

# Константы для экрана и сетки
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Чёрный цвет фона

# Константы направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация Pygame экрана и времени
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position, body_color):
        """Инициализирует объект с позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на переданной поверхности."""
        pygame.draw.rect(
            surface,
            self.body_color,
            pygame.Rect(
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
        )


class Apple(GameObject):
    """Класс для яблока, которое ест змея."""

    def __init__(self, position, body_color=(255, 0, 0)):
        """Создаёт объект яблока с позицией и цветом."""
        super().__init__(position, body_color)

    def randomize_position(self):
        """Перемещает яблоко в случайную позицию на игровом поле."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )


class Snake(GameObject):
    """Класс для змеи."""

    def __init__(self, position, body_color=(0, 255, 0)):
        """Инициализирует змею с начальной позицией и цветом."""
        super().__init__(position, body_color)
        self.positions = [position]
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """Двигает змею в текущем направлении."""
        head_x, head_y = self.get_head_position()
        new_position = (head_x + self.direction[0], head_y + self.direction[1])
        self.positions = [new_position] + self.positions[:-1]

    def reset(self):
        """Сбрасывает змею к исходной позиции и направлению."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT

    def update_direction(self, new_direction):
        """Обновляет направление движения змеи."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и обновляет направление змеи."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.update_direction(UP)
    elif keys[pygame.K_DOWN]:
        snake.update_direction(DOWN)
    elif keys[pygame.K_LEFT]:
        snake.update_direction(LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.update_direction(RIGHT)


def main():
    """Запускает основной игровой цикл."""
    snake = Snake(position=(GRID_WIDTH // 2, GRID_HEIGHT // 2))
    apple = Apple(
        position=(
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
    )

    running = True
    while running:
        screen.fill(BOARD_BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(snake)
        snake.move()

        # Если змея ест яблоко
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.positions.append(snake.positions[-1])  # Добавить к длине змеи

        # Отрисовка
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.flip()
        clock.tick(10)  # FPS

    pygame.quit()


# Проверка запуска основного модуля
if __name__ == "__main__":
    main()
