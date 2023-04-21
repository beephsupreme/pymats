import pandas as pd
from backlog import get_backlog
from data import get_data
from hfr import get_hfr
from schedule import get_schedule

if __name__ == '__main__':
    pd.options.display.max_columns = None
    schedule = get_schedule()
    backlog = get_backlog()
    hfr = get_hfr()
    data = get_data()
    print(data)
