# !/usr/bin/env python3

import os
import json
from application.models import *
import datetime
import zipfile
import random
import sys

from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
from configparser import ConfigParser
from io import BytesIO

from application.metabase.embed_link import get_dashboard_embed

app = Flask(__name__)
app.config['TESTING'] = True

Session(app)

# Route to homepage
@app.route("/", methods=['GET'])
def render_index():
    return render_template('home.html', page_title="Home")


@app.route("/game/create", methods=['GET'])
def render_game_create():
    return render_template('create.html', page_title="Create a game")


@app.route("/game/create", methods=['POST'])
def post_create_game():
    data = request.form
    print('data is:', data)
    db_result = create_game(data)
    print("db result is ", db_result)
    return redirect(url_for('join_game', game_id=db_result))


@app.route("/game/<game_id>/join", methods=['GET'])
def render_game_join(game_id):
    game_data = get_game_data(game_id)
    print('game data is a list of columns', game_data)
    return render_template('join.html', page_title="Join game", game_data=game_data)


@app.route("/game/<game_id>/join", methods=['POST'])
def join_game(game_id):
    form_data = request.form
    print('form data is:', form_data)
    player_id = create_player(form_data, game_id)
    print("db result is ", player_id)
    player_data = get_player_data(player_id)

    # save user data to session
    return redirect(url_for('render_game_play', game_id=game_id))


@app.route("/game/<game_id>/play", methods=['GET'])
def render_game_play(game_id):
    players = get_players()
    favors = get_favors()
    my_favors = get_my_favors(user_id=session["user_id"])
    return render_template('play.html', page_title="The Favors Game™",
                           players=players,
                           favors=favors,
                           my_favors=my_favors)


@app.route("/game/<id>/report", methods=['GET'])
def render_game_report(id):
    dashboardUrl = get_dashboard_embed(game_id=id)
    return render_template('report.html', page_title=f"Game {id} results", embedUrl=dashboardUrl)


@app.route("/game/<id>/exchange/create", methods=['POST'])
def exchange_favor(id):
    pass


# Necessary to run app if app.py is executed as a script
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
