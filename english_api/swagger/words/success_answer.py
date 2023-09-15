success_answer = {
    "tags": ["Words"],
    "summary": "Success answer",
    "description": "Change status of word to +1",
    "parameters": [
        {
            "name": "auth_token",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "auth_token of user"
        },
        {
            "name": "data",
            "in": "body",
            "type": "object",
            "required": True,
            "properties": {
                "word_id": {
                    "type": "integer",
                    "example": "1"
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful update status",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["OK"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["Successful update status"]
                    },
                    "data": {
                        "type": "object",
                        "properties": {}
                    },
                    "status_code": {
                        "type": "integer",
                        "enum": [0]
                    }
                }
            }
        },
        "400": {
            "description": "No such word_id of word",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["FAILURE"]
                    },
                    "description": {
                        "type": "string",
                        "enum": ["No such word_id of word"]
                    },
                    "data": {
                        "type": "object",
                        "properties": {}
                    },
                    "status_code": {
                        "type": "integer",
                        "enum": [3]
                    },
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
                    "data": {
                        "type": "object",
                        "properties": {}
                    },
                    "status_code": {
                        "type": "integer",
                        "enum": [5]
                    },
                }
            }
        }
    }
}
