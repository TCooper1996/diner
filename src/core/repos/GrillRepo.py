from typing import Protocol

from src.core.entities.grill import Grill


class GrillRepo(Protocol):
    def get_all_grills(self) -> list[Grill]:
        """Get all grills in the restaurant."""
        ...

    def get_grill(self, grill_id: str) -> Grill:
        """Get a specific grill by its ID."""
        ...