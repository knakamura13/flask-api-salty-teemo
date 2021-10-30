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
DATA_LOG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'live_data_log.json')

# Read data from file
with open(DATA_LOG_FILE, 'r') as initial_data_file:
    try:
        DATA_DICT = json.load(initial_data_file)
    except FileNotFoundError:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), DATA_LOG_FILE)


@app.errorhandler(Exception)
def basic_error(err):
    return f'<h3>Oops, the Flask server crashed!</h3><p>{err}</p>', 501


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico'), 200


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
        status = 201

        # Get the json from the PUT request
        req = request.get_json(force=True)

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
        DATA_DICT['status'] = status
        DATA_DICT['live_stats']['latest_update'] = get_datetime_str()

        # Write json to file
        with open(DATA_LOG_FILE, 'w+') as out_file:
            json.dump(DATA_DICT, out_file)

    # POST requests
    elif request.method == 'POST':
        status = 201

        # Get the json from the POST request
        req = request.get_json(force=True)
        DATA_DICT = req
        DATA_DICT['status'] = status
        DATA_DICT['live_stats']['latest_update'] = get_datetime_str()

        # Write json to file
        with open(DATA_LOG_FILE, 'w+') as out_file:
            json.dump(DATA_DICT, out_file)

    # GET requests
    elif request.method == 'GET':
        status = 200

        # Read data from file
        with open(DATA_LOG_FILE, 'r') as data_file:
            try:
                DATA_DICT = json.load(data_file)
            except (FileNotFoundError, FileExistsError) as e:
                status = 500
                DATA_DICT['error'] = str(e)
                return jsonify(DATA_DICT), status

    return jsonify(DATA_DICT), status


def get_datetime_str():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
