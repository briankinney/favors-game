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
    data = get_favors_table(name="Brian")
    fig, ax = plt.subplots()
    ax.bar(data["giver"], height=data["points"])
    filename = "./static/bar-chart.png"
    fig.savefig(filename)
    return "/static/bar-chart.png"


def get_leaderboard_src(): # YiJun!
    pass


def get_favors_table(name="my name"): # Lu
    data = [
        {"giver": "baz",
         "receiver": "bar",
         "favor": "Compliments",
         "boosted": True,
         "points": 5},
        {"giver": "foo",
         "receiver": "bar",
         "favor": "Compliments",
         "boosted": True,
         "points": 10},
        {"giver": "bing",
         "receiver": "bar",
         "favor": "Compliments",
         "boosted": True,
         "points": 15}
    ]

    dataframe = pd.DataFrame(data)
    return dataframe
    html = dataframe.to_html()

    return html