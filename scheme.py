from marshmallow import Schema, fields


class ParticipantSchema(Schema):
    uid = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    picture = fields.String(required=True)
    location = fields.String(required=True)
    about = fields.String(required=True)


participant_scheme = ParticipantSchema()
