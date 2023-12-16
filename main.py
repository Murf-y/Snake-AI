from game import SnakeGame
from agent import Agent, AgentType


def main():
    WIDTH, HEIGHT = 600, 600
    BLOCK_SIZE = 30
    FPS = 60

    agent = Agent(AgentType.HUMAN, WIDTH, HEIGHT, BLOCK_SIZE)
    snake_game = SnakeGame(WIDTH, HEIGHT, BLOCK_SIZE, FPS, agent)
    snake_game.run()


if __name__ == "__main__":
    main()
