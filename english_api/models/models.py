from datetime import datetime
import sqlalchemy as sa

from .. import db


# user_has_word_table = db.Table("user_has_word",
#     sa.Column("id", sa.BigInteger, primary_key=True),
#     sa.Column("user_id", sa.Integer, sa.ForeignKey('user.id', ondelete="CASCADE")),
#     sa.Column("word_id", sa.Integer, sa.ForeignKey('word.id', ondelete="CASCADE")),
#     sa.Column("status", sa.Integer, sa.ForeignKey('status.id', ondelete="CASCADE"), default=1),
#     sa.Column("update_time", sa.DateTime, default=datetime.utcnow)
# )


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.Text, unique=True)
    email = sa.Column(sa.Text, unique=True)
    password = sa.Column(sa.Text)
    # words = db.relationship('Word', secondary=user_has_word_table, backref='user')



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
    # user = db.relationship('User', secondary=user_has_word_table, backref='word')


class Status(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.Integer, unique=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False)


class Association(db.Model):
    # __tablename__ = 'association'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status', backref=db.backref('associations', lazy='dynamic'))

# class User_Has_Word(db.Model):
#     id = sa.Column(sa.BigInteger, primary_key=True)
#     user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
#     word_id = sa.Column(sa.Integer, sa.ForeignKey("word.id", ondelete='CASCADE'), nullable=False)
#     status_id = sa.Column(sa.Integer, sa.ForeignKey("status.id", ondelete='CASCADE'), nullable=False)
#     status = db.relationship("Status", backref='status', lazy=True)
#     update_time = sa.Column(sa.DateTime, default=datetime.utcnow)
