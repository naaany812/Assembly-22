from werkzeug.security import generate_password_hash, check_password_hash
from assembly22 import app, db
from flask import jsonify, request, session
from assembly22.models import Participant, Event, Location, Enrollment
from assembly22.scheme import participant_scheme, location_scheme, event_scheme
from datetime import datetime


# return json of participant without password
def get_json_participant_without_password(participant):
    participant_json = participant_scheme.dump(participant)
    participant_json.pop("password")
    return participant_json


# return all locations from db
@app.route("/locations/", methods=["GET"])
def locations():
    locations = db.session.query(Location).all()
    # if there is no locations then empty list is returned
    if not locations:
        return jsonify([])
    return jsonify(location_scheme.dump(locations))


# return events
# can be used with eventtype and location filters
@app.route("/events/", methods=["GET"])
def events():
    eventtype = request.args.get("eventtype")
    location = request.args.get("location")
    events = db.session.query(Event)
    # check that filters exist and use it
    if eventtype:
        events = events.filter(Event.type == eventtype)
    if location:
        events = events.filter(Event.location_code == location)
    if not events:
        return jsonify([])
    return jsonify(event_scheme.dump(events))


# create enrollment if doesn't exist
# delete enrollement if exist
# return status of operation
@app.route("/enrollments/<int:event_id>", methods=["POST", "DELETE"])
def post_enrollements(event_id):
    event = db.session.query(Event).get(event_id)
    # check that event exists
    if not event:
        return jsonify({"status": "No event error"}), 500
    # create enrollment flow
    if request.method == "POST":
        registrations = len(db.session.query(Enrollment).filter(
            Enrollment.event_id == event_id).all())
        if registrations < event.seats:
            user = session.get("user")
            if not user:
                return jsonify({"status": "auth error"}), 500
            enrollment = db.session.query(Enrollment).filter(db.and_(
                    Enrollment.participant_uid == user.get("uid"),
                    Enrollment.event_id == event_id)
                ).first()
            if enrollment:
                return jsonify(status="enrollment error"), 500
            enrollment = Enrollment(
                event_id=event_id,
                participant_uid=user.get("uid"),
                datetime=datetime.today()
            )
            db.session.add(enrollment)
            try:
                db.session.commit()
            except Exception:
                return jsonify({"status": "db error"}), 500
            return jsonify({"status": "success"})
        return jsonify({"status": "seats error"}), 500
    # delete enrollment flow
    elif request.method == "DELETE":
        user = session.get("user")
        if not user:
            return jsonify(status="auth error"), 200
        enrollment = db.session.query(Enrollment).filter(db.and_(
                Enrollment.participant_uid == user.get("uid"),
                Enrollment.event_id == event_id)).first()
        if not enrollment:
            return jsonify(status="error"), 500
        db.session.delete(enrollment)
        try:
            db.session.commit()
        except Exception:
            return jsonify(status="db error"), 500
        return jsonify({"status": "success"})


# register new participant
# return json with participant data
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
        location=data.get("location"),
        about=data.get("about")
    )
    db.session.add(participant)
    try:
        db.session.commit()
    except Exception:
        return jsonify({"status": "failed"}), 500
    return jsonify(
        participant=participant_scheme.dump(participant),
        uid=participant.uid,
        password=data.get("password")
    )


# auth by participant and create variable in session with uid and email
# return json with participant data without password
@app.route("/auth/", methods=["POST"])
def auth():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    participant = db.session.query(Participant).filter(
        Participant.email == email).first()
    if not participant:
        return jsonify({"status": "error"}), 500
    if not check_password_hash(participant.password, password):
        return jsonify({"status": "error"}), 500
    session["user"] = dict(
        email=participant.email,
        uid=participant.uid
    )
    return jsonify(get_json_participant_without_password(participant))


# return participant profile without password
@app.route("/profile/<int:uid>", methods=["GET"])
def profile(uid):
    participant = db.session.query(Participant).get(uid)
    if not participant:
        return jsonify({"status": "error"})
    return jsonify(get_json_participant_without_password(participant))
