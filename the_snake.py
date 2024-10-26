import pygame
import random


class Snake:
    """Класс, представляющий змею."""

    def __init__(self):
        """Инициализация змеи."""
        self.size = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 255, 0)
        self.score = 0

    def get_head_position(self):
        """Возвращает текущую позицию головы змеи."""
        return self.positions[0]

    def turn(self, point):
        """Поворачивает змею в заданном направлении."""
        if self.size > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        """Перемещает змею в текущем направлении."""
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.size:
                self.positions.pop()

    def reset(self):
        """Сбрасывает змею до начального состояния."""
        self.size = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        """Отрисовывает змею на экране."""
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        """Обрабатывает нажатия клавиш для управления змеей."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class Food:
    """Класс, представляющий еду для змеи."""

    def __init__(self):
        """Инициализация еды."""
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом задает позицию еды на экране."""
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    def draw(self, surface):
        """Отрисовывает еду на экране."""
        r = pygame.Rect((self.position[0], self.position[1]),
                        (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


def draw_grid(surface):
    """Отрисовывает сетку на экране."""
    for y in range(0, int(SCREEN_HEIGHT / GRIDSIZE)):
        for x in range(0, int(SCREEN_WIDTH / GRIDSIZE)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE),
                                (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE),
                                 (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)


# Константы для игры
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    """Главная функция для запуска игры."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("Snake")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    draw_grid(surface)

    snake = Snake()
    food = Food()

    while True:
        snake.handle_keys()
        draw_grid(surface)
        snake.move()

        if snake.get_head_position() == food.position:
            snake.size += 1
            snake.score += 1
            food.randomize_position()

        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
