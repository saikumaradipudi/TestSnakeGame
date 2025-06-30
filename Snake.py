import pygame
import random

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

FONT = pygame.font.SysFont('Arial', 24)

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Sprite, Walls, Pause")

clock = pygame.time.Clock()

# Optionally load a snake head sprite (replace with your file path)
head_img = pygame.image.load("snake_image.png").convert_alpha()
head_img = pygame.transform.scale(head_img, (TILE_SIZE, TILE_SIZE))


def new_food():
    return (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))  # inside walls

def draw(snake, food, score, paused):
    screen.fill(WHITE)

    # Draw walls
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TILE_SIZE))  # top
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - TILE_SIZE, WIDTH, TILE_SIZE))  # bottom
    pygame.draw.rect(screen, GRAY, (0, 0, TILE_SIZE, HEIGHT))  # left
    pygame.draw.rect(screen, GRAY, (WIDTH - TILE_SIZE, 0, TILE_SIZE, HEIGHT))  # right

    # Draw snake
    for i, segment in enumerate(snake):
        x = segment[0] * TILE_SIZE
        y = segment[1] * TILE_SIZE
        if i == 0 and head_img:  # Head
            screen.blit(head_img, (x, y))
        else:  # Body
            center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
            pygame.draw.circle(screen, GREEN, center, TILE_SIZE // 2)


    # Draw food
    food_center = (food[0] * TILE_SIZE + TILE_SIZE // 2, food[1] * TILE_SIZE + TILE_SIZE // 2)
    pygame.draw.circle(screen, RED, food_center, TILE_SIZE // 2)

    # Draw score
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if paused:
        pause_text = FONT.render("Paused", True, RED)
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))

    pygame.display.flip()

def move_snake(snake, direction):
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    snake.insert(0, new_head)
    return new_head

def check_collision(snake):
    head = snake[0]
    # Hit walls
    if head[0] == 0 or head[0] == GRID_WIDTH -1 or head[1] == 0 or head[1] == GRID_HEIGHT -1:
        return True
    # Hit itself
    if head in snake[1:]:
        return True
    return False

def game_loop():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (0, 0)
    food = new_food()
    score = 0
    speed = 10
    paused = False

    running = True
    while running:
        clock.tick(speed if not paused else 5)  # Slow refresh if paused
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)

        if not paused and direction != (0, 0):
            new_head = move_snake(snake, direction)
            if new_head == food:
                score += 1
                food = new_food()
                speed = min(30, speed + 1)  # Speed up
            else:
                snake.pop()

            if check_collision(snake):
                draw(snake, food, score, paused)
                print(f"💀 Game Over! Your score: {score}")
                running = False

        draw(snake, food, score, paused)

def main():
    while True:
        game_loop()
        print("Press R to restart or Q to quit.")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

if __name__ == "__main__":
    main()
