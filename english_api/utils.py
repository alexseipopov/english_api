def create_res_obj(status="OK", description="OK", data=dict()):
    return {
        "status": status,
        "description": description,
        "data": data
    }
