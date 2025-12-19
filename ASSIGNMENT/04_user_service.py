from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users')
def users():
    return jsonify([
        {"id": 1, "name": "Raju"},
        {"id": 2, "name": "Sai"}
    ])

if __name__ == '__main__':
    app.run(port=5001, debug=True)
