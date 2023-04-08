from flask import request
from werkzeug.security import check_password_hash, generate_password_hash

from english_api import db
from english_api.api import api
from english_api.models.models import User
from english_api.models.serializer import UserSchema
from english_api.utils import create_res_obj


@api.post("/register")
def register():
    """Принимаем что придет телефон в формате 7ХХХХХХХХХХ"""
    # TODO сделать валидацию на существование пришедшего телефона или почты
    # TODO сделать валидацию на прихоящие параметры (все ли необходимые есть)
    phone = request.form.get("phone")
    password = request.form.get("password")
    if not phone or not password:
        return create_res_obj(status="FAILURE", description="Not enought parameters: phone or password"), 400
    check_user = User.query.filter_by(phone=phone).first()
    if check_user:
        return create_res_obj(status="FAILURE", description=f"User with phone {phone} already exist"), 400
    password = generate_password_hash(password)
    user = User(phone=phone, password=password)
    db.session.add(user)
    db.session.commit()
    user_schema = UserSchema(exclude=["password"])
    result = user_schema.dump(user)
    return create_res_obj(data=result), 200


@api.post("/auth")
def auth():
    auth_token = request.headers.get("auth_token")
    if not auth_token:
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers"), 400
    auth_token = int(auth_token)
    phone = request.form.get("phone")
    password = request.form.get("password")
    if not phone or not password:
        return create_res_obj(status="FAILURE", description="No such parameters: phone or password"), 400
    user = User.query.filter_by(phone=phone).first()

    if not user or not check_password_hash(user.password, password=password):
        return create_res_obj(status="FAILURE", description="User or password is incorrect"), 400

    # TODO здесь будет проверка hash ключа
    if user.id != auth_token:
        return create_res_obj(status="FAILURE", description="Auth error. not found auth token in system"), 400

    user_schema = UserSchema(exclude=["password"])
    data = user_schema.dump(user)
    return create_res_obj(data=data), 200
