import pygame
import numpy as np
import sys
import time
import random
from snake import Snake
from agent import AgentType


class SnakeGame:
    def __init__(self, width, height, block_size, tick_rate, agent, graphics=True):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.tick_rate = tick_rate
        self.agent = agent
        self.graphics = graphics
        self.snake = Snake(block_size, width, height)

        self.grid = np.zeros(
            (self.width // self.block_size, self.height // self.block_size))

        for i in range(0, self.width, self.block_size):
            for j in range(0, self.height, self.block_size):
                self.grid[i // self.block_size][j // self.block_size] = 1

        self.food = self.generate_food()
        self.SNAKE_COLOR = (135, 212, 47)
        self.GRID_COLOR = (43, 43, 43)
        self.FOOD_COLOR = (212, 58, 47)
        self.BACKGROUND_COLOR = (31, 31, 31)

        if self.graphics:
            pygame.init()
            self.font = pygame.font.SysFont("segoeui", 24)
            self.screen = pygame.display.set_mode((width, height))
            self.clock = pygame.time.Clock()

    def generate_food(self):
        possible_food = []
        for i in range(self.width // self.block_size):
            for j in range(self.height // self.block_size):
                if self.grid[i][j] == 1:
                    if not any(np.array_equal(segment, [i * self.block_size, j * self.block_size]) for segment in self.snake.snake):
                        possible_food.append(
                            (i * self.block_size, j * self.block_size))

        return random.choice(possible_food)

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)

        # Draw grid with fading alpha
        for i in range(0, self.width, self.block_size):
            for j in range(0, self.height, self.block_size):
                pygame.draw.rect(self.screen, self.GRID_COLOR + (50,),
                                 pygame.Rect(i, j, self.block_size, self.block_size), 1)

        self.snake.draw(self.screen)

        # Draw food
        pygame.draw.rect(self.screen, self.FOOD_COLOR, pygame.Rect(
            self.food[0], self.food[1], self.block_size, self.block_size))

        score = self.snake.get_score()
        text = self.font.render(f"{score}", True, (255, 255, 255))
        self.screen.blit(text, (self.width - 50, 10))

        pygame.display.flip()

    def will_collide_after_move(self):
        return self.snake.collision()

    def can_eat(self):
        return self.snake.can_eat(self.food)

    def eat(self):
        self.snake.eat(self.food)
        self.food = self.generate_food()

    def move(self):
        self.snake.move()

    def change_direction(self, direction):
        self.snake.change_direction(direction)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_direction(np.array([0, -self.block_size]))
                elif event.key == pygame.K_DOWN:
                    self.change_direction(np.array([0, self.block_size]))
                elif event.key == pygame.K_LEFT:
                    self.change_direction(np.array([-self.block_size, 0]))
                elif event.key == pygame.K_RIGHT:
                    self.change_direction(np.array([self.block_size, 0]))

    def handle_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):

        start_time = time.time()

        while True:
            if self.graphics:
                self.draw()

            self.agent.update(self.snake, self.food)

            direction = self.agent.act()
            self.change_direction(direction)

            if self.can_eat():
                self.eat()

            if self.will_collide_after_move():

                if self.graphics:
                    pygame.quit()
                break

            self.move()

            if self.graphics:
                self.handle_close()
                self.clock.tick(self.tick_rate)
                time.sleep(1 / self.tick_rate)

        end_time = time.time()
        time_passed = end_time - start_time
        return self.snake.get_score(), time_passed
