user_get = {
    "summary": "GET user info",
    "consumes": "applicatin/json",
    "parameters": [
        { "$ref": "#/components/parameters/TokenParam" }
    ],
    "responses": {
        "200": {
            "description":"OK",
            "schema": {
                "$ref":"#/components/schemas/DefaultResponse"
            }
        },
        "500": {
            "description":"Errors",
            "schema": {
                "$ref":"#/components/schemas/DefaultResponse"
            }
        }
    },
    "tags": [
        "user"
    ]
}


user_post = {
    "summary": "POST registration user",
    "consumes": "application/json",
    "parameters": [
        {
            "name": "registration request",
            "in": "body",
            "description": "user info",
            "schema": {
                "$ref": "#/definitions/UserRegistrationInfo"
            }
        }
    ],
    "responses": {
        "200": {
            "description":"OK",
            "schema": {
                "$ref":"#/components/schemas/DefaultResponse"
            }
        },
        "500": {
            "description":"Errors",
            "schema": {
                "$ref":"#/components/schemas/DefaultResponse"
            }
        }
    },
    "tags": [
        "user"
    ],
    "definitions": {
        "UserRegistrationInfo": {
            "type": "object",
            "required": [
                "userid", "pw"
            ],
            "properties": {
                "userid": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                },
                "pw": {
                    "type": "string"
                }
            }
        }
    }
}