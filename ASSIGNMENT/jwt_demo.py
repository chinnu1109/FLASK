from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)

# JWT secret key
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

# 1️⃣ LOGIN (Generate JWT)
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # Dummy verification
    if username == "admin" and password == "123":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid credentials"}), 401


# 2️⃣ VERIFIED USERS ONLY (JWT REQUIRED)
@app.route('/verified')
@jwt_required()
def verified():
    current_user = get_jwt_identity()
    return jsonify({
        "msg": f"Hello {current_user}, you are VERIFIED"
    })


# 3️⃣ PUBLIC API (NO JWT)
@app.route('/public')
def public():
    return jsonify({
        "msg": "This is PUBLIC API, anyone can access"
    })


if __name__ == '__main__':
    app.run(debug=True)
