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
        }
    },
    "tags": [
        "user"
    ]
}