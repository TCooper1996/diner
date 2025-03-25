from typing import Dict, List
from src.game_engine.game import Game
from src.state.game import GameState
from src.tui.CustomerTab import CustomerTab
from src.tui.TabControllers.EmployeeTab import EmployeeTab
from src.tui.TabControllers.EmployeeTabGroup import EmployeeTabGroup
from src.tui.gameInfoTab import GameInfoTab
from textual.widgets import RichLog



class GameController:
    def __init__(self, employee_tab_group: EmployeeTabGroup, gameInfoTab: GameInfoTab, customerTab: CustomerTab, logTab: RichLog):
        self.employee_tab_group= employee_tab_group
        self.gameInfoTab = gameInfoTab
        self.customerTab = customerTab
        self.logTab = logTab

    def updateTabs(self, gameState: GameState):
        self.gameInfoTab.update(gameState)
        self.customerTab.update(gameState)
        self.employee_tab_group.update(gameState)
        self.logTab.clear()
        for i, game_turn in enumerate(gameState.employee_turns()):
            self.logTab.write(f"Turn {i}")
            for employee_turn in game_turn.employees:
                self.logTab.write(f" Employee {employee_turn.employee_name}")
                for attempt_num, attempt in enumerate(employee_turn.decisions):
                    spacing = " "*3
                    self.logTab.write(f"  Attempt {attempt_num}")
                    self.logTab.write(spacing + attempt.response.content)
                    self.logTab.write(spacing + attempt.invocation.tool)
                    self.logTab.write(spacing + attempt.result.tool_output + "\n")


    async def start(self, game: Game, pause_event):
        initState = await game.start()
        await self.loop(game, initState, pause_event)
        

    async def loop(self, game: Game, initState: GameState, pause_event):
        nextState = initState
        while True:
            nextState = await game.loop(nextState)

            self.updateTabs(nextState)

            await pause_event.wait()