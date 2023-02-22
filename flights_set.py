from typing import List

from flight_data import FlightData


def FlightsSet():
    def __init__(self, day, flights_data: List[FlightData] = []):
        self.day = day
        self.flights_data = flights_data

    def as_json(self):
        pass

    @staticmethod
    def is_max_success(flights_set):
        # check if flights set is above 20
        return True

