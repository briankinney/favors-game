import pandas as pd
import matplotlib.pyplot as plt


def get_chart_src(title=""):
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar(title=title)
    filename = './static/dataset1.png'
    fig.savefig(filename)
    return filename


def get_bar_chart_src(): # Brett!
    pass


def get_leaderboard_src(): # YiJun!
    # In this function, we must create a new file that contains the visualization you want to display.
    # Return the path the newly-created file.

    # For demonstration purposes, just put a random file in there.
    return "/static/wii-music.png"


def get_favors_table(name="my name"): # Lu
    data = [
        {"giver": "foo",
         "receiver": "bar",
         "favor": "Compliments",
         "boosted": True,
         "points": 10},
        {"giver": "foo",
         "receiver": "bar",
         "favor": "Compliments",
         "boosted": True,
         "points": 10},
        {"giver": "foo",
         "receiver": "bar",
         "favor": "Compliments",
         "boosted": True,
         "points": 10}
    ]

    dataframe = pd.DataFrame(data)
    html = dataframe.to_html()

    return html