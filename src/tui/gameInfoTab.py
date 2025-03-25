from textual.widgets import Markdown

from src.state.game import GameState
class GameInfoTab:
    def __init__(self, markdown: Markdown):
        self.markdown = markdown

    def update(self, gameState: GameState):
        self.markdown.update(f"# Game Info\n\n{gameState.to_prompt()}")
