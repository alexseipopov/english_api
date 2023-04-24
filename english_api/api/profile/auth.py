from flask import request
from werkzeug.security import check_password_hash, generate_password_hash

from english_api import db
from english_api.api import api
from english_api.models.models import Group, Status, User, UserWordStatus, Word
from english_api.models.serializer import UserSchema
from english_api.utils import create_res_obj


def insert_new_user(user_id):
    if not UserWordStatus.query.filter_by(user_id=user_id).first():
        group = Group.query.order_by(Group.level).first()
        words = Word.query.filter_by(group_id=group.id).all()
        status = Status.query.order_by(Status.number).first()
        for word in words:
            new_record = UserWordStatus(user_id=user_id, word_id=word.id, status_id=status.id)
            db.session.add(new_record)
        db.session.commit()


@api.post("/register")
def register():
    """Принимаем что придет телефон в формате 7ХХХХХХХХХХ"""
    phone = request.form.get("phone")
    password = request.form.get("password")
    email = request.form.get("email")
    if (not phone or not password) and (not email or not password):
        return create_res_obj(status="FAILURE", description="Not enough parameters: phone/email or password",
                              status_code=3), 400
    if phone is not None:
        check_user_phone = User.query.filter_by(phone=phone).first()
        if check_user_phone:
            return create_res_obj(status="FAILURE", description=f"User with phone {phone} already exist",
                                  status_code=1), 400

    if email is not None:
        check_user_email = User.query.filter_by(email=email).first()
        if check_user_email:
            return create_res_obj(status="FAILURE", description=f"User with email {email} already exist",
                                  status_code=2), 400
    password = generate_password_hash(password)
    user = User(phone=phone, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    user_schema = UserSchema(exclude=["password"])
    result = user_schema.dump(user)
    insert_new_user(result["id"])
    return create_res_obj(data=result), 200


@api.post("/auth")
def auth():
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")
    if (not phone or not password) and (not email or not password):
        return create_res_obj(status="FAILURE", description="No such parameters: phone/email or password", status_code=3), 400
    user = User.query.filter_by(phone=phone).first()
    if not user:
        user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password=password):
        return create_res_obj(status="FAILURE", description="User or password is incorrect", status_code=4), 400

    user_schema = UserSchema(exclude=["password"])
    data = user_schema.dump(user)
    print(data)
    data.setdefault("auth_token", user.id)
    return create_res_obj(data=data), 200
