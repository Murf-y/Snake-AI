from enum import Enum
import pygame
import random
import numpy as np


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

        self.snake_parts = []
        self.food = None

    def update(self, snake_parts, food):
        self.snake_parts = snake_parts
        self.food = food

    def act(self, current_direction):
        action = self.act_helper()
        direction = self.get_direction_from_action(action, current_direction)
        print(self.fitness_function(direction))
        return direction

    def get_direction_from_action(self, action, current_direction):
        if action == Action.UP:
            return np.array([0, -self.block_size])
        elif action == Action.DOWN:
            return np.array([0, self.block_size])
        elif action == Action.LEFT:
            return np.array([-self.block_size, 0])
        elif action == Action.RIGHT:
            return np.array([self.block_size, 0])
        else:
            return current_direction

    def act_helper(self):
        if self.agent_type == AgentType.HUMAN:
            return self.handle_events()
        elif self.agent_type == AgentType.RANDOM:
            return self.random_action()
        else:
            return self.ai_action()

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

    def fitness_function(self, direction):
        new_head = self.snake_parts[-1] + direction
        if new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
            return -100
        elif any((new_head == segment).all() for segment in self.snake_parts[:-1]):
            return -100

        elif new_head[0] == self.food[0] and new_head[1] == self.food[1]:
            return 100
        else:
            return 0

    def ai_action(self):
        best_action = Action.NONE
        best_fitness = -100

        for action in list(Action):
            fitness = self.fitness_function(self.get_direction_from_action(
                action, self.snake_parts[-1] - self.snake_parts[-2]))
            if fitness > best_fitness:
                best_fitness = fitness
                best_action = action

        return best_action
