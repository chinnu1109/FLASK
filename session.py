from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route('/login1', methods=['POST'])
def login1():
    if request.form['username'] == 'admin' and request.form['password'] == 'secret':
        session['user'] = request.form['username']
        return {"message": "Logged in"}
    return {"message": "Invalid credentials"}, 401


def requires_session_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return {"message": "Login required"}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@requires_session_auth
def protected():
    return {"message": f"Access granted: SESSION AUTH ({session['user']})"}

if __name__ == '__main__':
    app.run(port=5000)