import copy

# 게시판 공통 dto
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
                "title": {
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
                        "count": {
                            "type": "integer"
                        },
                        "list": {
                            "properties": {
                                "id": {
                                    "type": "integer"
                                },
                                "writer": {
                                    "type": "string"
                                },
                                "title": {
                                    "type": "string"
                                },
                                "update_at": {
                                    "type": "string"
                                }
                            }
                        },
                    }
                }
            }
        },
        "ResponseBoardDetailInfo": {
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
                        "title": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        },
                        "create_at":{
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
                "title": {
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
written_list["summary"] = "GET boardinfos"
written_list["responses"]["200"].clear()
written_list["responses"]["200"] =\
    {
        "description": "Ok",
        "schema": {
            "$ref": "#/definitions/ResponseBoardInfo"
        }
    }


# 게시글 목록
written_all_list = copy.deepcopy(written_list)
written_all_list["summary"] = "GET boardinfos in id"
written_all_list["parameters"].append(
    {
        "name": "id",
        "in": "path",
        "required": True,
        "description": "board id(pk), -1(all)",
        "type": "integer"
    }
)
written_list["responses"]["200"].clear()
written_list["responses"]["200"] =\
    {
        "description": "Ok",
        "schema": {
            "$ref": "#/definitions/ResponseBoardDetailInfo"
        }
    }


# 페이징 + 게시글 목록
written_paging = copy.deepcopy(base)
written_paging["summary"] = "GET boardinfos with page"
written_paging["parameters"].append(
    {
        "name": "num",
        "in": "path",
        "required": True,
        "description": "Number of paging",
        "type": "integer"
    }
)
written_paging["parameters"].append(
    {
        "name": "limit",
        "in": "path",
        "required": True,
        "description": "limit of paging",
        "type": "integer"
    }
)


# 작성자 검색
get_board_in_writer = copy.deepcopy(written_list)
get_board_in_writer["summary"] = "GET boardinfos in userid"
get_board_in_writer["parameters"].append(
    {
        "name": "writer",
        "in": "query",
        "required": True,
        "description": "userid",
        "type": "string"
    }
)
get_board_in_writer["parameters"].append(
    {
        "name": "num",
        "in": "query",
        "required": True,
        "description": "Number of paging",
        "type": "integer"
    }
)
get_board_in_writer["parameters"].append(
    {
        "name": "limit",
        "in": "query",
        "required": True,
        "description": "limit of paging",
        "type": "integer"
    }
)


# 제목 검색
get_board_in_title = copy.deepcopy(written_list)
get_board_in_title["parameters"].append(
    {
        "name": "title",
        "in": "query",
        "required": True,
        "description": "title",
        "type": "string"
    }
)
get_board_in_title["parameters"].append(
    {
        "name": "num",
        "in": "query",
        "required": True,
        "description": "Number of paging",
        "type": "integer"
    }
)
get_board_in_title["parameters"].append(
    {
        "name": "limit",
        "in": "query",
        "required": True,
        "description": "limit of paging",
        "type": "integer"
    }
)


# 내용 검색
get_board_in_content = copy.deepcopy(written_list)
get_board_in_content["summary"] = "GET boardinfos in content"
get_board_in_content["parameters"].append(
    {
        "name": "content",
        "in": "query",
        "required": True,
        "description": "content",
        "type": "string"
    }
)
get_board_in_content["parameters"].append(
    {
        "name": "num",
        "in": "query",
        "required": True,
        "description": "Number of paging",
        "type": "integer"
    }
)
get_board_in_content["parameters"].append(
    {
        "name": "limit",
        "in": "query",
        "required": True,
        "description": "limit of paging",
        "type": "integer"
    }
)
