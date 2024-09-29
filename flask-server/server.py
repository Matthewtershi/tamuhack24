<<<<<<< HEAD
from flask import Flask
import sqlite3

conn = sqlite3.connect("testerdb.db")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE users (
                email text,
                first text,
                last text,
                user_ID integer
                )""")

cursor.execute("""CREATE TABLE transactions (
                email text,
                restaurant text,
                item text,
                purchase_amount integer,
                date text
               
                )""")

conn.commit()

conn.close()
=======
from flask import Flask, jsonify
from flask_cors import CORS

from datasources import FWIData, RainData, WindData

import random
>>>>>>> b9d27d2cff8b098167bd940b24f77c0b49ac5ad5

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

<<<<<<< HEAD
@app.route("/")
def home_page():


    return 
=======
@app.route('/api/hotspots', methods=['GET'])
def get_hotspots():
    spots = [[random.uniform(-30, 30), random.uniform(-50, 50)] for _ in range(10)]
    
    return jsonify(spots)
>>>>>>> b9d27d2cff8b098167bd940b24f77c0b49ac5ad5

if __name__ == '__main__':
    app.run(debug=True)
