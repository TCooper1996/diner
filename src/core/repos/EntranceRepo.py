from typing import Protocol

from src.core.entities.entrance import Entrance


class EntranceRepo(Protocol):
    def get_all_entrances(self) -> list[Entrance]:
        """Get all entrances in the restaurant."""
        pass