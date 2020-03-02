from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    data = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    type = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    location_code = db.Column(
        db.String,
        db.ForeignKey("locations.code"),
        nullable=False)
    participants = db.relationship("Enrollment", back_populates="event")


class Participant(db.Model):
    __tablename__ = 'participants'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    enrollments = db.relationship(
        "Enrollment",
        back_populates="participant")


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        primary_key=True)
    participant_uid = db.Column(
        db.String,
        db.ForeignKey("participants.uid"),
        primary_key=True)
    participant = db.relationship("Participant", back_populates="enrollments")
    event = db.relationship("Event")
    datetime = db.Column(db.DateTime, nullable=False)


class Location(db.Model):
    __tablename__ = "locations"
    title = db.Column(db.String, nullable=True)
    code = db.Column(db.String, primary_key=True)
