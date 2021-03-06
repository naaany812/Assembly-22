from marshmallow import Schema, fields


class ParticipantSchema(Schema):
    uid = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    picture = fields.String(required=False)
    location = fields.String(required=True)
    about = fields.String(required=True)


participant_scheme = ParticipantSchema()


class LocationSchema(Schema):
    title = fields.String(required=True)
    code = fields.String(required=True)


location_scheme = LocationSchema(many=True)


class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    data = fields.String(required=True)
    time = fields.Time(required=True)
    type = fields.String(required=True)
    category = fields.String(required=True)
    address = fields.String(required=True)
    seats = fields.Integer(required=True)
    location_id = fields.String()
    location = fields.Nested("LocationSchema")


event_scheme = EventSchema(many=True)
