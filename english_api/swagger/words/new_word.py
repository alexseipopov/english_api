new_word = {
    "tags": ["Words"],
    "summary": "Get new word for study",
    "description": "Get new word for study",
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
            "schema": {
                "type": "object",
                "properties": {
                    "word_id": {
                        "type": "integer",
                        "example": 1
                    },
                    "status": {
                        "type": "integer",
                        "example": 1
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
                        "example": "Word was added to study"
                    },
                    "status_code": {
                        "type": "integer",
                        "example": 1
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "example": 1
                            },
                            "word_en": {
                                "type": "string",
                                "example": "Hello"
                            },
                            "word_ru": {
                                "type": "string",
                                "example": "Привет"
                            },
                            "transcription": {
                                "type": "string",
                                "example": "həˈləʊ"
                            },
                            "group_id": {
                                "type": "integer",
                                "example": 1
                            },
                            "example_en": {
                                "type": "string",
                                "example": "Hello, my name is ..."
                            },
                            "example_ru": {
                                "type": "string",
                                "example": "Привет, меня зовут ..."
                            },
                            "image_path": {
                                "type": "string",
                                "example": "hello.jpg"
                            },
                            "audio_path": {
                                "type": "string",
                                "example": "hello.mp3"
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
