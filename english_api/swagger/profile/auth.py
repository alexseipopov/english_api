auth = {
    "tags": ["Profile"],
    "summary": "Auth",
    "description": "Auth user",
    "parameters": [
        {
            "in": "body",
            "name": "data",
            "required": True,
            "type": "object",
            "schema": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string",
                        "example": "+79999999999"
                    },
                    "email": {
                        "type": "string",
                        "example": "test@example.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "123456"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "OK",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "OK"
                    },
                    "description": {
                        "type": "string",
                        "example": "User was authorized"
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 0
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "example": 1
                            },
                            "phone": {
                                "type": "string",
                                "example": "+79999999999"
                            },
                            "email": {
                                "type": "string",
                                "example": "example@test.com"
                            },
                            "auth_token": {
                                "type": "string",
                                "example": "1"
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Bad request",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "FAILURE"
                    },
                    "description": {
                        "type": "string",
                        "example": "User or password is incorrect"
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 4
                    }
                }
            }
        }
    }
}
