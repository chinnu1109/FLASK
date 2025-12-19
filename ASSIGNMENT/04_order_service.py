from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/orders')
def orders():
    users = requests.get("http://localhost:5001/users").json()

    return jsonify({
        "order_id": 101,
        "user": users[0]["name"],
        "item": "Laptop"
    })

if __name__ == '__main__':
    app.run(port=5002, debug=True)
