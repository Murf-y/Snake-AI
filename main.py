from game import SnakeGame
from agent import Agent, AgentType


def main():
    WIDTH, HEIGHT = 600, 600
    BLOCK_SIZE = 30
    FPS = 50

    agent = Agent(AgentType.AI, WIDTH, HEIGHT, BLOCK_SIZE)
    snake_game = SnakeGame(WIDTH, HEIGHT, BLOCK_SIZE,
                           FPS, agent, graphics=True)
    final_score, time_passed = snake_game.run()

    print("Final score: ", final_score, "Time passed: ", time_passed)


if __name__ == "__main__":
    main()
