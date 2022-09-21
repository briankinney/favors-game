import pandas as pd
import matplotlib.pyplot as plt


def get_chart_src(title=""):
    s = pd.Series([1, 2, 3])
    fig, ax = plt.subplots()
    s.plot.bar(title=title)
    fig.savefig('./static/dataset1.png')
    return './static/dataset1.png'