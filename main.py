import pandas as pd

from schedule import get_schedule

if __name__ == '__main__':
    schedule = get_schedule()
    pd.options.display.max_columns = None
    print(schedule)
