from flask import Flask, request

app = Flask(__name__)
TOKENS = {"mysecrettoken": "admin"}


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'secret':
       
        return {"message": "Logged in","Token":"mysecrettoken"}
    return {"message": "Invalid credentials"}, 401




def requires_token_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token not in TOKENS:
            return {"message": "Unauthorized"}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@requires_token_auth
def protected():
    return {"message": "Access granted: TOKEN AUTH"}

if __name__ == '__main__':
    app.run(port=5000)