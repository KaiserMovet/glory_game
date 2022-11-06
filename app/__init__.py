from flask import Flask

app = Flask(__name__, instance_relative_config=False)

app.config["TEMPLATES_AUTO_RELOAD"] = True

from .routes import app
