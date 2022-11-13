import logging
from pprint import pprint
from typing import Dict, Iterable, Set

from flask import Flask, abort, jsonify, make_response, render_template, request
from flask.wrappers import Response

from game import Color, IllegalMove

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
def index() -> str:
    return render_template("base.html")


@app.route("/player/<player_name>/game")
def game_view(player_name) -> str:
    return render_template("game.html")


# API functions


@app.route("/api/new", methods=["POST"])
def new_player() -> Response:
    player = request.json["name"]  # type: ignore
    NAMES.add(player)
    data = {"message": "Done", "code": "SUCCESS", "response": {"name": player}}
    return get_response(data)


@app.route("/api/new_players", methods=["GET"])
def get_new_players() -> Response:
    data = {"players": list(NAMES)}
    return get_response(data)


@app.route("/api/new_game")
def new_game() -> Response:
    global NAMES
    game_id = GAMES.new_game(NAMES)
    NAMES = set()
    return get_response({"game_id": game_id})


@app.route("/api/player/<player_name>/game")
def get_game(player_name: str) -> Response:
    game = GAMES.get_game_by_player(player_name)
    if not game:
        return abort(404)
    return get_response(game.get_data())


@app.route("/api/player/<player_name>/move", methods=["POST"])
def make_move(player_name: str) -> Response:
    game = GAMES.get_game_by_player(player_name)
    if not game:
        return abort(404)
    move = request.json["move"]  # type: ignore
    try:
        match move["type"]:
            case "get3":
                colors = {Color[color.lower()] for color in move["colors"]}
                game.get_3_coins(player_name, colors)
                return get_response()
            case "get2":
                color = move["color"].lower()
                game.get_2_coins(player_name, color)
                return get_response()
            case "buy":
                card_id = move["card_id"]
                game.buy_card(player_name, card_id)
                return get_response()
            case "pass":
                game.pass_move(player_name)
                return get_response()
    except IllegalMove:
        return get_response(message="Illegal move", code=404)
    return get_response(message="Wrong type of move", code=404)
