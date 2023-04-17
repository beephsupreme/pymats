from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import requests

PN = "Part Number"
OH = "On Hand"
OO = "On Order"
RO = "Reorder"
BL = "Backlog"
RLS = "Released"
HFR = "HFR"
TA = "T-Avail"
RA = "R-Avail"
MP = "Multiplier"
VP = "Vendor Part Num"


def validate(schedule):
    df = pd.read_csv("./data/validate.csv")
    valdict = dict(zip(df[VP], df[PN]))
    validated = True
    for index, row in schedule.iterrows():
        if index in valdict:
            continue
        else:
            print(f"{index} not found in validation table.")
            validated = False
    if not validated:
        exit(1)

def translate():
    print('translation skipped')


def get_schedule():
    html = requests.get('https://www.toki.co.jp/purchasing/TLIHTML.files/sheet001.htm')
    soup = BeautifulSoup(html.content, 'html.parser')
    table = soup.find_all('table')
    df = pd.read_html(str(table))[0]
    df = df.drop(columns=[1, 2, 3, 4])
    df.iloc[3][0] = 'TOKISTAR CODE'
    df.iloc[4] = df.iloc[3]
    df = df.drop(index=[0, 1, 2, 3])
    df.reset_index(drop=True, inplace=True)
    df = df.replace(np.NAN, 0)
    df.columns = df.iloc[0]
    df = df[1:]
    new_names = []
    temp = 0
    for name in df.columns:
        if temp == 0:
            new_names.append(name)
        else:
            new_names.append(str(temp) + ":" + name)
        temp += 1
    df.columns = new_names
    for index, row in df.iterrows():
        temp = re.split("[^\\w-]+", row[0])
        df.at[index, 'TOKISTAR CODE'] = temp[0]
    for name in df.columns:
        if name == 'TOKISTAR CODE':
            continue
        df[name] = pd.to_numeric(df[name])
    df = df.groupby('TOKISTAR CODE').sum()
    validate(df)
    translate()
    return df
