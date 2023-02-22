import os
from typing import List
import pandas as pd

import consts

"""Class to read create and update a csv file"""


class CsvParser:

    def __init__(self, csv_filename):
        """If the csv file exists we just keep the name
        otherwise we create an csv file with just the headers"""

        if not csv_filename:
            raise ValueError("No file name for CvsParser object")
        self.csv_filename = csv_filename
        # if file not exists create one with only headers
        does_file_exist = os.path.isfile(self.csv_filename)
        if not does_file_exist:
            self.create_csv_file_with_headers()

    def append_to_file(self, data_list_to_append: List[List[str]], mode: str = 'a'):
        """
        param data_list_to_append:
        param mode: 'a' for append 'w' for override
        """
        if len(data_list_to_append) == 0:
            print("Empty list to append")
            return 0
        df = pd.DataFrame.from_records([flight.__dict__.values() for flight in data_list_to_append],
                                       columns=consts.CSV_HEADERS)
        df.to_csv(self.csv_filename, mode=mode, index=False, header=True)

    def csv_to_list(self):
        df = pd.read_csv(self.csv_filename)
        return df.to_dict('records')

    def create_csv_file_with_headers(self):
        df = pd.DataFrame(columns=consts.CSV_HEADERS)
        df.to_csv(self.csv_filename, index=False)


if __name__ == '__main__':
    CsvParser('s.csv')
    exit(0)
    csv_parser = CsvParser('db.csv')
    dict_ = csv_parser.csv_to_list()
    for row in dict_:
        print(row)
    # print(list(dict_))
