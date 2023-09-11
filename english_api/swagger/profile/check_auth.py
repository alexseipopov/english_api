check_auth = {
    "tags": ["Profile"],
    "summary": "Check auth",
    "description": "Check auth",
    "parameters": [
        {
            "in": "header",
            "name": "auth_token",
            "type": "string",
            "required": True
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
                        "enum": ["SUCCESS", "FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["User or password is incorrect", "Not found auth_token in headers", "User not found"]
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "phone": {
                                "type": "string",
                                "pattern": "^[0-9]{11}$"
                            },
                            "email": {
                                "type": "string",
                                "example": "test@example.com"
                            }
                        }
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 1
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["Not found auth_token in headers"]
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 5
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
                        "enum": ["FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["User not found"]
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 6
                    }
                }
            }
        }
    }
}
