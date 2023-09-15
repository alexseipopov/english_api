studied_words = {
    "tags": ["Words"],
    "summary": "Get studied words",
    "description": "Get studied words",
    "parameters": [
        {
            "in": "header",
            "name": "auth_token",
            "type": "string",
            "required": True
        },
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
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "word_id": {
                                    "type": "integer",
                                    "example": 1
                                },
                                "word_en": {
                                    "type": "string",
                                    "example": "Hello"
                                },
                                "status": {
                                    "type": "integer",
                                    "example": 1
                                }
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
        "403": {
            "description": "Forbidden",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["OK", "FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "example": "Not found auth_token in headers"
                    },
                    "data": {
                        "type": "object",
                        "properties": {}
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 5
                    }
                }
            }
        }
    },
}
