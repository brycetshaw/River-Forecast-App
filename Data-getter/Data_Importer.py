import pandas as pd
import csv
from itertools import islice


def get_row_col(csv_filename, row, col):
    with open(csv_filename, 'rt') as f:
        return next(islice(csv.reader(f), row, row + 1))[col]


def import_flow_data(csv_path):
    print(get_row_col(csv_path, 5, 1))
    flow_raw = pd.read_csv(csv_path, header=10)
    flow_object = DataGroup(get_row_col(csv_path, 5, 1), get_row_col(csv_path, 5, 0), flow_raw)
    return flow_object


class DataGroup:
    def __init__(self, river_gauge_title, river_gauge_id, df_river_flow):
        self.river_gauge_title = river_gauge_title
        self.river_gauge_id = river_gauge_id
        self.df = df_river_flow
        print(f"Created ")
        print(self.df.info)


def main():
    print('hello')
    flow_raw = import_flow_data('../Data/Spillimacheen/08NA011_QR_Apr-2-2020_06_01_41PM.csv')



if __name__ == '__main__':
    main()
