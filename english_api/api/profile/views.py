from flask import request, jsonify

from english_api import db,swagger
from english_api.models.models import Word

from .. import api
from .utils import *

@swag_from
@api.get("/words")
def get_all_words():
    """
    First try to generate automatic API doc
    ---
    responses:
        200:
            desrciption: Some text
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
    """
    words = SerializeTable(Word).all_data()
    return create_res_obj(data=words)


# @api.post("/user")
# def insert_new_user():
#     user = User(phone=request.form.get("phone"), email=request.form.get("email"))
#     db.session.add(user)
#     db.session.commit()
#     return "OK"
