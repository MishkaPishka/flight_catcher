from typing import List
from flask import Flask, jsonify, request
import consts
import db
from flight_data import FlightData, generate_flight_data_from_json

app = Flask(__name__)


def init_db(flask_app, path_to_file):
    if not path_to_file:
        path_to_file = consts.DEFAULT_CSV_FILENAME
    flask_app.db_filepath = path_to_file
    flask_app.db = db.DataManager(path_to_file)
    return flask_app


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return "exception", 500


@app.route('/add-flights', methods=["POST"])
def add_flights():
    """
    add flights to db
    keeps the data sorted by arrival time
    calculates the success of the new flights
    doesn't touch success of old flights
    """
    flights = request.json.get('flights')
    flight_data: List[FlightData] = generate_flight_data_from_json(flights, ignore_success=True)
    flights_added = app.db.update_success_values_and_insert_flights(flight_data)
    return str(flights_added), 200


@app.route('/get-flight-data/<string:flight_id>', methods=["GET"])
def get_flight_data(flight_id: str):
    """
    If flight_id exists in today's db - give it
    else - either we get that None or we have exception somewhere - > make sure that
    exception is called or printed and\or that if flight doesn't exist -> print it
    """
    flight_data: FlightData = app.db.get_flight_by_id(flight_id)
    if not flight_data:
        return {'error': f'Could not retrieve info about flight id:{flight_id}'}, 404
    return jsonify(flight_data.__dict__), 200


@app.route('/get-flights-list/', methods=["GET"])
def get_flights_list():
    flights: FlightData = app.db.get_flight_list()
    return jsonify([flight_data.__dict__ for flight_data in flights]), 200


if __name__ == '__main__':
    db_name = ''
    # app.config.update(
    #     TESTING=True,
    # )
    app = init_db(app, db_name)

    app.run(debug=True, use_reloader=False)
#
