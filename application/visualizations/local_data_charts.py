from pathlib import Path
from typing import Union, Dict, Callable, Optional, Any
import pathlib
import matplotlib
matplotlib.use("Agg")   ## changes the backend to address "not threadsafe" apparently

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import application.models
from application.models import query_data_with_template


def get_chart_src(title=""):
    ## s = pd.Series([1, 2, 3])
    ## fig, ax = plt.subplots()
    ## s.plot.bar(title=title)
    filename = './static/dataset1.png'
    ## fig.savefig(filename)
    return filename


def get_leaderboard_src(): # YiJun!
    # In this function, we must create a new file that contains the visualization you want to display.
    # Return the path the newly-created file.

    ## get data and sort
    data = pd.DataFrame(application.models.get_exchanges_game_29())
    data.reset_index(inplace = True)
    data = data[["giver", "points"]]    ## not sure if should be using boosted points
    data = data.groupby(by=["giver"], as_index = False).sum()
    data.sort_values(inplace=True, by=["points"], ascending=True)
    ## I haven't the foggiest why. but ascending = False, which you would think creates a descending plot?
        ## it doesn't. you get an ascending plot.

    ## start viz
    ## fig = plt.figure(figsize=(10, 5))
    plt.barh(data["giver"], data["points"])
    plt.xlabel("Jollies acquired")
    plt.ylabel("Players in game")
    plt.title("Player Leaderboard")

    ## save viz
    savefile = "./static/leaderboard.png"
    plt.savefig(savefile)

    return savefile

def get_awards_src():
    ## in this function we determine who the winners of the various awards are
    ## assuming only giver can accumulate points, assuming no ties

    ## collection
    awards = {}

    ## get complete transaction log
    ## get data and sort
    data = pd.DataFrame(application.models.get_exchanges_game_29())
    data.reset_index(inplace=True)

    ## could probably encap these into a function
        ## they're all mosts

    ## sweetie, most points from H2H favors
    sweetie = data.query("favor_type == 'Heart To Heart'")[["giver","points"]]
    sweetie = sweetie.groupby(by = ["giver"], as_index = False).sum()
    sweetie.sort_values(inplace = True, by = ["points"], ascending = False)
    awards.update({"sweetie":sweetie["giver"][0]})

    ## most talent, most points created from entertainment favors
    most_talented = data.query("favor_type == 'Entertainment'")[["giver","points"]]
    most_talented = most_talented.groupby(by = ["giver"], as_index = False).sum()
    most_talented.sort_values(inplace = True, by = ["points"], ascending = False)
    awards.update({"most_talented":most_talented["giver"][0]})

    ## most outgoing, most people helped
        ## assuming unique people
    most_outgoing = data[["giver","receiver"]]
    most_outgoing = most_outgoing.groupby(by = ["giver"], as_index = False).nunique()
    most_outgoing.sort_values(inplace = True, by = ["receiver"], ascending = False)
    awards.update({"most_outgoing":most_outgoing["giver"][0]})

    ## best quality, most boosted favors
    best_quality = data.query("boost_value != points")[["giver","exchange_id"]]
    best_quality = best_quality.groupby(by = ["giver"], as_index = False).count()
    best_quality.sort_values(inplace = True, by = ["exchange_id"], ascending = False)
    awards.update({"best_quality":best_quality["giver"][0]})

    awards = pd.DataFrame(awards).T.to_html()

    return awards


# Best Quality: Most boosted favors




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






