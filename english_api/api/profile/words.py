from flasgger import swag_from
from flask import abort, jsonify, make_response, request, url_for
from sqlalchemy import func

from english_api import db, logger
from english_api.api import api
from english_api.models.models import User, UserWordStatus, Word
from english_api.models.serializer import WordSchema
from english_api.swagger import (know_this_word, new_word, studied_words,
                                 study_words, success_answer, new_ten_words)
from english_api.utils import auth_check, create_res_obj

BASE_URL = "http://195.133.197.62:3015"

@api.get("/study_words")
@swag_from(study_words)
def get_words():
    logger.info("Get study words")
    if not auth_check(request):
        logger.info("Not found auth_token in headers")
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
        logger.info("No words for this user")
        return create_res_obj(status="OK", description="No words for this user", status_code=6), 200
    res = [{
        "word_id": i[1],
        "word_en": Word.query.filter_by(id=i[1]).first().word_en,
        "status_id": i[2]
    } for i in words]
    logger.info("Get study words success")
    return create_res_obj(data=res), 200


@api.get("/studied_words")
@swag_from(studied_words)
def get_studied_words():
    logger.info("Get studied words")
    if not auth_check(request):
        logger.info("Not found auth_token in headers")
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
        logger.info("No words for this user")
        return create_res_obj(status="OK", description="No words for this user", status_code=6), 200
    res = [{
        "word_id": i[1],
        "word_en": Word.query.filter_by(id=i[1]).first().word_en,
        "status_id": i[2]
    } for i in words]
    logger.info("Get studied words success")
    return create_res_obj(data=res), 200


@api.get("/new_ten_words")
@swag_from(new_ten_words)
def get_new_ten_words():
    logger.info("Get new ten words")
    if not auth_check(request):
        logger.info("Not found auth_token in headers")
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
        "wordEn": Word.query.filter_by(id=i[1]).first().word_en
    } for i in words]
    logger.info("Get new ten words success")
    return create_res_obj(data=res), 200


def check_request(req):
    logger.debug(f"req: {req.json}")
    if not auth_check(req):
        logger.error("Not found auth_token in headers")
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="Not found auth_token in headers",
                                                     status_code=5)), 403))
    user_id = request.headers.get("auth_token")
    logger.debug(f"user_id: {user_id}")
    word_id = req.json.get("word_id")
    logger.debug(f"word_id: {word_id}")
    if not word_id:
        logger.error("No such word_id of word")
        abort(make_response(jsonify(**create_res_obj(status="FAILURE", description="No such word_id of word",
                                                     status_code=3)), 400))
    return word_id, user_id


@api.post("/new_word")
@swag_from(new_word)
def get_new_word():
    logger.info("Try to get new word")
    word_id, user_id = check_request(request)
    user_id = int(user_id)
    logger.debug(f"word_id: {word_id}, user_id: {user_id}")
    logger.info(f"word_id: {word_id}, user_id: {user_id}")
    row = UserWordStatus.query.filter_by(word_id=word_id, user_id=user_id).first()
    word = Word.query.filter_by(id=row.word_id).first()
    word_schema = WordSchema()
    result = word_schema.dump(word)
    result["audio_path"] = BASE_URL + url_for("static", filename="materials/" + result["audio_path"])
    result["image_path"] = BASE_URL + url_for("static", filename="materials/" + result["image_path"])
    row.status_id = 2
    db.session.commit()
    logger.info("Change status of word to 2")
    logger.info("New word was sent")
    return create_res_obj(data=result), 200


@api.post("/know_this_word")
@swag_from(know_this_word)
def know_this_word():
    logger.info("Try to know this word")
    word_id, user_id = check_request(request)
    row = UserWordStatus.query.filter_by(word_id=word_id, user_id=user_id).first()
    row.status_id = 8
    db.session.commit()
    logger.info("Change status of word to 8")
    return create_res_obj(), 200


@api.post("/success_answer")
@swag_from(success_answer)
def success_answer():
    logger.info("Try to success answer")
    word_id, user_id = check_request(request)
    row = UserWordStatus.query.filter_by(word_id=word_id, user_id=user_id).first()
    row.status_id += 1
    db.session.commit()
    logger.info(f"Change status of word to {row.status_id}")
    return create_res_obj(data={"new_status": row.status_id}, description="Successful update status"), 200
