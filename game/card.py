import random
from dataclasses import asdict, dataclass, field
from typing import Dict, List
from uuid import uuid4

from _collections_abc import dict_items

from .color import Color


class CardDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.list = []

    def add_card(self, card) -> None:
        self[card.obj_id] = card
        self.list.append(card)

    def remove_card(self, card: "Card") -> None:
        del self[card.obj_id]

    def remove_card_by_id(self, card_id: str) -> None:
        del self[card_id]

    def shuffle(self) -> None:
        random.shuffle(self.list)

    def get_list(self, amount_of_cards: int | None = None) -> List["Card"]:
        if amount_of_cards is None:
            return self.list
        return self.list[0:amount_of_cards]

    def __delitem__(self, card_id: str) -> None:
        self.list.remove(self[card_id])
        super().__delitem__(card_id)


@dataclass()
class Card:
    color: Color
    cost: Dict[Color, int]
    obj_id: str = field(default_factory=lambda: str(uuid4()))
    value: int = 0

    def get_data(self) -> dict:
        data = asdict(self)
        data["cost"] = self.cost
        return data
