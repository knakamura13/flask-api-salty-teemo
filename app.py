from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from datetime import datetime
import json
import errno
import os

# Flask setup
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

# Global variables
DATA_DICT = {}
DATA_LOG_FILE = 'data/liveDataCurrent.json'

# Read data from file
with open(DATA_LOG_FILE, 'r') as f:
    try:
        DATA_DICT = json.load(f)
    except FileNotFoundError as e:
        pass


@app.route('/')
def index():
    return jsonify({
        "status_code": 200,
        "result": "Welcome to the unofficial Salty Teemo REST API!"
    })


@app.route('/live')
def test():
    return render_template('live.html', stats=DATA_DICT['live_stats'])


@app.route('/live-data', methods=['GET', 'POST', 'PUT'])
def live_data():
    global DATA_DICT, DATA_LOG_FILE

    status = 500

    # PUT requests
    if request.method == 'PUT':
        # Get the json from the PUT request
        req = request.get_json(force=True)
        status = 201

        # Check each property to see what the PUT request is updating
        if 'live_stats' in req.keys():
            stats = req['live_stats']
            if 'betting_is_open' in stats.keys():
                DATA_DICT['live_stats']['betting_is_open'] = stats['betting_is_open']
            if 'blue' in stats.keys():
                DATA_DICT['live_stats']['blue'] = stats['blue']
            if 'red' in stats.keys():
                DATA_DICT['live_stats']['red'] = stats['red']
            if 'total' in stats.keys():
                DATA_DICT['live_stats']['total'] = stats['total']

        DATA_DICT['live_stats']['latest_update'] = get_datetime_str()
        DATA_DICT['status'] = status

        # Write json to file
        with open(DATA_LOG_FILE, 'w+') as out_file:
            json.dump(DATA_DICT, out_file)

        return jsonify(DATA_DICT), status

    # POST requests
    elif request.method == 'POST':
        # Get the json from the POST request
        req = request.get_json(force=True)
        DATA_DICT = req
        status = 201

        DATA_DICT['status'] = status

        DATA_DICT['live_stats']['latest_update'] = get_datetime_str()

        # Write json to file
        with open(DATA_LOG_FILE, 'w+') as out_file:
            json.dump(DATA_DICT, out_file)

        # Return the new data, indicating the POST was successful
        return jsonify(DATA_DICT), status

    # GET requests
    elif request.method == 'GET':
        # Read data from file
        with open(DATA_LOG_FILE, 'r+') as json_file:
            try:
                DATA_DICT = json.load(json_file)
            except Exception as e:
                DATA_DICT['error'] = str(e)

                # Return an error with code 500
                status = 500
                return jsonify(DATA_DICT), status

        # Return the contents of the json file, indicating the GET was successful
        status = 200
        return jsonify(DATA_DICT), status


def get_datetime_str():
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted
