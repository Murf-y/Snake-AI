import pygame
import numpy as np
import sys
import time
import random
from snake import Snake

# def collision(snake, direction, width, height):
#     new_head = snake[-1] + direction
#     if new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height:
#         return True
#     elif any((new_head == segment).all() for segment in snake[:-1]):
#         return True
#     else:
#         return False


def generate_food(snake, width, height, BLOCK_SIZE):
    food = [random.randrange(0, width, BLOCK_SIZE), random.randrange(0, height, BLOCK_SIZE)]
    
    return food

def main():
    SNAKE_COLOR = (135, 212, 47)
    GRID_COLOR = (43, 43, 43)
    FOOD_COLOR = (212, 58, 47)
    BACKGROUND_COLOR = (31, 31, 31)
    WIDTH, HEIGHT = 600, 600
    BLOCK_SIZE = 30
    
    
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake(BLOCK_SIZE, WIDTH, HEIGHT)
    food = generate_food(snake, WIDTH, HEIGHT, BLOCK_SIZE)

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Draw grid with fading alpha
        for i in range(0, WIDTH, BLOCK_SIZE):
            for j in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.rect(screen, GRID_COLOR + (50,), pygame.Rect(i, j, BLOCK_SIZE, BLOCK_SIZE), 1)

        snake.draw(screen)
        
        # Draw food
        pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.display.flip()

        # Move snake
        new_head = snake[-1] + direction
        
        if snake.collision():
            pygame.quit()
            sys.exit()
        elif (new_head == food).all():
            snake.eat(food)
            food = generate_food(snake, WIDTH, HEIGHT, BLOCK_SIZE)
        else:
            snake.move()
            

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = np.array([0, -BLOCK_SIZE])
                elif event.key == pygame.K_DOWN:
                    direction = np.array([0, BLOCK_SIZE])
                elif event.key == pygame.K_LEFT:
                    direction = np.array([-BLOCK_SIZE, 0])
                elif event.key == pygame.K_RIGHT:
                    direction = np.array([BLOCK_SIZE, 0])

        # Slow down the snake
        time.sleep(0.1)

if __name__ == "__main__":
    main()