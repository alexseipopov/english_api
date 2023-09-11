recovery_password = {
    "tags": ["Profile"],
    "summary": "Recovery password",
    "description": "Recovery password",
    "parameters": [
        {
            "name": "email",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "Email"
        }
    ],
    "responses": {
        "200": {
            "description": "Success",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["SUCCESS"]
                    },
                    "description": {
                        "type": "string"
                    }
                }
            }
        },
        "400": {
            "description": "Failure",
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["FAILURE"]
                    },
                    "description": {
                        "type": "string"
                    }
                }
            }
        }
    }
}
