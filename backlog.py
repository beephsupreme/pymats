import numpy as np
import pandas as pd


def get_backlog():
    df = pd.read_csv("./data/bl.txt")
    df[['Qty Ordered']] = df[['Qty Ordered']].multiply(df['UM_Multiplier'], axis='index')
    df = df.groupby('Part Number').sum()
    df = df.drop(columns=['UM_Multiplier'])
    return df

