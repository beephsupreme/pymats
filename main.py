from backlog import get_backlog
from hfr import get_hfr
from schedule import get_schedule

if __name__ == '__main__':
    schedule = get_schedule()
    # pd.options.display.max_columns = None
    # print(schedule)
    backlog = get_backlog()
    hfr = get_hfr()
    print(hfr)
