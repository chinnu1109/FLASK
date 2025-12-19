from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

# Dummy users (normally from DB)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "employee": {"password": "emp123", "role": "employee"}
}

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = USERS.get(data["username"])

    if user and user["password"] == data["password"]:
        token = create_access_token(
            identity=data["username"],
            additional_claims={"role": user["role"]}
        )
        return jsonify(access_token=token)

    return jsonify(message="Invalid credentials"), 401


# ---------- ADMIN-ONLY DECORATOR ----------
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify(message="Admin access only"), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


# ---------- PAYMENT PAGE ----------
@app.route("/payment")
@admin_required
def payment():
    return jsonify(message="Welcome Admin, Payment Page")


# ---------- COMMON PAGE ----------
@app.route("/dashboard")
@jwt_required()
def dashboard():
    return jsonify(message="Admin & Employee both can access")


@app.route("/test")
def test():
    return "Flask is working"

if __name__ == "__main__":
    app.run(debug=True,port=5005)
