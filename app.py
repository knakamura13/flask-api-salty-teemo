from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def index():
    data = {}

    # POST requests
    if request.method == 'POST':
        # Get the json from the request
        data = request.get_json()

        # Write json to file
        with open('output.json', 'w+') as outfile:
            json.dump(data, outfile)

        # Return the new data, indicating the POST was successful
        return jsonify({
            "status_code": 201,
            "result": data
        }), 201

    # GET requests
    elif request.method == 'GET':
        # Read data from file
        with open('output.json', 'r+') as json_file:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
