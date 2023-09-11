from flasgger import swag_from
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash

from english_api import db
from english_api.api import api
from english_api.models.models import Group, Status, User, UserWordStatus, Word
from english_api.models.serializer import UserSchema
from english_api.swagger import (auth, change_password, check_auth, delete,
                                 recovery_password, register)
from english_api.utils import auth_check, create_res_obj


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
@swag_from(register)
def register():
    phone = request.json.get("phone")
    password = request.json.get("password")
    email = request.json.get("email")
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
@swag_from(auth)
def auth():
    phone = request.json.get("phone")
    email = request.json.get("email")
    password = request.json.get("password")
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


@api.post("/change_password")
@swag_from(change_password)
def change_password():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")
    user = User.query.filter_by(id=request.headers.get("auth_token")).first()
    if not user or not check_password_hash(user.password, password=old_password):
        return create_res_obj(status="FAILURE", description="User or password is incorrect", status_code=4), 400
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return create_res_obj(status="SUCCESS", description="Password changed"), 200


@api.delete("/delete_user")
@swag_from(delete)
def delete_user():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    user = User.query.filter_by(id=request.headers.get("auth_token")).first()
    if not user:
        return create_res_obj(status="FAILURE", description="User not found", status_code=6), 400
    db.session.delete(user)
    db.session.commit()
    return create_res_obj(status="SUCCESS", description="User deleted"), 200


@api.get("/check_auth")
@swag_from(check_auth)
def check_auth():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    token = request.headers.get("auth_token")
    user = User.query.filter_by(id=token).first()
    if not user:
        return create_res_obj(status="FAILURE", description="User not found", status_code=6), 400
    data = {
        "phone": user.phone,
        "email": user.email
    }
    return create_res_obj(status="SUCCESS", description="User is authorized", data=data), 200


@api.get("/recovery_password")
@swag_from(recovery_password)
def recovery_password():
    email = request.args.get("email")
    if not email:
        return create_res_obj(status="FAILURE", description="Not found email in args", status_code=7), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return create_res_obj(status="FAILURE", description="User not found", status_code=6), 400
    # TODO тут будет логика восстановления пароля
    return create_res_obj(status="SUCCESS", description="Password recovery (mock)"), 200
