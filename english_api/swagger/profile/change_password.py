change_password = {
    "tags": ["Profile"],
    "summary": "Change password",
    "description": "Change password",
    "parameters": [
        {
            "name": "auth_token",
            "in": "header",
            "type": "string",
            "required": True
        },
        {
            "name": "data",
            "in": "body",
            "type": "object",
            "required": True,
            "properties": {
                "old_password": {
                    "type": "string",
                    "example": "123456"
                },
                "new_password": {
                    "type": "string",
                    "example": "1234567"
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Password changed",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["SUCCESS"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["Password changed"]
                    }
                }
            }
        },
        "400": {
            "description": "User or password is incorrect",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["User or password is incorrect"]
                    }
                }
            }
        },
        "403": {
            "description": "Not found auth_token in headers",
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
                    }
                }
            }
        }
    }
}
