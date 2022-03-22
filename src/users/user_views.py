user_get = {
    "summary": "GET user info",
    "consumes": "applicatin/json",
    "responses": {
        "200": {
            "description":"OK",
            "schema": {
                "$ref":"#/components/schemas/DefaultResponse"
            }
        }
    },
    "tags": [
        "user"
    ]    
}