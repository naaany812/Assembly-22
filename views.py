from werkzeug.security import generate_password_hash, check_password_hash
from assembly22 import app, db
from flask import jsonify, request
from assembly22.models import Participant, Event, Location, Enrollment
from assembly22.scheme import participant_scheme


@app.route("/locations/", methods=["GET"])
def locations():
    return jsonify([])


@app.route("/events/", methods=["GET"])
def events():
    return jsonify([])


@app.route("/enrollments/<int:event_id>", methods=["POST", "DELETE"])
def post_enrollements(event_id):
    if request.method == "POST":
        return jsonify({"status": "success"})
    elif request.method == "DELETE":
        return jsonify({"status": "success"})


@app.route("/register/", methods=["POST"])
def register():
    data = request.json
    email = db.session.query(Participant).filter(
        Participant.email == data.get("email")).first()
    if email:
        return jsonify({"status": "error"}), 500
    participant = Participant(
        name=data.get("name"),
        email=data.get("email"),
        password=generate_password_hash(data.get("password")),
        picture=data.get("picture"),
        location=data.get("location"),
        about=data.get("about")
    )
    db.session.add(participant)
    try:
        db.session.commit()
    except Exception:
        return jsonify(), 500
    return jsonify(
        participant=participant_scheme.dump(participant),
        uid=participant.uid,
        password=data.get("password")
    )


@app.route("/auth/", methods=["POST"])
def auth():
    return jsonify({"status": "success", "key": 111111111})


@app.route("/profile/", methods=["GET"])
def profile():
    return jsonify({
        "id": 1,
        "picture": "",
        "city": "nsk",
        "about": "",
        "enrollments": []})
