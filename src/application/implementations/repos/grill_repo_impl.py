from src.core.entities.grill import Grill
from src.core.repos.GrillRepo import GrillRepo


class GrillRepoImpl(GrillRepo):
    """
    Implementation of the GrillRepo protocol that stores grills in a dictionary.
    """

    def __init__(self):
        self._grills: dict[str, Grill] = {}

    def get_all_grills(self) -> list[Grill]:
        """
        Get all grills in the restaurant.
        
        Returns:
            A list of all grills.
        """
        return list(self._grills.values())
    
    def add_grill(self, grill: Grill) -> None:
        """
        Add a grill to the repository.
        
        Args:
            grill: The grill to add.
            
        Raises:
            ValueError: If a grill with the same ID already exists.
        """
        if grill.id in self._grills:
            raise ValueError(f"Grill with ID {grill.id} already exists")
        
        self._grills[grill.id] = grill
    
    def get_grill(self, grill_id: str) -> Grill:
        """
        Get a grill by ID.
        
        Args:
            grill_id: The ID of the grill to get.
            
        Returns:
            The grill with the specified ID.
            
        Raises:
            KeyError: If no grill exists with the specified ID.
        """
        if grill_id not in self._grills:
            raise KeyError(f"No grill found with ID {grill_id}")
        
        return self._grills[grill_id]