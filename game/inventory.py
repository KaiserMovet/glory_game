from dataclasses import dataclass, field
from collections import defaultdict
from .card import Card, CardDict
from typing import List, Dict
from .color import Color


@dataclass
class Inventory:
    cards: CardDict = field(default_factory=CardDict)
    coins: Dict[Color, int] = field(default_factory=dict)

    def __post_init__(self):
        for color in Color:
            self.coins[color.value] = 0

    @property
    def points(self) -> int:
        return sum([card.value for card in self.cards])

    def get_data(self) -> dict:

        cards_data = {
            card_id: card.get_data() for card_id, card in self.cards.items()
        }
        data = {
            "cards": cards_data,
            "coins": self.coins,
        }
        return data

    def get_color_amount(
        self, color: Color, coins_only=False, cards_only=False
    ) -> int:
        if coins_only and cards_only:
            raise Exception()
        if coins_only:
            return self.coins[color]
        if cards_only:
            len([card for card in self.cards.values() if card.color == color])

        return (
            len([card for card in self.cards.values() if card.color == color])
            + self.coins[color]
        )

    def pay(self, value: int, color: Color) -> None:
        """
        Pay the given value of the given color. Card will be taken into account

        Args:
            value (int): value to pay
            color (Color): color to pay
        """
        value = value - self.get_color_amount(color, cards_only=True)
        if value > 0:
            self.coins[color] -= value

    def can_buy(self, card: Card) -> bool:
        """
        Check if the card can be bought.


        Args:
            card (Card): card to be checked

        Returns:
            bool: True, if the card can be bought
        """
        for color, amount in card.cost.items():
            if self.get_color_amount(color) < amount:
                return False
        return True

    def buy(self, card: Card) -> bool:
        """
        Buy the given card.

        Args:
            card (Card): card to be bought
        """
        if not self.can_buy(card):
            return False
        for color, amount in card.cost.items():
            self.pay(amount, color)
        self.cards.add_card(card)
        return True
