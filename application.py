# !/usr/bin/env python3

import os
import json
import sqlalchemy
import datetime
import zipfile
import random
import sys

from flask import Flask, render_template, request, send_file
from sqlalchemy.sql import text
from configparser import ConfigParser
from io import BytesIO

app = Flask(__name__)
app.config['TESTING'] = True

DATABASE_URL = f"postgresql://something or other"
engine = sqlalchemy.create_engine(DATABASE_URL)


# Route to homepage
@app.route("/", methods=['GET'])
def render_index():
    return render_template('home.html', page_title="Home")

@app.route("/game/create", methods=['GET'])
def render_game_create():
    return render_template('create.html', page_title="Create a game")

@app.route("/game/create", methods=['POST'])
def create_game():
    pass

@app.route("/game/<id>/join", methods=['GET'])
def render_game_join(id):
    return render_template('join.html', page_title="Join game")

@app.route("/game/<id>/join", methods=['POST'])
def join_game(id):
    pass

@app.route("/game/<id>/play", methods=['GET'])
def render_game_play(id):
    return render_template('play.html', page_title="The Favors Game™")

@app.route("/game/<id>/report", methods=['GET'])
def render_game_report(id):
    return render_template('report.html', page_title=f"Game {id} results")

@app.route("/game/<id>/exchange/create", methods=['POST'])
def exchange_favor(id):
    pass

# Necessary to run app if app.py is executed as a script
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')