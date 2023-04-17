import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

URL = 'https://www.toki.co.jp/purchasing/TLIHTML.files/sheet001.htm'
PARSER = 'html.parser'
FIRSTLINE_TEXT = 'TOKISTAR CODE'
SCHEDULE_WIDTH = 5
ELEMENT = 'td'
U3000 = '\u3000'
ZERO = "0"


def make_soup():
    html = requests.get(URL)
    soup = BeautifulSoup(html.content, PARSER)
    lines = soup.find_all(ELEMENT)
    page = []
    for line in lines:
        text = line.get_text()
        if text == U3000:
            text = ZERO
        page.append(text)
    return page


def find_datapoints(page):
    # find index of schedule header
    # indicated by FIRSTLINE_TEXT
    first_line = 0
    for first_line, d in enumerate(page):
        if d == FIRSTLINE_TEXT:
            break
    # traverse backwards from FIRSTLINE_TEXT until blank found
    # then move forward 1 place where the first shipping date and remember the index
    first_date = 0
    for first_date in range(first_line, 0, -1):
        if page[first_date] == "":
            first_date += 1
            break
    return first_line, first_date


def trim_page(page, first_line, first_date):
    # calculate number of shipping dates and width of table
    num_dates = first_line - first_date
    line_length = num_dates + SCHEDULE_WIDTH

    # move shipping dates to proper location
    for i in range(num_dates):
        page[first_date + line_length + i] = page[first_line - num_dates + i]

    # slice off everything before FIRSTLINE_TEXT
    return page[first_line:]


def make_table(page, first_line, first_date):
    num_dates = first_line - first_date
    line_length = num_dates + SCHEDULE_WIDTH
    # calculate number of rows in table
    num_lines = (len(page) // line_length) - 1
    # convert list into table
    table = []
    for i in range(num_lines):
        line = []
        for j in range(line_length):
            line.append(page[i + i * (line_length - 1) + j])
        line = line[:1] + line[SCHEDULE_WIDTH:]
        table.append(line)
    return table


def make_schedule(table):
    # delete notes in part numbers
    # convert quantites to float values
    num_lines = len(table)
    num_dates = len(table[0]) - SCHEDULE_WIDTH
    for i in range(1, num_lines):
        temp = re.split("[^\\w-]+", table[i][0])
        table[i][0] = temp[0]
        for j in range(1, num_dates + 1):
            table[i][j] = float(table[i][j])

    header = table[0]
    df = pd.DataFrame.from_records(table[1:], columns=header)
    return df


def validate_schedule():
    print()


def translate_schedule():
    print()


def get_schedule():
    page = make_soup()
    first_line, first_date = find_datapoints(page)
    page = trim_page(page, first_line, first_date)
    table = make_table(page, first_line, first_date)
    schedule = make_schedule(table)
    validate_schedule()
    translate_schedule()
    return schedule
