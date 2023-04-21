import pandas as pd


def get_data():
    df = pd.read_csv("./data/data.txt")
    df.insert(2, "bl", 0.0)
    df.insert(3, "rl", 0.0)
    df.insert(4, "hold", 0.0)
    df.insert(6, "ta", 0.0)
    df.insert(7, "ra", 0.0)
    labels = ['Part Number', 'On Hand', 'Backlog', 'Released', 'HFR', 'On Order', 'T-Avail', 'R-Avail', 'Reorder']
    df.columns = labels
    return df

