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


def get_money_chart_src(title="Player Wealth Leaderboard", game_id=29): # Brett!
    """
    :param title: the title that will be displayed in the resulting plot
    :param game_id: the ID for the game whose leaderboard should be displayed
    :return: returns the filename of the plot
    """

    filename = './static/money_chart_' + str(game_id) + '.png'

    # Get the player wealth data and prepare it for plotting
    players = application.models.get_players_money(game_id)
    players_list = list(zip([p['money'] for p in players], [p['name'] for p in players]))
    players_list.sort(reverse=True)

    # Plot the chart
    fig, ax = plt.subplots(figsize=(8, 3))
    plt.bar([p[1] for p in players_list], [p[0] for p in players_list])

    # Decorate the figure
    ax.set_title(title)
    ax.set_xlabel('Player')
    ax.set_ylabel('Dollars')

    plt.gcf().subplots_adjust(bottom=0.15)
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