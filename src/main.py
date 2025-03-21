import asyncio
from src.game_engine.game import Game
from src.tui import Window

def main():
    game = Game()
    window = Window(game)
    window.run()

if __name__ == "__main__":
    main()

