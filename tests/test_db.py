# load fake db from json csv
# or load from empty file as well
import pytest
from csv_parser import CsvParser
from db import DataManager
from flight_data import FlightData


# pytest -q test_db.py
# pytest
# create db by day

class TestDB:

    def test_init_csv_parser_with_no_filename_throws_exception(self):
        with pytest.raises(ValueError, match="No file name for CvsParser object"):
            csv_file_name = CsvParser('')

    def test_init_csv_with_file_name_creates_correct_headers(self):
        filename = 'test_filename.csv'
        CsvParser(filename)
        import pandas as pd
        expected_value = {0: {0: 'Flight ID'}, 1: {0: 'Arrival'}, 2: {0: 'Departure'}, 3: {0: 'Success'}}
        actual_value = pd.read_csv(filename, header=None).to_dict()
        assert expected_value == actual_value


    def test_load_actual_file(self):
        filename = 'test_db.csv'
        csv_parser = CsvParser(filename)
        import pandas as pd
        records = csv_parser.csv_to_list()
        expected_records_length = 3
        actual_records_length = len(records)
        assert expected_records_length == actual_records_length

    def test_data_manager_get_flight(self):
        flight_number = '2'
        csv_file_path = 'data_manager_tests_data.csv'
        data_manager = DataManager(csv_file_path)
        flight_data = data_manager.get_flight_by_id(flight_number).__dict__
        expected_flight_data = FlightData.from_list(['2', '02:10', '01:00', 'success']).__dict__
        assert flight_data == expected_flight_data

    def test_data_manager_get_current_flights(self):
        csv_file_path = 'data_manager_tests_data.csv'
        data_manager = DataManager(csv_file_path)
        actual_count = len(data_manager.get_current_flights())
        expected_count = 3
        assert actual_count == expected_count

    @classmethod
    def teardown_class(cls):
        import os
        os.remove('test_filename.csv')
