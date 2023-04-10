from flask import request
from english_api.api import api
from english_api.utils import auth_check, create_res_obj

@api.post("/word/<int:id>")
def get_word():
    if not auth_check(request):
        return create_res_obj(status="FAILURE", description="Not found auth_token in headers"), 400
    