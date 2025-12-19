from flask import Flask, request, make_response

app = Flask(__name__)

# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'secret':
        resp = make_response({"message": "Logged in"})
        resp.set_cookie('user', 'admin')
  #httponly=True document.cookie means can not access this
        return resp
    return {"message": "Invalid credentials"}, 401


# ---------- DECORATOR ----------
def requires_cookie_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        user = request.cookies.get('user')
        if not user:
            return {"message": "Login required (cookie missing)"}, 401
        return f(*args, **kwargs)
    return decorated


# ---------- PROTECTED ----------
@app.route('/protected')
@requires_cookie_auth
def protected():
    user = request.cookies.get('user')
    return {"message": f"Access granted: COOKIE AUTH ({user})"}


# ---------- PUBLIC ----------
@app.route('/public')
def public():
    return {"message": "This is a public endpoint. No auth required."}


if __name__ == '__main__':
    app.run(port=5000)