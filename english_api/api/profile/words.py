import logging
import random

from flasgger import swag_from
from flask import Response, abort, jsonify, make_response, request, url_for
from sqlalchemy import and_, func

from english_api import db
from english_api.api import api
from english_api.models.models import User, UserWordStatus, Word
from english_api.models.serializer import WordSchema
from english_api.swagger import know_this_word, new_word, study_words, studied_words
from english_api.utils import auth_check, create_res_obj


@api.get("/study_words")
@swag_from(study_words)
def get_words():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    user_id = request.headers.get("auth_token")
    subquery = db.session.query(UserWordStatus.user_id, UserWordStatus.word_id,
                                func.max(UserWordStatus.status_id).label("m")) \
        .group_by(UserWordStatus.word_id, UserWordStatus.user_id) \
        .subquery()
    words = db.session.query(subquery.c.user_id, subquery.c.word_id, subquery.c.m) \
        .filter(subquery.c.m != 8, subquery.c.user_id == user_id, subquery.c.m > 1) \
        .all()
    if not words:
        return create_res_obj(status="OK", description="No words for this user", status_code=6), 200
    res = [{
        "word_id": i[1],
        "word_en": Word.query.filter_by(id=i[1]).first().word_en,
        "status": i[2]}
        for i in words]
    return create_res_obj(data=res), 200


@api.get("/studied_words")
@swag_from(studied_words)
def get_studied_words():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    user_id = request.headers.get("auth_token")
    subquery = db.session.query(UserWordStatus.user_id, UserWordStatus.word_id,
                                func.max(UserWordStatus.status_id).label("m")) \
        .group_by(UserWordStatus.word_id, UserWordStatus.user_id) \
        .subquery()
    words = db.session.query(subquery.c.user_id, subquery.c.word_id, subquery.c.m) \
        .filter(subquery.c.m == 8, subquery.c.user_id == user_id) \
        .all()
    if not words:
        return create_res_obj(status="OK", description="No words for this user", status_code=6), 200
    res = [{
        "word_id": i[1],
        "word_en": Word.query.filter_by(id=i[1]).first().word_en,
        "status": i[2]}
        for i in words]
    return create_res_obj(data=res), 200


@api.get("/new_ten_words")
def get_new_ten_words():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    user_id = request.headers.get("auth_token")
    subquery = db.session.query(UserWordStatus.user_id, UserWordStatus.word_id,
                                func.max(UserWordStatus.status_id).label("m")) \
        .group_by(UserWordStatus.word_id, UserWordStatus.user_id) \
        .subquery()
    words = db.session.query(subquery.c.user_id, subquery.c.word_id, subquery.c.m) \
        .filter(subquery.c.m == 1, subquery.c.user_id == user_id) \
        .order_by(func.random()) \
        .limit(10) \
        .all()
    if not words:
        return create_res_obj(status="OK", description="No words for this user", status_code=6), 200
    res = [{
        "word_id": i[1],
        "wordEn": Word.query.filter_by(id=i[1]).first().word_en,
        "status": i[2]}
        for i in words]
    return create_res_obj(data=res), 200


def check_request(req):
    logging.debug(f"req: {req.json}")
    if not auth_check(req):
        logging.error("Not found auth_token in headers")
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="Not found auth_token in headers",
                                                     status_code=5)), 403))
    status = req.json.get("status")
    logging.debug(f"status: {status}")
    user_id = request.headers.get("auth_token")
    logging.debug(f"user_id: {user_id}")
    if not status:
        logging.error("No such status of word")
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="No such status of word",
                                                     status_code=3)), 400))
    word_id = req.json.get("word_id")
    logging.debug(f"word_id: {word_id}")
    if not word_id:
        logging.error("No such word_id of word")
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="No such word_id of word",
                                                     status_code=3)), 400))
    return word_id, user_id, status


@api.post("/new_word")
@swag_from(new_word)
def get_new_word():
    logging.info("Try to get new word")
    word_id, user_id, status = check_request(request)
    user_id = int(user_id)
    logging.debug(f"word_id: {word_id}, user_id: {user_id}, status: {status}; types: {type(word_id)}, {type(user_id)}, {type(status)}")
    logging.info(f"word_id: {word_id}, user_id: {user_id}, status: {status}; types: {type(word_id)}, {type(user_id)}, {type(status)}")
    row = UserWordStatus.query.filter_by(word_id=word_id, status_id=status, user_id=user_id).first()
    word = Word.query.filter_by(id=row.word_id).first()
    word_schema = WordSchema()
    result = word_schema.dump(word)
    result["audio_path"] = url_for("static", filename="materials/" + result["audio_path"])
    result["image_path"] = url_for("static", filename="materials/" + result["image_path"])
    logging.info("New word was sent")
    return create_res_obj(data=result), 200


@api.post("/know_this_word")
@swag_from(know_this_word)
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
