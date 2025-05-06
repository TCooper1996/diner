from src.core.entities.entrance import Entrance
from src.core.repos.EntranceRepo import EntranceRepo


class EntranceRepoImpl(EntranceRepo):
    """
    Implementation of the EntranceRepo protocol that stores entrances in a list.
    """

    def __init__(self):
        self._entrances: list[Entrance] = []

    def get_all_entrances(self) -> list[Entrance]:
        """
        Get all entrances in the restaurant.
        
        Returns:
            A list of all entrances.
        """
        return self._entrances.copy()
    
    def add_entrance(self, entrance: Entrance) -> None:
        """
        Add an entrance to the repository.
        
        Args:
            entrance: The entrance to add.
        """
        self._entrances.append(entrance)