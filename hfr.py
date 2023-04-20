import numpy as np
import pandas as pd


def get_hfr():
    df = pd.read_csv("./data/hfr.txt")
    df[['Qty Ordered']] = df[['Qty Ordered']].multiply(df['UM_Multiplier'], axis='index')
    df = df.groupby('Part Number').sum()
    df = df.drop(columns=['UM_Multiplier'])
    return df

