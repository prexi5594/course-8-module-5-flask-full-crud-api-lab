from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
events = []
next_id = 1


# Helper function
def find_event(event_id):
    return next((event for event in events if event["id"] == event_id), None)


# ✅ Root route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Events API"})


# ✅ GET all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events)


# ✅ POST create event
@app.route("/events", methods=["POST"])
def create_event():
    global next_id

    data = request.get_json()

    # Input validation
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_event = {
        "id": next_id,
        "title": data["title"]
    }

    events.append(new_event)
    next_id += 1

    return jsonify(new_event), 201


# ✅ PATCH update event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if "title" in data:
        event["title"] = data["title"]

    return jsonify(event)


# ✅ DELETE event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return jsonify({"message": "Event deleted"})


if __name__ == "__main__":
    app.run(debug=True)