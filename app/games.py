import collections
from datetime import datetime
from typing import Dict, NamedTuple, Set, Tuple
from uuid import uuid4

from game import Game


class GameTuple(NamedTuple):
    time: datetime
    game: Game


class Games:
    def __init__(self) -> None:
        self.games : Dict[str, GameTuple] = {}

    def get_game(self, game_id: str)-> Game:
        return self.games[game_id].game

    def new_game(self, names: Set[str]) -> str:
        """
        Create a new game

        Args:
            names (List[str]): List of names of players

        Returns:
            str: id of the game
        """
        now = datetime.now()
        game_id = str(uuid4())
        self.games[game_id] = GameTuple(time=now, game=Game(names))
        return game_id

GAMES = Games()