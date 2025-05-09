from dataclasses import dataclass
from typing import Protocol

from src.core.entities.customer import Customer


class CustomerRepo(Protocol):
    def get_all_customers(self) -> list[Customer]:
        """Get all customers."""
        ...

    def get_customer(self, customer_id: str) -> Customer:
        """Get a customer by ID."""
        ...

    def get_count(self) -> int:
        """Get the count of customers."""
        ...

    def add_customer(self, customer: Customer) -> None:
        """Add a new customer."""
        ...

    def update_customer(self, customer: Customer) -> None:
        """Update an existing customer."""
        ...