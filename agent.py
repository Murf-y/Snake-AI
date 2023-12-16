from enum import Enum
import pygame
import random
import math
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
        self.current_direction = None
        self.current_score = 0

    def update(self, snake_parts, food, current_direction, current_score):
        self.snake_parts = snake_parts
        self.food = food
        self.current_direction = current_direction
        self.current_score = current_score

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

        # Unallowed action
        if np.array_equal(direction, -self.current_direction):
            return -100

        # The head of the snake after the action is taken
        new_head = self.snake_parts[-1] + direction

        # Hit wall
        if new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
            return -100

        # Hit self
        if any((new_head == segment).all() for segment in self.snake_parts[:-1]):
            return -100

        # Hit food
        if new_head[0] == self.food[0] and new_head[1] == self.food[1]:
            return 100

        # Euclidean distance to food
        distance_to_food = np.linalg.norm(new_head - self.food)
        return 1 / distance_to_food

    def ai_action(self):
        best_action = Action.NONE
        best_fitness = -math.inf

        for action in list(Action):
            direction = self.get_direction_from_action(action)
            fitness = self.fitness_function(direction)

            if fitness > best_fitness:
                best_fitness = fitness
                best_action = action

        print(best_action, best_fitness)
        return best_action
