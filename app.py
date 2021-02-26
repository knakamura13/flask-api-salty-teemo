from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'


# Global data object
data = {}
log_file = 'data/liveDataCurrent.json'

# Read data from file
with open(log_file, 'r') as json_file:
    try:
        data = json.load(json_file)
    except Exception as e:
        pass

@app.route('/')
def index():
    return jsonify({
        "status_code": 200,
        "result": "Welcome to the unofficial Salty Teemo REST API!"
    })

@app.route('/live-data', methods=['GET', 'POST', 'PUT'])
def live_data():
    global data, log_file

    status = 500

    # PUT requests
    if request.method == 'PUT':
        # Get the json from the PUT request
        req = request.get_json()
        status = 201

        # Check each property to see what the PUT request is updating
        if 'live_stats' in req.keys():
            stats = req['live_stats']
            if 'betting_is_open' in stats.keys():
                data['live_stats']['betting_is_open'] = stats['betting_is_open']
            if 'blue' in stats.keys():
                data['live_stats']['blue'] = stats['blue']
            if 'red' in stats.keys():
                data['live_stats']['red'] = stats['red']
            if 'total' in stats.keys():
                data['live_stats']['total'] = stats['total']

        data['live_stats']['latest_update'] = '000-111-000'
        data['status'] = status

        # Write json to file
        with open(log_file, 'w+') as out_file:
            json.dump(data, out_file)

        return jsonify(data), status

    # POST requests
    elif request.method == 'POST':
        # Get the json from the POST request
        req = request.get_json()

        # Write json to file
        with open(log_file, 'w+') as out_file:
            json.dump(req, out_file)

        # Return the new data, indicating the POST was successful
        status = 201
        return jsonify({
            "status_code": status,
            "data": req
        }), status

    # GET requests
    elif request.method == 'GET':
        # Read data from file
        with open(log_file, 'r+') as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                data['error'] = str(e)

                # Return an error with code 500
                status = 500
                return jsonify({
                    "status_code": status,
                    "result": data
                }), status

        # Return the contents of the json file, indicating the GET was successful
        status = 200
        return jsonify({
            "status_code": status,
            "data": data
        }), status
