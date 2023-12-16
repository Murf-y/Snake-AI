import pygame
import numpy as np
import sys
import time
import random


def collision(snake, direction, width, height):
    new_head = snake[-1] + direction
    if new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height:
        return True
    elif any((new_head == segment).all() for segment in snake[:-1]):
        return True
    else:
        return False


def generate_food(snake, width, height, BLOCK_SIZE):
    food = [random.randrange(0, width, BLOCK_SIZE), random.randrange(0, height, BLOCK_SIZE)]
    
    return food

def main():
    SNAKE_COLOR = (135, 212, 47)
    GRID_COLOR = (43, 43, 43)
    FOOD_COLOR = (212, 58, 47)
    WIDTH, HEIGHT = 600, 600
    BLOCK_SIZE = 30
    SNAKE_START = [(WIDTH // 2, HEIGHT // 2)]
    
    
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = SNAKE_START.copy()
    direction = np.array([0, -BLOCK_SIZE])
    food = generate_food(snake, WIDTH, HEIGHT, BLOCK_SIZE)

    while True:
        screen.fill((31, 31, 31))

        # Draw grid with fading alpha
        for i in range(0, WIDTH, BLOCK_SIZE):
            for j in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.rect(screen, GRID_COLOR + (50,), pygame.Rect(i, j, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw food
        pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.display.flip()

        # Move snake
        new_head = snake[-1] + direction
        
        # Check for collision
        if collision(snake, direction, WIDTH, HEIGHT):
            pygame.quit()
            sys.exit()
        else:
            snake.append(new_head)
        
        if (new_head == food).all():
            food = generate_food(snake, WIDTH, HEIGHT, BLOCK_SIZE)
        else:
            snake.pop(0)
            

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