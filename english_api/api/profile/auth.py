from flask import request
from werkzeug.security import check_password_hash, generate_password_hash

from english_api import db
from english_api.api import api
from english_api.models.models import User, UserWordStatus, Word
from english_api.models.serializer import UserSchema
from english_api.utils import create_res_obj


def insert_new_user(user_id):
    words = Word.query.filter_by(group_id=1).all()
    for word in words:
        line = UserWordStatus(user_id=user_id, word_id=word.id, status_id=1)
        db.session.add(line)
    db.session.commit()


@api.post("/register")
def register():
    """Принимаем что придет телефон в формате 7ХХХХХХХХХХ"""
    # TODO сделать валидацию на существование пришедшего телефона или почты
    # TODO сделать валидацию на прихоящие параметры (все ли необходимые есть)
    phone = request.form.get("phone")
    password = request.form.get("password")
    if not phone or not password:
        return create_res_obj(status="FAILURE", description="Not enough parameters: phone or password"), 400
    check_user = User.query.filter_by(phone=phone).first()
    if check_user:
        return create_res_obj(status="FAILURE", description=f"User with phone {phone} already exist"), 400
    password = generate_password_hash(password)
    user = User(phone=phone, password=password)
    db.session.add(user)
    db.session.commit()
    user_schema = UserSchema(exclude=["password"])
    result = user_schema.dump(user)
    insert_new_user(result["id"])
    return create_res_obj(data=result), 200


@api.post("/auth")
def auth():
    phone = request.form.get("phone")
    password = request.form.get("password")
    if not phone or not password:
        return create_res_obj(status="FAILURE", description="No such parameters: phone or password"), 400
    user = User.query.filter_by(phone=phone).first()

    if not user or not check_password_hash(user.password, password=password):
        return create_res_obj(status="FAILURE", description="User or password is incorrect"), 400

    user_schema = UserSchema(exclude=["password"])
    data = user_schema.dump(user)
    return create_res_obj(data=data), 200
