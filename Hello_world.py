from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/index')
def home():
    return render_template("index.html")

@app.route('/index1')
def home():
    return render_template("index.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template("contact.html")

    try:
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        message = request.form.get('message')

        print(f"Received submission: Name={name}, Mobile={mobile}, Email={email}, Message={message}")

        return jsonify({
            'success': True,
            'data': {
                'name': name,
                'mobile': mobile,
                'email': email,
                'message': message
            }
        })
    except Exception as e:
        print("Error handling contact POST:", e)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/getcustomer/<int:id>')
@app.route('/getcustomer/<int:id>/<string:name>')
def getcustomer(id, name=None):
    if name:
        return f'Customer ID: {id}, Name: {name}'
    return f'Customer ID: {id}'


# query parameter
@app.route('/train')
def train_info():
    train_name = request.args.get('name', '').lower()

    if train_name == "shatabdi":
        return jsonify({"train": "Shatabdi", "time": "7 AM"})
    elif train_name == "chennai express":
        return jsonify({"train": "Chennai Express", "time": "7 PM"})
    else:
        return jsonify({"message": "NO DATA FOUND"})


# multiple query parameter (&)
@app.route('/multrain')
def train_info1():
    train_name = request.args.get('name', '').lower()
    coach_type = request.args.get('coach', '')  # keep original casing/user string
    train_type = request.args.get('type', '')

    if train_name == "shatabdi":
        return jsonify({
            "train": "Shatabdi",
            "time": "7 AM",
            "coach": coach_type or "AC",
            "type": train_type or "Express"
        })

    elif train_name == "chennai express":
        return jsonify({
            "train": "Chennai Express",
            "time": "7 PM",
            "coach": coach_type or "Non-AC",
            "type": train_type or "Express"
        })

    else:
        return jsonify({"message": "NO DATA FOUND"})


# DYNAMIC NAME data (same as you had)
users = [
    {'name': 'John Doe', 'age': 25, 'email': 'john@example.com'},
    {'name': 'Jane Smith', 'age': 17, 'email': 'jane@example.com'},
    {'name': 'Bob Johnson', 'age': 30, 'email': 'bob@example.com'}
]

# context variable (keep as you used)
context = {
    'title': 'Flask Templates Demo',
    'users': users,
    'current_user': 'John Doe'
}

@app.route('/about')
def about():
    namenode = request.args.get('name')
    namelist = ["siva","sai","Raju"]

    # --- Merge context safely so we don't pass same key twice ---
    ctx = dict(context)                # copy original context
    ctx.update({
        'name': namenode,
        'namelistdata': namelist
    })

    # now pass a single expanded dict (no duplicate 'users' problem)
    return render_template("about.html", **ctx)


# optional: show how to use plain explicit passing (you can keep this or remove)
@app.route('/about1')
def about1():
    namenode = request.args.get('name')
    namelist = ["siva","sai","Raju"]
    # explicit passing (no context)
    return render_template("about.html", name=namenode, namelistdata=namelist, users=users, title="About1 (explicit)", current_user="John Doe")


@app.route('/api/check_source')
def check_source():
    source = request.args.get('source', '').lower()
    if source == 'abacus':
        return jsonify({"message": "hii from abacus", "source": "Abacus"})
    elif source == 'onyx':
        return jsonify({"message": "hii from onyx", "source": "Onyx"})
    else:
        return jsonify({"message": "Unknown source. Please specify 'abacus' or 'onyx'.", "source": "Unknown"})


@app.route('/api_view')
@app.route('/api_view/<source>')
def api_view(source=None):
    return render_template("api_view.html", source=source)


if __name__ == '__main__':
    app.run(debug=True)
