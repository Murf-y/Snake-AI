import pygame
import numpy as np
import sys


class Snake:
    def __init__(self, block_size, width, height):
        self.block_size = block_size
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = np.array([0, -block_size])
        self.score = 0

    def get_score(self):
        return self.score

    def get_direction(self):
        return self.direction

    def collision(self):
        new_head = self.snake[-1] + self.direction
        if new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
            return True
        elif any((new_head == segment).all() for segment in self.snake[:-1]):
            return True
        else:
            return False

    def move(self):
        new_head = self.snake[-1] + self.direction
        self.snake.append(new_head)
        self.snake.pop(0)

    def eat(self, food):
        self.snake.append(food)
        self.score += 1

    def can_eat(self, food):
        return (self.snake[-1] + self.direction == food).all()

    def change_direction(self, direction):
        if not np.array_equal(self.direction, -direction):
            self.direction = direction

    def draw(self, screen):
        SNAKE_COLOR = (135, 212, 47)
        for segment in self.snake:
            pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(
                segment[0], segment[1], self.block_size, self.block_size))
