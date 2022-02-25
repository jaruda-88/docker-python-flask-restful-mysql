# todo method


todo_post = {

}


todo_get = {
    "summary": "Get todo list",
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