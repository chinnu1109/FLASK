from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

# MySQL connection string
# Note: The password 'Sivasai@12345' contains '@', which is a reserved character in URLs.
# We must replace it with '%40'.
engine = create_engine(
    "mysql+pymysql://root:Sivasai%4012345@localhost:3306/event_management",
    echo=True
)

@app.route("/")
def home():
    return {"message": "Flask + MySQL running"}

# --------------------------------------------------
# Get all events
# --------------------------------------------------
@app.route("/events", methods=["GET"])
def get_events():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM events"))
        events = [dict(row._mapping) for row in result]
    return jsonify(events)

# --------------------------------------------------
# Add new event
# --------------------------------------------------
@app.route("/events", methods=["POST"])
def add_event():
    data = request.get_json()

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO events
                (event_name, event_date, venue, description, organizer, contact_email)
                VALUES
                (:event_name, :event_date, :venue, :description, :organizer, :contact_email)
            """),
            data
        )

    return {"message": "Event added successfully"}, 201

if __name__ == "__main__":
    app.run(debug=True, port=5001)
