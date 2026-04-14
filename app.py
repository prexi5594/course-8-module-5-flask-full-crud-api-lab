from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
events = []
next_id = 1


# ✅ REQUIRED BY TESTS
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# Helper function
def find_event(event_id):
    return next((event for event in events if event["id"] == event_id), None)


# Root route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Events API"}), 200


# GET all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events), 200


# POST create event
@app.route("/events", methods=["POST"])
def create_event():
    global next_id

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_event = Event(next_id, data["title"])

    event_dict = new_event.to_dict()

    events.append(event_dict)
    next_id += 1

    return jsonify(event_dict), 201


# PATCH update event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "title" in data:
        event["title"] = data["title"]

    return jsonify(event), 200


# DELETE event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)