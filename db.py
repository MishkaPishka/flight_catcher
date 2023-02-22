from typing import List
import consts
import utils
from csv_parser import CsvParser
from flight_data import FlightData


class DataManager(object):

    def __init__(self, cvs_filepath):
        self.cvs_parser = CsvParser(cvs_filepath)
        self.preprocess_data()

    def get_flight_by_id(self, flight_id) -> FlightData:
        """
        :param flight_id:
        :return: FlightData object with flight_id or None if doesn't exist in db
        """
        flights = [FlightData.from_list(flight.values()) for flight in self.cvs_parser.csv_to_list()]
        relevant_flight = list(filter(lambda flight: str(flight.flight_id) == flight_id, flights))
        if len(relevant_flight) > 0:
            return relevant_flight[0]

    def get_flight_list(self) -> List[FlightData]:
        return [FlightData.from_list(flight.values()) for flight in self.cvs_parser.csv_to_list()]

    def get_current_flights(self) -> List[FlightData]:
        return [FlightData.from_list(flight.values()) for flight in self.cvs_parser.csv_to_list()]

    def update_success_values_and_insert_flights(self, new_flights_data: List[FlightData]) -> int:
        """
        sorts current + new flights data according to arrival
        adds success value to new_flights_data (if needed)
        :param new_flights_data:
        :return: number of flights in db
        """
        # get current flights from db
        current_flights = self.get_current_flights()
        # verify new flight_data doesn't contain too many success value
        current_flights.extend(new_flights_data)
        current_flights.sort(key=lambda flight: utils.convert_str_to_time(flight.arrival))

        current_success_count = FlightData.get_current_number_of_successes(current_flights)
        FlightData.set_success_value_of_flights_from_list(current_flights, current_success_count)
        # append new flights to existing ones
        # sort list by arrival time
        self.cvs_parser.append_to_file(current_flights, mode='w')
        return len(current_flights)

    def preprocess_data(self):
        """
        when accessed for the first time we may have records without success value
        therefore we get the records, calculate the values and save them
        """
        data_as_dict: List[FlightData] = [FlightData.from_list(flight.values()) for flight in
                                          self.cvs_parser.csv_to_list()]
        # check if any record is missing a valid success value
        does_exists_entry_with_invalid_success = any([True if flight.success not in [consts.FlightStatus.SUCCESS.value,
                                                                                     consts.FlightStatus.FAIL.value] else False
                                                      for flight in data_as_dict])

        if does_exists_entry_with_invalid_success:
            # if yes - calculate success values and update db
            self.update_success_values_and_insert_flights([])


if __name__ == '__main__':
    x = DataManager('s.csv')
