import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt

import application.models

def get_chart_src(title=""):
    #s = pd.Series([1, 2, 3])
    #fig, ax = plt.subplots()
    #s.plot.bar(title=title)
    filename = './static/dataset1.png'
    #fig.savefig(filename)
    return filename


def get_money_chart_src(title="", game_id=29): # Brett!
    filename = './static/money_chart.png'

    players = application.models.get_players(game_id)
    names = [d['name'] for d in players]
    print('NAMES', names)
    balances = [d['money'] if d['money'] is not None else 0 for d in players]
    print('BALANCES', balances)

    fig, ax = plt.subplots(figsize=(8, 3))
    plt.bar(names, balances)
    fig.savefig(filename)

    return filename


def get_leaderboard_src(): # YiJun!
    # In this function, we must create a new file that contains the visualization you want to display.
    # Return the path the newly-created file.

    # For demonstration purposes, just put a random file in there.
    return "/static/wii-music.png"


def get_favors_table(name="my name"): # Lu
    data = application.models.get_exchanges_game_29()

    print(data)
    dataframe = pd.DataFrame(data)
    html = dataframe.to_html()

    return html