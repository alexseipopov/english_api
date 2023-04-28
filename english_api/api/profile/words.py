import random

from flask import request, abort, Response, jsonify, make_response
from sqlalchemy import func

from english_api import db
from english_api.api import api
from english_api.models.models import UserWordStatus, Word, User
from english_api.models.serializer import WordSchema
from english_api.utils import auth_check, create_res_obj


@api.post("/words")
def get_words():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    user_id = request.headers.get("auth_token")
    subquery = db.session.query(UserWordStatus.user_id, UserWordStatus.word_id,
                                func.max(UserWordStatus.status_id).label("m"))\
        .group_by(UserWordStatus.word_id, UserWordStatus.user_id)\
        .subquery()
    words = db.session.query(subquery.c.user_id, subquery.c.word_id, subquery.c.m)\
        .filter(subquery.c.m != 8, subquery.c.user_id == user_id)\
        .limit(10).all()
    if not words:
        return "not"
    # TODO продумать при окончании слов о переходе на следующий уровень
    res = [{
        "word_id": i[1],
        "word": Word.query.filter_by(id=i[0]).first().word_en,
        "status": i[2]}
        for i in words]
    return create_res_obj(data=res), 200


def check_request(req):
    if not auth_check(req):
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="Not found auth_token in headers",
                                                     status_code=5)), 403))
    status = req.form.get("status")
    user_id = request.headers.get("auth_token")
    if not status:
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="No such status of word",
                                                     status_code=3)), 400))
    word_id = req.form.get("word_id")
    if not word_id:
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="No such word_id of word",
                                                     status_code=3)), 400))
    return word_id, user_id, status


@api.post("/new_word")
def get_new_word():
    word_id, user_id, status = check_request(request)
    row = UserWordStatus.query.filter_by(word_id=word_id, status_id=status, user_id=user_id).first()
    word = Word.query.filter_by(id=row.word_id).first()
    word_schema = WordSchema()
    result = word_schema.dump(word)
    return create_res_obj(data=result), 200


@api.post("/know_this_word")
def know_this_word():
    word_id, user_id, status = check_request(request)
    new_row = UserWordStatus(word_id=word_id, user_id=user_id, status_id=8)
    db.session.add(new_row)
    db.session.commit()
    return create_res_obj(), 200


@api.post("/option_1")
def option_1():
    word_id, user_id, status = check_request(request)
    this_word = Word.query.filter_by(id=word_id).first()
    user = User.query.filter_by(id=user_id).first()
    all_words = Word.query.filter_by(group_id=user.level).all()
    random_choice = [this_word.word_ru]
    while len(random_choice) < 4:
        random_option = random.choice(all_words)
        if random_option not in random_choice:
            random_choice.append(random_option.word_ru)
    response = {
        "word": this_word.word_en,
        "options": random_choice,
        "answer": this_word.word_ru,
        "audio": this_word.audio_path
    }
    return create_res_obj(data=response, status_code=0), 200


@api.post("/option_2")
def option_2():
    word_id, user_id, status = check_request(request)
    this_word = Word.query.filter_by(id=word_id).first()
    user = User.query.filter_by(id=user_id).first()
    all_words = Word.query.filter_by(group_id=user.level).all()
    random_choice = [this_word.word_ru]
    while len(random_choice) < 4:
        random_option = random.choice(all_words)
        if random_option not in random_choice:
            random_choice.append(random_option.word_ru)
    response = {
        "options": random_choice,
        "answer": this_word.word_ru,
        "audio": this_word.audio_path
    }
    return create_res_obj(data=response, status_code=0), 200


@api.post("/option_3")
def option_3():
    word_id, user_id, status = check_request(request)
    this_word = Word.query.filter_by(id=word_id).first()
    user = User.query.filter_by(id=user_id).first()
    all_words = Word.query.filter_by(group_id=user.level).all()
    random_choice = [this_word.word_en]
    while len(random_choice) < 4:
        random_option = random.choice(all_words)
        if random_option not in random_choice:
            random_choice.append(random_option.word_en)
    response = {
        "options": random_choice,
        "answer": this_word.word_en,
        "image": this_word.image_path
    }
    return create_res_obj(data=response, status_code=0), 200


@api.post("/option_4")
def option_4():
    word_id, user_id, status = check_request(request)
    this_word = Word.query.filter_by(id=word_id).first()
    user = User.query.filter_by(id=user_id).first()
    all_words = Word.query.filter_by(group_id=user.level).all()
    random_choice = [this_word.word_en]
    while len(random_choice) < 4:
        random_option = random.choice(all_words)
        if random_option not in random_choice:
            random_choice.append(random_option.word_en)
    response = {
        "options": random_choice,
        "answer": this_word.word_en,
        "word": this_word.word_ru
    }
    return create_res_obj(data=response, status_code=0), 200


@api.post("/success_answer")
def success_answer():
    word_id, user_id, status = check_request(request)
    row = UserWordStatus(user_id=user_id, word_id=word_id, status_id=int(status) + 1)
    db.session.add(row)
    db.session.commit()
    return create_res_obj(data={"new_status": row.status_id}, description="Successful update status"), 200
