import csv
import logging
import random
from collections import ChainMap
from pprint import pprint
from typing import Dict, Iterable, List, Set

from .card import Card, CardDict
from .color import Color
from .player import Player

GENERATE_CARDS = True
CARDS_LEVEL_1 = 40
CARDS_LEVEL_2 = 30
CARDS_LEVEL_3 = 20


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


class CustomChainMap:
    def __init__(self, list_of_dicts: List[dict]):
        self.list_of_dicts = list_of_dicts

    def __getitem__(self, key):
        for dic in self.list_of_dicts:
            if key in dic:
                return dic[key]
        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key):
        logging.info(f"Removing {key} card from deck")
        for dic in self.list_of_dicts:
            if key in dic:
                del dic[key]
                return
        raise KeyError(f"Key {key} not found")

    def remove(self, key):
        del self[key]


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

        self.deck_all: CustomChainMap = CustomChainMap(
            list((self.deck.values()))
        )
        self.current_player_index = 0
        self.coins = {}
        for color in Color:
            self.coins[color.value] = 7

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def _load_cards_from_csv(self):
        with open("game/cards.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            next(reader)
            for row in reader:
                cost_dict = {}
                cost_dict[Color.white] = int(row[3])
                cost_dict[Color.red] = int(row[4])
                cost_dict[Color.green] = int(row[5])
                cost_dict[Color.blue] = int(row[6])
                cost_dict[Color.black] = int(row[7])
                card = Card(
                    color=Color[row[1].lower()],
                    cost=cost_dict,
                    value=int(row[2]),
                )
                self.deck[int(row[0])].add_card(card)

    @staticmethod
    def _generate_card(color: Color, total_cost: List, values: List) -> Card:
        cost = {color2: 0 for color2 in Color}
        other_colors: List[Color] = [
            color2 for color2 in Color if color2 is not color
        ]
        for _ in range(random.choice(total_cost)):
            cost[random.choice(other_colors)] += 1
        card = Card(color=color, cost=cost, value=random.choice(values))
        return card

    def _generate_cards(self) -> None:
        for color in Color:
            # Level 1
            for _ in range(CARDS_LEVEL_1 // 5):
                self.deck[1].add_card(
                    self._generate_card(
                        color=color, total_cost=[3] * 3 + [4] * 1, values=[0]
                    )
                )
            # Level 2
            for _ in range(CARDS_LEVEL_2 // 5):
                self.deck[2].add_card(
                    self._generate_card(
                        color=color,
                        total_cost=[5] * 1 + [6] * 3 + [7] * 1,
                        values=[0] + [1] * 4 + [2] * 2,
                    )
                )
            # Level 3
            for _ in range(CARDS_LEVEL_3 // 5):
                self.deck[3].add_card(
                    self._generate_card(
                        color=color,
                        total_cost=[7] + [8] * 3 + [9] * 1,
                        values=[3] * 2 + [4] + [5],
                    )
                )

    def _load_cards(self) -> None:
        if not GENERATE_CARDS:
            self._load_cards_from_csv()
        self._generate_cards()

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

        data = {
            "players": player_data,
            "deck": cards_data,
            "cards_in_deck": {
                level: len(cards) for level, cards in self.deck.items()
            },
            "coins": self.coins,
            "current_player": self.current_player.name,
        }
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
        payment = self.current_player.buy(card)
        if payment is None:
            raise IllegalMove(
                f"Player {player_name} cannot buy card: {card_id}"
            )
        self.deck_all.remove(card_id)
        for color, coins in payment.items():
            self.coins[color] += coins

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
