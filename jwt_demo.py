from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
jwt = JWTManager(app)

users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'role': 'admin'
    }
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)


    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if username in users and check_password_hash(users[username]['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/about', methods=['GET'])
def about():
    return jsonify({
        "title": "About JSON Web Tokens (JWT)",
        "definition": "JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.",
        "how_it_works": "Information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.",
        "why_use_it": "It's compact, self-contained, and works across different programming languages, making it ideal for stateless authentication in modern web applications."
    }), 200


if __name__ == '__main__':
    app.run(debug=True)