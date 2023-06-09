import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def webscrape():
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
    return df


def validate(schedule):
    df = pd.read_csv("./data/validate.csv")
    valdict = dict(zip(df['Vendor Part Num'], df['Part Number']))
    validated = True
    for index, row in schedule.iterrows():
        if index in valdict:
            continue
        else:
            print(f"{index} not found in validation table.")
            validated = False
    if not validated:
        exit(1)


def translate(schedule):
    df = pd.read_csv("./data/translate.csv")
    transdict = dict(zip(df['Part Number'], df['Factor']))
    for index, row in schedule.iterrows():
        if index in transdict:
            factor = transdict[index]
            row = row * factor
            temp = []
            for r in row:
                temp.append(r)
            schedule.loc[index] = temp


def get_schedule():
    schedule = webscrape()
    validate(schedule)
    translate(schedule)
    return schedule


def get_backlog():
    df = pd.read_csv("./data/bl.txt")
    df[['Qty Ordered']] = df[['Qty Ordered']].multiply(df['UM_Multiplier'], axis='index')
    df = df.groupby('Part Number').sum()
    df = df.drop(columns=['UM_Multiplier'])
    return df


def get_hfr():
    df = pd.read_csv("./data/hfr.txt")
    df[['Qty Ordered']] = df[['Qty Ordered']].multiply(df['UM_Multiplier'], axis='index')
    df = df.groupby('Part Number').sum()
    df = df.drop(columns=['UM_Multiplier'])
    return df


def get_data():
    df = pd.read_csv("./data/data.txt")
    return df


if __name__ == '__main__':
    pd.options.display.max_columns = None
    schedule = get_schedule()
    backlog = get_backlog()
    hfr = get_hfr()
    data = get_data()
    header = ['Part Number', 'On Hand', 'Backlog', 'Released', 'HFR', 'On Order', 'T-Avail', 'R-Avail', 'Reorder']
    header.extend(schedule.columns)
    df = pd.DataFrame(columns=header)
    df['Part Number'] = data['Part Number']
    df['On Hand'] = data['QtyRealTimeOnHand']
    df['On Order'] = data['QtyOnPurchaseOrder']
    df['Reorder'] = data['Minimum_Stock_Level']
    df[['Backlog', 'Released', 'HFR', 'T-Avail', 'R-Avail']] = 0
    df[schedule.columns] = 0
    for row in df.index:
        key = df.loc[row, 'Part Number']
        if key in backlog:
            df.loc[row, 'Backlog'] = backlog.loc[key, 'Qty Ordered']
            print(df.loc[row, 'Backlog'])
    # print(df)
