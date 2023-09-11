know_this_word = {
    "tags": ["Words"],
    "summary": "Know this word",
    "description": "Know this word",
    "parameters": [
        {
            "in": "header",
            "name": "auth_token",
            "type": "string",
            "required": True
        },
        {
            "in": "body",
            "name": "data",
            "required": True,
            "type": "object",
            "schema": {
                "type": "object",
                "properties": {
                    "word_id": {
                        "type": "integer",
                        "example": 1
                    },
                    "status": {
                        "type": "integer",
                        "example": 2
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
                        "example": "Word status was changed"
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 0
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
                        "example": "No such status of word"
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 3
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
                        "example": "FAILURE"
                    },
                    "description": {
                        "type": "string",
                        "example": "Not found auth_token in headers"
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 5
                    }
                }
            }
        }
    }
}
