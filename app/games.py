import collections
import logging
import sched
import threading
import time
import traceback
from datetime import datetime, timedelta
from pprint import pprint
from typing import Dict, List, NamedTuple, Set, Tuple
from uuid import uuid4

from apscheduler.schedulers.background import BackgroundScheduler

from game import Game

scheduler = BackgroundScheduler()
scheduler.start()


@scheduler.scheduled_job(trigger="interval", minutes=15)
def cleanup():
    GAMES.cleanup()
    pass


class GameTuple(NamedTuple):
    time: datetime
    game: Game


class Games:
    def __init__(self) -> None:
        self.games: Dict[str, GameTuple] = {}

    def cleanup(self) -> None:

        pprint(self.games)
        games_to_remove: List[str] = []
        for game_id, game in self.games.items():
            if game.time < datetime.now() - timedelta(hours=1):
                games_to_remove.append(game_id)
        for game_id in games_to_remove:
            logging.warning(f"Removing game with id {game_id}")
            del self.games[game_id]

    def get_game(self, game_id: str) -> Game:
        return self.games[game_id].game

    def get_game_by_player(self, player_name: str) -> Game | None:
        for _, game in self.games.items():
            if player_name in [player.name for player in game.game.players]:
                return game.game
        return None

    def delete_game_by_player(self, player_name: str) -> None:
        for game_id, game in self.games.items():
            if player_name in [player.name for player in game.game.players]:
                logging.warning(f"Removing game with id {game_id}")
                del self.games[game_id]
                return
        return

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
