from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
from marshmallow import Schema, fields, validate, ValidationError
from bson import ObjectId



# ----- Setup -----
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client["mydb"]
users_col = db["users"]


class UserSchema(Schema): #this is marshmallow schema
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18))

user_schema = UserSchema()

# ----- Helper -----
def sanitize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# ----- Simple HTML template (INLINE) -----
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>User Test</title>
</head>
<body>
    <h2>Create User</h2>

    <form method="POST" action="/create-user">
        <input type="text" name="name" placeholder="Name" required><br><br>
        <input type="email" name="email" placeholder="Email" required><br><br>
        <input type="number" name="age" placeholder="Age" required><br><br>
        <button type="submit">Create</button>
    </form>

    {% if user %}
        <h3>Created User</h3>
        <pre>{{ user }}</pre>
    {% endif %}

    {% if errors %}
        <h3 style="color:red;">Errors</h3>
        <pre>{{ errors }}</pre>
    {% endif %}
</body>
</html>
"""


# ----- HTML Page -----
@app.get("/")
def home():
    return render_template_string(HTML)

# ----- HTML Form Submit -----
@app.post("/create-user")
def create_user_form():
    try:
        data = user_schema.load({  #verify (validate) the data and convert it to clean Python data.
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "age": int(request.form.get("age"))
        })
    except ValidationError as err:
        return render_template_string(HTML, errors=err.messages)

    res = users_col.insert_one(data)
    created = users_col.find_one({"_id": res.inserted_id})

    return render_template_string(
        HTML,
        user=sanitize(created)
    )



# ----- Run -----
if __name__ == "__main__":
    app.run(debug=True, port=5002)