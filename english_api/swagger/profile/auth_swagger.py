register = {
    "tags": ["Profile"],
    "summary": "Регистрация пользователя",
    "description": "Регистрация пользователя",
    "parameters": [
        {
            "name": "data",
            "in": "body",
            "description": "Отправляется набор параметров из phone или email и password",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string",
                        "example": "79999999999"
                    },
                    "email": {
                        "type": "string",
                        "example": "test#example.com"
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
                        "enum": ["OK", "FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "example": "OK"
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
                                "example": "79999999999"
                            },
                            "email": {
                                "type": "string",
                                "example": "test@test.com"
                            }
                        }
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 0
                    }
                }
            }
        },
        "400": {
            "description": "Not enough parameters: phone/email or password",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "example": "Not enough parameters: phone/email or password"
                    },
                    "data": {
                        "type": "object",
                        "properties": {}
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 3
                    }
                }
            }
        }
    }
}
