from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home_page():
    return jsonify({"message": "Welcome to the Flask backend!"})

if __name__ == "__main__":
    app.run(debug=True)