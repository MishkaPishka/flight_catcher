from enum import Enum

DEFAULT_CSV_FILENAME = 'default.csv'
CSV_HEADERS = ['Flight ID', 'Arrival', 'Departure', 'Success']
MAX_FLIGHT_DURATION = 180
MAX_FLIGHTS_PER_DAY = 20


class FlightStatus(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'
