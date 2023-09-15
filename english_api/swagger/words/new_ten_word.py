new_ten_words = {
    "tags": ["Words"],
    "summary": "Get ten new words for study",
    "description": "Get ten new words for study",
    "parameters": [
        {
            "name": "auth_token",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "Auth token"
        }
    ],
    "responses": {
        "200": {
            "description": "OK",
            "schema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "word_id": {
                                    "type": "integer",
                                    "description": "Word id",
                                    "example": 1
                                },
                                "wordEn": {
                                    "type": "string",
                                    "description": "Word in english",
                                    "example": "Hello"
                                }
                            }
                        }
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
                        "description": "Status",
                        "example": "FAILURE"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description",
                        "example": "Not found auth_token in headers"
                    },
                    "data": {
                        "type": "object",
                        "properties": {}
                    },
                    "status_code": {
                        "type": "integer",
                        "description": "Status code",
                        "example": 5
                    }
                }
            }
        }
    }
}