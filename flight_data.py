import json
from typing import List
import re
import consts
import utils


class FlightData(object):

    def __init__(self, flight_id: str, arrival: str, departure: str, success: str = ''):
        # todo - verify flight_id, departue, arrival are not empty
        self.flight_id = str(flight_id)
        # verify arrival\departure are hh:mm
        r = re.compile("^\\d{2}:\\d{2}$")
        if not (r.search(arrival.strip()) and r.search(departure.strip())):
            raise ValueError(f"Expected strings of type hh:mm, got:{arrival},{departure}")
        self.arrival = arrival
        self.departure = departure
        self.success = success

    def is_flight_under_max_duration(self):
        departure = utils.convert_str_to_time(self.departure)
        arrival = utils.convert_str_to_time(self.arrival)
        diff = utils.subtract_times(departure, arrival)
        return diff <= consts.MAX_FLIGHT_DURATION

    def get_json_repr(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_dict(kwargs):
        return FlightData(**kwargs)

    @staticmethod
    def from_list(args):
        return FlightData(*args)

    @staticmethod
    def sort_flight_list_by_arrival(flight_list: List):
        return flight_list.sort(key=lambda flight: utils.convert_str_to_time(flight.arrival))

    @staticmethod
    def get_current_number_of_successes(flight_list):
        # todo - moveto be static methos in flightDat
        return sum(1 if flight.success == consts.FlightStatus.SUCCESS.value else 0 for flight in flight_list)

    @staticmethod
    def set_success_value_of_flights_from_list(flight_data, current_success_count=0):
        possible_successes_to_add = consts.MAX_FLIGHTS_PER_DAY - current_success_count

        for flight in flight_data:
            # if can still add flight
            if flight.success != consts.FlightStatus.FAIL.value and flight.is_flight_under_max_duration() and current_success_count < possible_successes_to_add:
                flight.success = consts.FlightStatus.SUCCESS.value
                current_success_count += 1
            else:
                flight.success = consts.FlightStatus.FAIL.value



def generate_flight_data_from_json(flights, ignore_success=False) -> List[FlightData]:
    flights_list = []
    for flight in flights:
        flight_data_as_dict = FlightData.from_dict(flight)
        if ignore_success:
            flight_data_as_dict.success = ''
        flights_list.append(FlightData.from_dict(flight))
    return flights_list
