delete = {
    "tags": ["Profile"],
    "summary": "Delete user",
    "description": "Delete user",
    "parameters": [
        {
            "name": "auth_token",
            "in": "header",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "User deleted",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["SUCCESS"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["User deleted"]
                    },
                    "status_code": {
                        "type": "integer",
                        "enum": [0]
                    }
                }
            }
        },
        "400": {
            "description": "User not found",
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
                        "enum": [6]
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
                    },
                    "status_code": {
                        "type": "integer",
                        "enum": [5]
                    }
                }
            }
        }
    }
}
