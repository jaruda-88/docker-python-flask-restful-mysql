from re import M


board_post = {
    "summary": "POST board writer",
    "consumes": "application/json",
    "parameters": [
        { "$ref": "#/components/parameters/TokenParam" },
        {
            "name": "writer",
            "in": "body",
            "description": "register board content",
            "schema": {
                "$ref": "#/definitions/WritingInfo"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "OK",
            "schema": {
                "$ref": "#/components/schemas/DefaultResponse"
            }
        },
        "500": {
            "description": "Errors",
            "schema": {
                "$ref": "#/components/schemas/DefaultResponse"
            }
        }
    },
    "tags": [
        "board"
    ],
    "definitions": {
        "WritingInfo": {
            "type": "object",
            "required": [
                "writer", "content"
            ],
            "properties": {
                "writer": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                }
            }
        }
    }
}


board_get = {
    "summary": "GET board list",
    "consumes": "application/json",
    "parameters": [
        { "$ref" : "#/components/parameters/TokenParam" }
    ],
    "responses": {
        "200": {
            "description": "OK",
            "schema": {
                "$ref": "#/definitions/BoardResponse"
            }
        },
        "500": {
            "description": "Errors",
            "schema": {
                "$ref": "#/components/schemas/DefaultResponse"
            }
        }
    },
    "tags": [
        "board"
    ],
    "definitions": {
        "BoardResponse": {
            "type": "object",
            "properties": {
                "resultCode": {
                    "type": "integer"
                },
                "resultMsg": {
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "writer": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        },
                        "update_at": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}

board_delete = {
    "summary": "DELETE board row",
    "consumes": "application/json",
    "parameters": [
        { "$ref": "#/components/parameters/TokenParam" },
        {
            "name": "board_id",
            "in": "query",
            "description": "pk",
            "type": "integer"
        }
    ],
    "tags": [
        "board"
    ],
    "responses": {
        "200": {
            "description": "OK",
            "schema": {
                "$ref": "#/definitions/BoardResponse"
            }
        },
        "500": {
            "description": "Errors",
            "schema": {
                "$ref": "#/definitions/BoardResponse"
            }
        }
    }
}