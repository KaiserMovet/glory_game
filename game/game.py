from typing import Dict, Iterable, List

from .card import Card, CardDict
from .player import Player


class Game:
    def __init__(self, player_names: Iterable[str]) -> None:
        self.players: List[Player] = [Player(name) for name in player_names]
        self.deck: Dict[int, CardDict] = {
            1: CardDict(),
            2: CardDict(),
            3: CardDict(),
        }
        self.current_player_index = 0

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(
            self.players
        )

    def get_data(self) -> dict:
        player_data = {}
        for player in self.players:
            player_data[player.name] = player.get_data()
        cards_data = {}
        for level, cards in self.deck.items():
            cards_data[level] = [card.get_data() for card in cards]
        data = {"players": player_data, "deck": cards_data}
        return data
