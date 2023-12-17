from enum import Enum
import pygame
import random
import math
import numpy as np
from snake import Snake


class AgentType(Enum):
    HUMAN = 1
    AI = 2
    RANDOM = 3


class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5


class Agent:
    def __init__(self, agent_type: AgentType, width, height, block_size):
        self.agent_type = agent_type
        self.width = width
        self.height = height
        self.block_size = block_size

        self.snake = None
        self.food = None
        self.current_direction = None
        self.current_score = 0

    def update(self, snake, food):
        self.snake = snake
        self.current_direction = snake.get_direction()
        self.current_score = snake.get_score()
        self.food = food

    def act(self):
        action = self.act_helper()
        direction = self.get_direction_from_action(action)
        return direction

    def get_direction_from_action(self, action):
        if action == Action.UP:
            return np.array([0, -self.block_size])
        elif action == Action.DOWN:
            return np.array([0, self.block_size])
        elif action == Action.LEFT:
            return np.array([-self.block_size, 0])
        elif action == Action.RIGHT:
            return np.array([self.block_size, 0])
        else:
            return self.current_direction

    def act_helper(self):
        if self.agent_type == AgentType.HUMAN:
            return self.handle_events()

        if self.agent_type == AgentType.RANDOM:
            return self.random_action()

        fitness, action = self.ai_action(self.snake, depth=1)
        return action

    def random_action(self):
        return random.choice(list(Action))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return Action.UP
                elif event.key == pygame.K_DOWN:
                    return Action.DOWN
                elif event.key == pygame.K_LEFT:
                    return Action.LEFT
                elif event.key == pygame.K_RIGHT:
                    return Action.RIGHT

        return Action.NONE

    def check_collisions(self, direction, snake_parts):
        new_head = snake_parts[-1] + direction

        if np.array_equal(direction, -self.current_direction):
            return True

        if new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
            return True

        if any((new_head == segment).all() for segment in snake_parts):
            return True

    def check_food(self, direction, snake_parts):
        new_head = snake_parts[-1] + direction

        if new_head[0] == self.food[0] and new_head[1] == self.food[1]:
            return True

    def fitness_function(self, direction, snake):
        death_penalty = 1000
        food_reward = -1000
        if self.check_collisions(direction, snake.snake):
            return death_penalty

        if self.check_food(direction, snake.snake):
            return food_reward

        new_head = snake.snake[-1] + direction
        # Calculate distance to food using manhattan distance
        distance_to_food = abs(
            new_head[0] - self.food[0]) + abs(new_head[1] - self.food[1])

        return distance_to_food

    def ai_action(self, snake, depth):
        best_fitness_score = 1001
        best_action = Action.NONE

        for action in Action:
            copy_snake = Snake(self.block_size, self.width, self.height)
            copy_snake.snake = snake.snake.copy()
            copy_snake.score = snake.score
            copy_snake.direction = snake.direction

            new_direction = self.get_direction_from_action(action)

            if depth == 0:
                fitness_score = self.fitness_function(
                    new_direction, copy_snake)
            else:
                if self.check_collisions(new_direction, copy_snake.snake):
                    fitness_score = 1000
                elif self.check_food(new_direction, copy_snake.snake):
                    fitness_score = -1000
                else:
                    copy_snake.change_direction(new_direction)
                    copy_snake.move()
                    fitness_score, _ = self.ai_action(copy_snake, depth - 1)

            if fitness_score < best_fitness_score:
                best_fitness_score = fitness_score
                best_action = action

        return best_fitness_score, best_action

    def get_action_from_direction(self, direction):
        if np.array_equal(direction, np.array([0, -self.block_size])):
            return Action.UP
        elif np.array_equal(direction, np.array([0, self.block_size])):
            return Action.DOWN
        elif np.array_equal(direction, np.array([-self.block_size, 0])):
            return Action.LEFT
        elif np.array_equal(direction, np.array([self.block_size, 0])):
            return Action.RIGHT
        else:
            return Action.NONE
