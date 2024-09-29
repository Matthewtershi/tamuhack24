from flask import Flask, jsonify, g
from flask_cors import CORS
from datasources import DataSources

import pandas as pd

import joblib
import threading

from points import points

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_ds_lock():
    if 'dslock' not in g:
        g.dslock = threading.Lock()
    return g.dslock

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
    with get_ds_lock():
        ds = get_datasources()
        with ds.FWI.lock, ds.Rain.lock, ds.GFS.lock:
            FWIs = []
            for lat, long in points:
                try:
                    FWIs.append(ds.FWI.get_data(lat, long))
                except:
                    print(f"ERROR: {lat}, {long}")
                    return
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
