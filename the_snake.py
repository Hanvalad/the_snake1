import pygame
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
FONT_COLOR = (255, 255, 255)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)


class GameObject:
    """Представляет игровой объект с позицией и цветом."""

    def __init__(self, position, color):
        """Инициализация игрового объекта.

        Args:
            position (tuple): Позиция объекта (x, y).
            color (tuple): Цвет объекта в RGB.
        """
        self.position = position
        self.color = color

    def draw(self, surface):
        """Отрисовывает объект на указанной поверхности.

        Args:
            surface (pygame.Surface): Поверхность, на которой рисуется объект.
        """
        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.color, rect)


class Apple(GameObject):
    """Представляет яблоко на игровом поле."""

    def __init__(self):
        """Инициализация яблока с случайной позицией."""
        super().__init__(self.randomize_position(), APPLE_COLOR)

    def randomize_position(self):
        """Случайным образом генерирует позицию яблока.

        Returns:
            tuple: Случайная позиция (x, y) на игровом поле.
        """
        return (random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1))


class Snake:
    """Представляет змейку в игре."""

    def __init__(self):
        """Инициализация змейки с начальной позицией и направлением."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def get_head_position(self):
        """Получает текущую позицию головы змейки.

        Returns:
            tuple: Позиция головы (x, y).
        """
        return self.positions[0]

    def change_direction(self, new_direction):
        """Изменяет направление движения змейки.

        Args:
            new_direction (tuple): Новое направление (dx, dy).
        """
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def move(self):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        delta_x, delta_y = self.direction
        new_head = ((head_x + delta_x) % GRID_WIDTH,
                    (head_y + delta_y) % GRID_HEIGHT)

        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if not self.grow:
                self.positions.pop()
            self.grow = False

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def draw(self, surface):
        """Отрисовывает змейку на указанной поверхности.

        Args:
            surface (pygame.Surface): Поверхность, на которой рисуется змейка.
        """
        for position in self.positions:
            rect = pygame.Rect(
                (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, SNAKE_COLOR, rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления змейки.

    Args:
        snake (Snake): Объект змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)


def draw_score(surface, score):
    """Отображает текущий счет на экране.

    Args:
        surface (pygame.Surface): Поверхность, на которой рисуется счет.
        score (int): Текущий счет игры.
    """
    score_text = font.render(f'Score: {score}', True, FONT_COLOR)
    surface.blit(score_text, (10, 10))


def main():
    """Главная функция игры."""
    snake = Snake()
    apple = Apple()
    score = 0

    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow = True
            apple.position = apple.randomize_position()
            score += 1  # Увеличиваем счет

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        draw_score(screen, score)  # Рисуем счет
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
