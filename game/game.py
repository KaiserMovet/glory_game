import csv
import logging
from collections import ChainMap
from pprint import pprint
from typing import Dict, Iterable, List, Set

from .card import Card, CardDict
from .color import Color
from .player import Player


class GameException(Exception):
    pass


class IllegalMove(GameException):
    pass


def player_move(f):
    def wrapper(*args):
        args[0].check_player(args[1])
        f(*args)
        args[0].next()

    return wrapper


class Game:
    def __init__(self, player_names: Iterable[str]) -> None:
        self.players: List[Player] = [Player(name) for name in player_names]
        self.deck: Dict[int, CardDict] = {
            1: CardDict(),
            2: CardDict(),
            3: CardDict(),
        }
        self._load_cards()
        for level in self.deck.values():
            level.shuffle()

        self.deck_all: ChainMap = ChainMap(*list(self.deck.values()))
        self.current_player_index = 0
        self.coins = {}
        for color in Color:
            self.coins[color.value] = 7

        pprint(self.get_data())

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def _load_cards(self) -> None:
        with open("game/cards.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            next(reader)
            for row in reader:
                cost_dict = {}
                cost_dict[Color.WHITE] = int(row[3])
                cost_dict[Color.RED] = int(row[4])
                cost_dict[Color.GREEN] = int(row[5])
                cost_dict[Color.BLUE] = int(row[6])
                cost_dict[Color.BLACK] = int(row[7])
                card = Card(
                    color=Color[row[1].upper()],
                    cost=cost_dict,
                    value=int(row[2]),
                )
                self.deck[int(row[0])].add_card(card)

        pass

    def next(self) -> None:
        previous_player = self.current_player
        self.current_player_index = (self.current_player_index + 1) % len(
            self.players
        )
        logging.info(
            f"Next player: {previous_player.name} -> {self.current_player.name}"
        )

    def get_data(self, get_hidden_cards=False) -> dict:
        player_data = {}
        for player in self.players:
            player_data[player.name] = player.get_data()

        cards_data = {}
        for level, cards in self.deck.items():
            if get_hidden_cards:
                cards_data[level] = [
                    card.get_data() for card in cards.get_list()
                ]
            else:
                cards_data[level] = [
                    card.get_data() for card in cards.get_list(5)
                ]

        data = {"players": player_data, "deck": cards_data, "coins": self.coins}
        return data

    def check_player(self, player_name: str) -> None:
        if player_name != self.current_player.name:
            raise GameException(
                f"{player_name} is not a current player. Current player is {self.current_player.name}"
            )

    # Moves
    @player_move
    def buy_card(self, player_name, card_id: str) -> None:
        logging.info(f"Player {player_name} buy card {card_id}")
        card = self.deck_all[card_id]
        self.current_player.buy(card)
        del self.deck_all[card_id]

    @player_move
    def get_3_coins(self, player_name, colors: Set[Color]) -> None:
        logging.info(f"Player {player_name} get 3 coins: {', '.join(colors)}")
        if len(colors) > 3:
            raise IllegalMove(
                f"Player {player_name} can buy 3 coins, tried to "
                f"buy {len(colors)} coins."
            )
        for color in colors:
            if self.coins[color] < 1:
                raise IllegalMove(
                    f"Player {player_name} tried to buy {color} coins. "
                    f"Number of this coins is less than 1"
                )
            self.coins[color] -= 1
            self.current_player.inventory.coins[color] += 1

    @player_move
    def get_2_coins(self, player_name, color: Color) -> None:
        logging.info(f"Player {player_name} get 2 coins: {color}")
        if self.coins[color] < 2:
            raise IllegalMove(
                f"Player {player_name} tried to buy 2 {color} coins. "
                f"Number of this coins is less than 2"
            )
        self.coins[color] -= 2
        self.current_player.inventory.coins[color] += 2

    @player_move
    def pass_move(self, player_name) -> None:
        logging.info(f"Player {player_name} pass move")
