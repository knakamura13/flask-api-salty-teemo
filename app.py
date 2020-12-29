from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return jsonify({
        "status_code": 200,
        "result": "Welcome to the unofficial Salty Teemo REST API!"
    })

@app.route('/live-data', methods=['GET', 'POST'])
def live_data():
    data = {}
    log_file = 'data/liveDataCurrent.json'

    # POST requests
    if request.method == 'POST':
        # Get the json from the request
        data = request.get_json()

        # Write json to file
        with open(log_file, 'w+') as out_file:
            json.dump(data, out_file)

        # Return the new data, indicating the POST was successful
        return jsonify({
            "status_code": 201,
            "result": data
        }), 201

    # GET requests
    elif request.method == 'GET':
        # Read data from file
        with open(log_file, 'r+') as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                data['error'] = str(e)

                # Return an error with code 500
                return jsonify({
                    "status_code": 500,
                    "result": data
                }), 500

        # Return the contents of the json file, indicating the GET was successful
        return jsonify({
            "status_code": 200,
            "result": data
        }), 200
