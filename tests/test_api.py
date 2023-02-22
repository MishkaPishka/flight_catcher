import pytest
from flight_data import FlightData
from main import app, init_db


class TestAPI:

    def test_add_flights(self):
        init_db(app, 'test_filename_add_flights.csv')
        response = app.test_client().post('/add-flights', json={'flights': self.get_flights_to_add()})
        expected_response = str(2)
        assert response.status_code == 200
        assert response.data.decode('utf-8') == expected_response

    def test_check_existing_flight(self):
        existing_flight_id = '1'
        init_db(app, 'test_filename_existing.csv')
        flight_to_add = FlightData.from_list(['1', '10:00', '09:00', 'success'])
        app.db.update_success_values_and_insert_flights([flight_to_add])
        response = app.test_client().get(f'/get-flight-data/{existing_flight_id}')
        assert response.status_code == 200
        expected_response_data = {'arrival': '10:00', 'departure': '09:00', 'flight_id': '1', 'success': 'success'}
        actual_flight_data = response.json
        assert actual_flight_data == expected_response_data

    def test_check_non_existing_flight(self):
        existing_flight_id = 'X'
        init_db(app, 'test_filename_non_existing.csv')
        response = app.test_client().get(f'/get-flight-data/{existing_flight_id}')
        assert response.status_code == 404

    def test_get_flights(self):
        expected_db_name = 'api_tests_data.csv'
        init_db(app, expected_db_name)
        response = app.test_client().get(f'/get-flights-list/')
        assert response.status_code == 200
        expected_response_data = [{'arrival': '02:00', 'departure': '00:00', 'flight_id': '1', 'success': 'success'},
                                  {'arrival': '02:10', 'departure': '01:00', 'flight_id': '2', 'success': 'success'},
                                  {'arrival': '04:00', 'departure': '00:13', 'flight_id': '3', 'success': 'fail'}]

        actual_response_data = response.json
        assert actual_response_data == expected_response_data

    def test_add_flight_is_sorted(self):
        expected_db_name = 'api_tests_list_sorted.csv'
        init_db(app, expected_db_name)
        unsorted_flight_data = [{'arrival': '03:00', 'departure': '00:00', 'flight_id': '1', 'success': 'success'},
                                {'arrival': '02:10', 'departure': '01:00', 'flight_id': '2', 'success': 'success'},
                                {'arrival': '04:00', 'departure': '00:13', 'flight_id': '3', 'success': 'fail'}]

        app.test_client().post('/add-flights', json={'flights': unsorted_flight_data})

        response = app.test_client().get(f'/get-flights-list/')
        assert response.status_code == 200
        expected_response_data = [
            {'arrival': '02:10', 'departure': '01:00', 'flight_id': '2', 'success': 'success'},
            {'arrival': '03:00', 'departure': '00:00', 'flight_id': '1', 'success': 'success'},
            {'arrival': '04:00', 'departure': '00:13', 'flight_id': '3', 'success': 'fail'}]

        actual_response_data = response.json
        assert actual_response_data == expected_response_data

    def get_flights_to_add(self):
        return [{'flight_id': 'a', 'arrival': '10:00', 'departure': '01:00'},
                {'flight_id': 'b', 'arrival': '02:00', 'departure': '01:00'}]

    @classmethod
    def teardown_class(cls):
        import os
        os.remove('test_filename_add_flights.csv')
        os.remove('api_tests_list_sorted.csv')
        os.remove('test_filename_existing.csv')
        os.remove('test_filename_non_existing.csv')
