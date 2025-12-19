# Allows frontend from one origin to access backend API from another origin.

# When CORS NOT Needed?
# Same origin (same port)

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS(app)

@app.route('/data')
def data():
    return jsonify({"message": "Hello from backend (CORS ENABLED)"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
