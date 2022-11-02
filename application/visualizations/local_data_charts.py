import matplotlib
matplotlib.use("Agg")   ## changes the backend to address "not threadsafe" apparently

import pandas as pd
import matplotlib.pyplot as plt

import application.models

def get_chart_src(title=""):
    ## s = pd.Series([1, 2, 3])
    ## fig, ax = plt.subplots()
    ## s.plot.bar(title=title)
    filename = './static/dataset1.png'
    ## fig.savefig(filename)
    return filename


def get_bar_chart_src(): # Brett!
    pass


def get_leaderboard_src(): # YiJun!
    # In this function, we must create a new file that contains the visualization you want to display.
    # Return the path the newly-created file.

    ## get data and sort
    data = pd.DataFrame(application.models.get_exchanges_game_29())
    data.reset_index(inplace = True)
    data = data[["giver", "points"]]
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


def get_favors_table(name="my name"): # Lu
    data = application.models.get_exchanges_game_29()

    print(data)
    dataframe = pd.DataFrame(data)
    html = dataframe.to_html()

    return html