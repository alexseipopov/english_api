import sqlalchemy as sa

from .. import db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.Text)
    email = sa.Column(sa.Text)


class Group(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    level = sa.Column(sa.Integer, nullable=False, default=0)
    words = db.relationship('Word', backref='group', lazy=True)


class Word(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    word_en = sa.Column(sa.Text, nullable=False)
    word_ru = sa.Column(sa.Text, nullable=False)
    example = sa.Column(sa.Text)
    audio = sa.Column(sa.Text)
    image = sa.Column(sa.Text)
    group = sa.Column(sa.Integer, sa.ForeignKey('group.id'), nullable=False)
