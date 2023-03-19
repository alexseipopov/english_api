import sqlalchemy as sa

from .. import db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.Text)
    email = sa.Column(sa.Text)


class Group(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    label = sa.Column(sa.Text)
    level = sa.Column(sa.Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"{self.label}: {self.level} level"


class Word(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    word_en = sa.Column(sa.Text, nullable=False)
    word_ru = sa.Column(sa.Text, nullable=False)
    example = sa.Column(sa.Text)
    audio_path = sa.Column(sa.Text)
    image_path = sa.Column(sa.Text)
    group_id = sa.Column(sa.Integer, db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group', backref='group', lazy=True)
