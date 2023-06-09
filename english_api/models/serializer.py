from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    phone = fields.String()
    email = fields.String()
    password = fields.String()


class WordSchema(Schema):
    id = fields.Integer()
    word_en = fields.String()
    word_ru = fields.String()
    example_en = fields.String()
    example_ru = fields.String()
    transcription = fields.String()
    audio_path = fields.String()
    image_path = fields.String()
    group_id = fields.Integer()
