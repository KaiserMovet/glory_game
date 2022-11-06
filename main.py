import logging
from pprint import pprint

from app import app
from game import Card, Color, Game


def main():
    # game = Game(player_names=["alfa", "bravo", "charlie", "delta"])
    # game.deck[1].add_card(Card(Color.RED, {Color.GREEN: 2}, value=2))
    # pprint(game.get_data())
    logging.debug("debug message")
    logging.info("info message")
    logging.warning("warn message")
    logging.error("error message")
    logging.critical("critical message")
    app.run(host="0.0.0.0", port=81)


if __name__ == "__main__":
    main()
