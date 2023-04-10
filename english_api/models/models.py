from datetime import datetime

import sqlalchemy as sa

from .. import db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.Text, unique=True)
    email = sa.Column(sa.Text, unique=True)
    password = sa.Column(sa.Text)


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
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id', ondelete="CASCADE"), nullable=False)
    group = db.relationship('Group', backref='group', lazy=True)

    def __repr__(self) -> str:
        return f"<Word> {self.word_en}"


class Status(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.Integer, unique=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False)

    def __repr__(self) -> str:
        return f"Status {self.number}. {self.description}"


class User_Has_Word(db.Model):
    # __tablename__ = 'association'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete="CASCADE"))
    word_id = sa.Column(sa.Integer, sa.ForeignKey('word.id', ondelete="CASCADE"))
    status_id = sa.Column(sa.Integer, sa.ForeignKey('status.id', ondelete="CASCADE"))
    update_time = sa.Column(sa.DateTime, default=datetime.utcnow)
