# todo method


todo_post = {
    "summary": "POST todo",
    "consumes": "application/json",
    "parameters": [
        {
            "name": "ReqSend",
            "in": "body",
            "description": "register todo",
            "schema": {
                "$ref": "#/definitions/task"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "OK"
        }
    },
    "tags":[
        "todo"
    ],
    "definitions":{
        "task": {
            "type": "object",
            "required": [
                "task"
            ],
            "properties": {
                "task": {
                    "type": "string",
                }
            }
        }
    }
}


todo_get = {
    "summary": "GET todo list",
    "consumes": "applicatin/json",
    "parameters": [
        {
            "name": "todo_id",
            "in": "query",
            "description": "todo_id",
            "type": "string"
        }
    ],
    "responses": {
        "200": {
            "description":"OK",
            "schema": {
                "$ref":"#/definitions/doto_list"
            }
        }
    },
    "tags": [
        "todo"
    ],
    "definitions": {
        "doto_list": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                },
                "todo":{
                    "type": "string",
                }
            }
        }
    }
}