from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


# Flask setup
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/stats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DB schema definition
class Stats(db.Model):
    """ DB Schema Initialization Example
    # >>> from app import db
    # >>> from app import Stats
    # >>> from datetime import datetime
    # >>> db.create_all()
    # >>> stats = Stats(betting_is_open=False, blue_bets=0, blue_mushrooms=0, red_bets=0, red_mushrooms=0, latest_update=datetime.now(), status_code=200)
    # >>> db.session.add(stats)
    # >>> db.session.commit()
    # >>> exit()
    """
    id = db.Column(db.Integer, primary_key=True)
    betting_is_open = db.Column(db.Boolean, unique=False, nullable=False)
    blue_bets = db.Column(db.Integer, unique=False, nullable=False)
    blue_mushrooms = db.Column(db.Integer, unique=False, nullable=False)
    red_bets = db.Column(db.Integer, unique=False, nullable=False)
    red_mushrooms = db.Column(db.Integer, unique=False, nullable=False)
    latest_update = db.Column(db.String(30), unique=False, nullable=False)
    status_code = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return json.dumps({
            "live_stats": {
                "betting_is_open": self.betting_is_open,
                "blue": {
                    "bets": self.blue_bets,
                    "mushrooms": self.blue_mushrooms
                },
                "red": {
                    "bets": self.red_bets,
                    "mushrooms": self.red_mushrooms
                },
                "total": {
                    "bets": self.blue_bets + self.red_bets,
                    "mushrooms": self.blue_mushrooms + self.red_mushrooms
                },
                "latest_update": self.latest_update
            },
            "status_code": self.status_code
        })


try:
    db.create_all()
    stats = Stats(betting_is_open=False, blue_bets=0, blue_mushrooms=0, red_bets=0, red_mushrooms=0,
                  latest_update=datetime.now(), status_code=200)
    db.session.add(stats)
    db.session.commit()
except Exception as e:
    print(e)


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
    return render_template('live.html', stats=Stats.query.first())


@app.route('/live-data', methods=['GET', 'POST', 'PUT'])
def live_data():
    # Load the data from the DB
    latest = Stats.query.first()

    status = 500

    # PUT requests
    if request.method == 'PUT':
        status = 201

        # Get the json from the PUT request
        put_data = request.get_json(force=True)['live_stats']

        # Replace each property that is set in the PUT request data
        if 'live_stats' in put_data.keys():
            if 'betting_is_open' in put_data.keys():
                latest.betting_is_open = put_data['betting_is_open']
            if 'blue' in put_data.keys():
                latest.blue_bets = put_data['blue']['bets']
                latest.blue_mushrooms = put_data['blue']['mushrooms']
            if 'red' in put_data.keys():
                latest.red_bets = put_data['red']['bets']
                latest.red_mushrooms = put_data['red']['mushrooms']
    # POST requests
    elif request.method == 'POST':
        status = 201

        # Get the json from the POST request
        post_data = request.get_json(force=True)['live_stats']

        # Replace all the properties using the POST request data
        latest.betting_is_open = post_data['betting_is_open']
        latest.blue_bets = post_data['blue']['bets']
        latest.blue_mushrooms = post_data['blue']['mushrooms']
        latest.red_bets = post_data['red']['bets']
        latest.red_mushrooms = post_data['red']['mushrooms']
    # GET requests
    elif request.method == 'GET':
        status = 200

    # Apply final changes to the DB session
    latest.status_code = status
    latest.latest_update = get_datetime_str()

    # Commit changes to the DB
    db.session.commit()

    print(request.method, status)
    print(latest)

    # Return a JSON response
    return json.loads(latest.__repr__()), status


def get_datetime_str():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
