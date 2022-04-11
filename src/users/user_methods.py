import copy


# 유저 method 공통
base = {
    "consumes": "application/json",
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
        "users"
    ],
    "definitions": {
        "ResponseUserInfo": {
            "type": "object",
            "properties": {
                "resultCode": {
                    "type": "string"
                },
                "resultMsg": {
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "userid": {
                            "type": "string"
                        },
                        "username": {
                            "type": "string"
                        },
                        "connected_at": {
                            "type": "string"
                        }
                    }
                }
            }
        },
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
        },
        "UserEditInfo": {
            "type": "object",
            "required": [
                "id", "userid", "pw"
            ],
            "properties": {
                "id": {
                    "type": "integer"
                },
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


# 유저 정보(토큰 인증)
user_get = copy.deepcopy(base)
user_get['summary'] = "GET user info"


# 유저 정보 DB pk 검색
user_get_in_id = copy.deepcopy(base)
user_get_in_id['summary'] = "GET userinfos in pk(id)"
user_get_in_id['parameters'].append(
    { 
        "name" : 'pk',
        "in": "path",
        "description": "-1(all) or pk(id)",
        "type": "integer",
        "required" : True 
    }
)
user_get_in_id['responses']['200'].clear()
user_get_in_id['responses']['200'] =\
    {
        "description":"Ok",
        "schema": {
            "$ref": "#/definitions/ResponseUserInfo"
        }
    }


# 유저 정보 DB userid 검색
user_get_in_userid = copy.deepcopy(base)
user_get_in_userid['summary'] = "GET userinfos in userid"
user_get_in_userid['parameters'].append(
    { 
        "name" : 'userid',
        "in": "path",
        "description": "userid",
        "type": "string",
        "required" : True 
    }
)
user_get_in_userid['responses']['200'].clear()
user_get_in_userid['responses']['200'] =\
    {
        "description":"Ok",
        "schema": {
            "$ref": "#/definitions/ResponseUserInfo"
        }
    }


# 유저 정보 DB username 검색
user_get_in_username = copy.deepcopy(base)
user_get_in_username['summary'] = "GET userinfos in username"
user_get_in_username['parameters'].append(
    {
        "name": "name",
        "in": "path",
        "description": "username",
        "type": "string",
        "required": True
    }
)
user_get_in_username['responses']['200'].clear()
user_get_in_username['responses']['200'] =\
    {
        "description":"Ok",
        "schema": {
            "$ref": "#/definitions/ResponseUserInfo"
        }
    }


# 유저 등록
user_post = copy.deepcopy(base)
user_post['summary'] = "POST registration user"
user_post['parameters'] = [
    {
        "name": "registration request",
        "in": "body",
        "description": "user info",
        "schema": {
            "$ref": "#/definitions/UserRegistrationInfo"
        }
    }
]


# 유저 수정
user_put = copy.deepcopy(base)
user_put['summary'] = "PUT edit user"
user_put['parameters'].append(
    {
        "name": "user edit request",
        "in": "body",
        "description": "modify userinfo",
        "schema": {
            "$ref": "#/definitions/UserEditInfo"
        }
    }
)
