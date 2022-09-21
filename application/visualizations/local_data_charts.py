import pandas as pd
import matplotlib.pyplot as plt


def get_chart_src(title=""):
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar(title=title)
    filename = './static/dataset1.png'
    fig.savefig(filename)
    return filename


def get_bar_chart(): # Brett!
    pass


def get_leaderboard(): # YiJun!
    pass


def get_favor_list(name="my name"): # Lu
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

    filename = "./static/my_favors.html"
    with open(filename, 'w') as fp:
        fp.write(html)

    return filename