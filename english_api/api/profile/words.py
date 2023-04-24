from flask import request

from english_api.api import api
from english_api.models.models import User, UserWordStatus, Word
from english_api.utils import auth_check, create_res_obj


@api.post("/words")
def get_words():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 400
    words = UserWordStatus.query.filter_by(user_id=request.headers.get("auth_token"))\
        .filter(UserWordStatus.status_id != 4).all()
    if not words:
        return "not"
    res = [{
        "word_id": i.word_id,
        "word": Word.query.filter_by(id=i.word_id).first().word_en,
        "status": i.status_id}
        for i in words]
    # TODO продумать при окончании слов о переходе на следующий уровень
    return create_res_obj(data=res), 200


@api.post("/word/<int:id>")
def get_word():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers", status_code=5), 400
