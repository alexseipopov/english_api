from datetime import date, datetime

import sqlalchemy as sa

from .. import db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.Text, unique=True)
    email = sa.Column(sa.Text, unique=True)
    password = sa.Column(sa.Text)
    level = sa.Column(sa.Integer, nullable=False, default=1)
    code_id = sa.Column(sa.Integer, sa.ForeignKey('code.id', ondelete='CASCADE'))
    code = db.relationship("Code", backref='code', lazy=True)


class Code(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    code_value = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String)

    def __repr__(self):
        return f"{self.code} {self.name}"


class Group(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    label = sa.Column(sa.Text)
    level = sa.Column(sa.Integer, nullable=False, default=0)
    status = sa.Column(sa.Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.label}: {self.level} level"


class Word(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    word_en = sa.Column(sa.Text, nullable=False)
    word_ru = sa.Column(sa.Text, nullable=False)
    example_en = sa.Column(sa.Text, nullable=False)
    audio_path = sa.Column(sa.Text)
    image_path = sa.Column(sa.Text)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id', ondelete="CASCADE"), nullable=False)
    group = db.relationship('Group', backref='group', lazy=True)
    transcription = sa.Column(sa.Text, nullable=False)
    example_ru = sa.Column(sa.Text, nullable=False)

    def __repr__(self) -> str:
        return f"<Word> {self.word_en}"


class Status(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.Integer, unique=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False)

    def __repr__(self) -> str:
        return f"Status {self.number}. {self.description}"


class UserWordStatus(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id', ondelete="CASCADE"))
    word_id = sa.Column(sa.Integer, sa.ForeignKey('word.id', ondelete="CASCADE"))
    status_id = sa.Column(sa.Integer, sa.ForeignKey('status.id', ondelete="CASCADE"))
    update_time = sa.Column(sa.DateTime, default=datetime.utcnow)


class Statistic(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id'), nullable=False)
    start = sa.Column(sa.Date, default=date.today, nullable=False)
    finish = sa.Column(sa.Date)
    learning = sa.Column(sa.Integer, default=0, nullable=False)
    learned = sa.Column(sa.Integer, default=0, nullable=False)
