import copy


base = {
    "consumes": "application/json",
    "parameters": [
        { "$ref": "#/components/parameters/TokenParam" }
    ],
    "responses":{
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
    "tags":[
        "boards"
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
        },
        "ResponseBoardInfo": {
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
                        "create_at": {
                            "type": "string"
                        },
                        "update_at": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "BoardEditInfo": {
            "type": "object",
            "required": [
                "writer", "id"
            ],
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
            }
        }
    }
}


# 글 작성 
writing = copy.deepcopy(base)
writing["summary"] = "POST board writer"
writing["parameters"].append(
    {
        "name": "writer",
        "in": "body",
        "description": "register board content",
        "schema": {
            "$ref": "#/definitions/WritingInfo"
        }
    }
)


# 글 수정 
edit = copy.deepcopy(base)
edit["summary"] = "PUT edit"
edit["parameters"].append(
    {
        "name": "edit",
        "in": "body",
        "description": "modify written",
        "schema": {
            "$ref": "#/definitions/BoardEditInfo"
        }
    }
)


# 글 삭제
delete_post = copy.deepcopy(base)
delete_post["summary"] = "DELETE board row"
delete_post["parameters"].append(
    {
        "name": "id",
        "in": "path",
        "required" : True,
        "description": "board id(pk)",
        "type": "integer"
    }
)


# 작성한 목록
written_list = copy.deepcopy(base)
written_list["summary"] = "Get boardinfos"
written_list["responses"]["200"].clear()
written_list["responses"]["200"] =\
    {
        "description": "Ok",
        "schema": {
            "$ref": "#/definitions/ResponseBoardInfo"
        }
    }