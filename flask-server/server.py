from flask import Flask, jsonify, g
from flask_cors import CORS

from datasources import DataSources

import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_datasources():
    if 'ds' not in g:
        g.ds = DataSources()
    return g.ds

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/hotspots', methods=['GET'])
def get_hotspots():
    spots = [[random.uniform(-30, 30), random.uniform(-50, 50)] for _ in range(10)]
    
    return jsonify(spots)

if __name__ == '__main__':
    app.run(debug=True)
