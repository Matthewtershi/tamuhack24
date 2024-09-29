from flask import Flask, jsonify, g
from flask_cors import CORS

from datasources import DataSources

import random
import joblib
import pandas as pd

import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

points = [
    [57.92900996,-97.0816169],
    [27.09801359,-112.81176051],
    [45.75263624,-111.0033351],
    [23.44729451,-94.09268845],
    [42.3891449,-91.31661755],
    [48.7929325,-85.1165672],
    [23.9807458,-110.23275588],
    [18.42757772,-95.52909601],
    [22.22032968,-85.68552048],
    [53.2581922,-88.18004554],
    [26.5621422,-83.87259051],
    [50.1391022,-74.69180214],
    [25.06497028,-109.66824819],
    [34.6696197,-85.46701865],
    [49.0498863,-111.55614649],
    [36.26829164,-113.57370684],
    [44.97645301,-71.72194676],
    [35.80289987,-89.38390997],
    [46.0270959,-81.60818029],
    [25.38161645,-109.603156],
    [43.3125477,-118.18247617],
    [55.42886155,-110.41466286],
    [45.70863455,-70.00345934],
    [23.52861768,-87.09628074],
    [43.72662065,-115.4990241],
    [58.17312434,-89.55532982],
    [60.69055189,-94.92634646],
    [37.11558312,-82.26420403],
    [34.01361957,-108.96631017],
    [48.77212941,-107.65463661],
    [45.69938326,-90.10437457],
    [35.48843709,-87.70098933],
    [36.42061993,-105.03070001],
    [53.62940036,-87.68047122],
    [34.75282218,-110.02942078],
    [42.27506439,-107.6964712],
    [44.5515405,-85.61650641],
    [40.95614942,-80.75756254],
    [47.89372018,-99.28542618],
    [31.56742683,-113.65020646],
    [43.54236035,-96.52387237],
    [31.22894737,-95.96348543],
    [36.15041869,-77.14738199],
    [30.08196298,-89.52548768],
    [25.05760996,-107.18192255],
    [39.83069688,-118.18695045],
    [41.50560601,-124.41777941],
    [40.55282711,-105.38733901],
    [55.05676674,-96.39069283],
    [30.49393192,-108.20006391],
]

def get_datasources():
    if 'ds' not in g:
        g.ds = DataSources()
    return g.ds

def get_model():
    if 'model' not in g:
        g.model = joblib.load("model2.joblib")
    return g.model

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/hotspots', methods=['GET'])
def get_hotspots():
    ds = get_datasources()
    with ds.FWI.lock, ds.Rain.lock, ds.GFS.lock:
        FWIs = [ds.FWI.get_data(lat, long) for lat, long in points]
        rains = [ds.Rain.get_data(lat, long) for lat, long in points]
        tmp_rh_winds = [ds.GFS.get_data(lat, long) for lat, long in points]
        d = {
            "FFMC": [fwi["FFMC"] for fwi in FWIs],
            "DMC": [fwi["DMC"] for fwi in FWIs], 
            "DC": [fwi["DC"] for fwi in FWIs], 
            "ISI": [fwi["ISI"] for fwi in FWIs],
            "temp": [tmp for tmp, _, _ in tmp_rh_winds],
            "RH": [rh for _, rh, _ in tmp_rh_winds], 
            "wind": [wind for _, _, wind in tmp_rh_winds], 
            "rain": [rain for rain in rains]
        }

    df = pd.DataFrame(d)
    df['TempAndFFMC'] = df['temp'] / df['FFMC']
    
    layer = (pd.concat([df[['ISI', 'temp', 'DC', 'ISI', 'RH', 'wind','TempAndFFMC']]], axis=1)).values
    likelihoods = get_model().predict(layer).transpose()[0]

    likely_points = [{"point": point, "confidence": float(likelihoods[i])} for i, point in enumerate(points) if likelihoods[i] >= 0.5]

    return jsonify(likely_points)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
