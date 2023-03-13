import sqlalchemy as sa
from .. import app, db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    phone = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
