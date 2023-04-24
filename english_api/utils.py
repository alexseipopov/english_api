def create_res_obj(status="OK", description="OK", data=dict(), status_code=0):
    return {
        "status": status,
        "description": description,
        "data": data,
        "status_code": status_code
    }


def auth_check(request_data):
    auth_token = request_data.headers.get("auth_token")
    if not auth_token:
        return False
    return True
