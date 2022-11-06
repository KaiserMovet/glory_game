from .inventory import Inventory
from .card import Card


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

    def buy(self, card: Card) -> bool:
        """
        Buy the given card.

        Args:
            card (Card): card to be bought
        """
        return self.inventory.buy(card)

    def get_data(self) -> dict:
        return self.inventory.get_data()
