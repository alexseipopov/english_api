from flask import request

from english_api import db
from english_api.api import api
from english_api.models.models import User, UserWordStatus, Word
from english_api.utils import auth_check, create_res_obj
from english_api.models.serializer import WordSchema


@api.post("/words")
def get_words():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    user_id = request.headers.get("auth_token")
    words = db.session.query(UserWordStatus.word_id, db.func.max(UserWordStatus.status_id))\
        .group_by(UserWordStatus.word_id)\
        .filter(UserWordStatus.status_id != 8, UserWordStatus.user_id == user_id).limit(10).all()
    if not words:
        return "not"
    # TODO продумать при окончании слов о переходе на следующий уровень
    res = [{
        "word_id": i[0],
        "word": Word.query.filter_by(id=i[0]).first().word_en,
        "status": i[1]}
        for i in words]
    return create_res_obj(data=res), 200


@api.post("/word/")
def get_word():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    word_id = int(request.form.get("word_id"))
    status_id = int(request.form.get("status"))
    if not word_id or not status_id:
        return create_res_obj(status="FAILURE", description="No such param in body of request", status_code=3), 400
    if status_id == 1:
        pass
        # TODO надо поменять статус с НЕ ОТКРЫВАЛ на ОТКРЫЛ (1 -> 2)
    if status_id == 2:
        pass
        # TODO если слово было открыто то ждем пока пользователь ответит, знает он слово или нет. Значит отправить надо все данные для слова
    return create_res_obj(data={"target": request.form.get("word_id")}), 200


@api.post("/new_word")
def get_new_word():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 403
    user_id = request.headers.get("auth_token")
    status = request.form.get("status")
    if not status:
        return create_res_obj(status="FAILURE", description="No such status of word", status_code=3), 400
    word_id = request.form.get("word_id")
    if not word_id:
        return create_res_obj(status="FAILURE", description="No such word_id of word", status_code=3), 400
    row = UserWordStatus.query.filter_by(word_id=word_id, status_id=status, user_id=user_id).first()
    if row.status_id == 1:
        # TODO не правим текущий, а создаем новую запись
        row.status_id = 2
        db.session.commit()
    word = Word.query.filter_by(id=row.word_id).first()
    word_schema = WordSchema()
    result = word_schema.dump(word)
    return create_res_obj(data=result), 200
