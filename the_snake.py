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

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Фон поля - черный
BORDER_COLOR = (93, 216, 228)  # Граница ячейки
APPLE_COLOR = (255, 0, 0)  # Яблоко
SNAKE_COLOR = (0, 255, 0)  # Змейка

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class Apple:
    """Класс для представления яблока на игровом поле."""

    def __init__(self):
        """Инициализация позиции яблока и цвета тела."""
        self.position = self.random_position()
        self.body_color = APPLE_COLOR

    def random_position(self):
        """Генерирует случайную позицию для яблока на сетке."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отображение яблока на игровом экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake:
    """Класс для представления змейки."""

    def __init__(self):
        """Инициализация начальных параметров змейки."""
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.body_color = SNAKE_COLOR
        self.next_direction = None
        self.last = None

    def move(self):
        """Перемещение змейки в текущем направлении."""
        x, y = self.positions[0]
        dx, dy = self.direction
        new_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        if new_head in self.positions[1:]:
            raise SystemExit  # Конец игры при столкновении с телом

        self.positions.insert(0, new_head)
        self.last = self.positions.pop() if len(self.positions) > 1 else None

    def grow(self):
        """Увеличивает длину змейки."""
        self.positions.append(self.positions[-1])

    def draw(self):
        """Отображение змейки на игровом экране."""
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

    def update_direction(self):
        """Обновляет направление движения змейки на основе следующего шага."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления направлением змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция для инициализации и запуска игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = apple.random_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
