import copy


base = {
    "summary": "base",
    "parameters": [
        { "$ref": "#/components/parameters/TokenParam" }
    ],
    "responses": {
        "200": {
            "description": "Ok",
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
        "comments"
    ],
    "definitions": {
        "ResponseCommentInfo": {
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
                        "user_id": {
                            "type": "integer"
                        },
                        "writer": {
                            "type": "string"
                        },
                        "create_at": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}


comment_paging = copy.deepcopy(base)
comment_paging["summary"] = "GET board comment with page"
comment_paging["parameters"].append(
    {
        "name": "num",
        "in": "query",
        "required": True,
        "description": "Number of paging",
        "type": "integer"
    }
)
comment_paging["parameters"].append(
    {
        "name": "limit",
        "in": "query",
        "required": True,
        "description": "Limit of paging",
        "type": "integer"
    }
)
comment_paging["parameters"].append(
    {
        "name": "board id",
        "in": "query",
        "required": True,
        "description": "board id(pk)",
        "type": "integer"
    }
)
comment_paging["responses"]["200"].clear()
comment_paging["responses"]["200"] =\
    {
        "description": "Ok",
        "schema": {
            "$ref": "#/definitions/ResponseCommentInfo"
        }
    }
