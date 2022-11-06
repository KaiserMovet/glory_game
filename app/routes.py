from typing import Dict, Iterable, Set

from flask import Flask, jsonify, make_response, request
from flask.wrappers import Response

from .games import GAMES

NAMES: Set[str] = set()
app = Flask(__name__)


def refresh_games():
    pass


def get_response(
    data: object | None = None,
    code: int = 201,
    message="Done",
):
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
