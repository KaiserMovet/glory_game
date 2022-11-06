import logging
from typing import Dict, Iterable, Set

from flask import Flask, jsonify, make_response, request
from flask.wrappers import Response

from game import Color

from .games import GAMES

NAMES: Set[str] = set()
app = Flask(__name__)


def refresh_games():
    pass


def get_response(
    data: object | None = None,
    code: int = 201,
    message="Done",
) -> Response:
    res: Dict[str, object] = {
        "message": message,
        "code": "SUCCESS" if code == 201 else "Failure",
    }
    if data is not None:
        res["response"] = data
    return make_response(jsonify(res), code)


@app.route("/")
def index():
    return "Web App with Python Flask!"


@app.route("/api/new", methods=["GET"])
def new_player() -> Response:
    player = request.args["name"]
    NAMES.add(player)
    data = {"message": "Done", "code": "SUCCESS", "response": {"name": player}}
    return get_response(data)


@app.route("/api/new_game")
def new_game() -> Response:
    global NAMES
    game_id = GAMES.new_game(NAMES)
    NAMES = set()
    return get_response({"game_id": game_id})


@app.route("/api/game/<game_id>")
def get_game(game_id: str) -> Response:
    try:
        game = GAMES.get_game(game_id)
    except KeyError:
        return get_response(code=404, message="Game not found")
    return get_response(game.get_data())


@app.route("/api/game/<game_id>/player/<player_name>", methods=["POST"])
def make_move(game_id: str, player_name: str) -> Response:
    game = GAMES.get_game(game_id)
    move = request.json["move"]
    match move["type"]:
        case "get3":
            colors = {Color[color.upper()] for color in move["colors"]}
            game.get_3_coins(player_name, colors)
            return get_response()
        case "get2":
            color = move["color"].upper()
            game.get_2_coins(player_name, color)
            return get_response()
        case "buy":
            card_id = move["card_id"]
            game.buy_card(player_name, card_id)
            return get_response()
        case "pass":
            game.pass_move(player_name)
            return get_response()
    return get_response(message="Wrong type of move", code=404)
