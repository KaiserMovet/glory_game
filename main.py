import logging
from pprint import pprint

from app import app
from game import Card, Color, Game


def main():
    game = Game(player_names=["alfa", "bravo", "charlie", "delta"])
    # game.deck[1].add_card(Card(Color.RED, {Color.GREEN: 2}, value=2))
    # data= game.get_data(get_hidden_cards=True)
    # pprint(data['deck'])
    # print(1, len(data['deck'][1]))
    # print(2, len(data['deck'][2]))
    # print(3, len(data['deck'][3]))

    app.run(
        host="0.0.0.0",
        port=81,
        debug=True,
    )


if __name__ == "__main__":
    main()
