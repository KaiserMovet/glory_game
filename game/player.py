from typing import Dict

from .card import Card
from .color import Color
from .inventory import Inventory


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.inventory = Inventory()

    @property
    def points(self) -> int:
        return self.inventory.points

    def can_buy(self, card: Card) -> bool:
        """
        Check if the card can be bought by player.


        Args:
            card (Card): card to be checked

        Returns:
            bool: True, if the card can be bought
        """
        return self.inventory.can_buy(card)

    def buy(self, card: Card) -> Dict[Color, int] | None:
        """
        Buy the given card.

        Args:
            card (Card): card to be bought

        Returns:
            Dict[Color, int] | None: None if the card cannot be bought.
            Otherwise dict with payment
        """
        return self.inventory.buy(card)

    def is_winner(self, points_to_win: int) -> bool:
        return points_to_win <= self.inventory.points

    def get_data(self) -> dict:
        return self.inventory.get_data()

    def __repr__(self) -> str:
        return f"<Player: {self.name}>"
