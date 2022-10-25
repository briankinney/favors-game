from pathlib import Path
from typing import Union, Dict, Callable, Optional, Any
import pathlib

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import application.models
from application.models import query_data_with_template


def get_chart_src(title=""):
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar(title=title)
    filename = './static/dataset1.png'
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


def chart_player_ranking_by_jollies(this_game: int = 29) -> Path:
    """
    Draw a horizontal barchart ranking players by the amount of jollies received in the game identified by this_game.
    If this_game is None, the result for game id 29 will be drawn.
    Save figure as "most_jollies_{this_game}.png" in static folder and return file name.
    """
    df = pd.DataFrame(
        query_data_with_template(
            template_file='rank_players_by_jollies.sql',
            game_id=this_game
        )
    ).astype({'n_jollies': int})

    png_file = pathlib.Path('static') / f'most_jollies_{this_game}.png'

    fig, ax = plt.subplots(1, 1, dpi=300)
    ax = sns.barplot(data=df, y='receiver_name', x='n_jollies', orient='h', color='tab:green')
    plt.title('Most jollies: the happiest person on earth')
    plt.xlabel('jollies received')
    plt.ylabel('')
    plt.xlim(0, df['n_jollies'].max() + 2)
    for patch in ax.patches:
        x, y = patch.get_width(), patch.get_y() + 0.5 * patch.get_height()
        plt.text(0.5 + x, y,
                 f'{x:.0f}',
                 ha='center', va='center')
    plt.savefig(png_file)

    print(f'Figure saved as {png_file} showing {len(df.index)} bars')

    return png_file






