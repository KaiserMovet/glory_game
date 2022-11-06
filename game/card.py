from dataclasses import dataclass, asdict, field
from .color import Color
from _collections_abc import dict_items
from typing import Dict
from uuid import uuid4


class CardDict(dict):
    def add_card(self, card) -> None:
        self[card.obj_id] = card

    def remove_card(self, card: "Card") -> None:
        del self[card.obj_id]


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
