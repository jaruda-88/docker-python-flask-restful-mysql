# settings
from enum import Enum


class BuildType(Enum):
    SERVER = 1
    LOCAL = 2
    DEVELOP = 3
    NONE = 4


BUILD_TYPE = BuildType.SERVER


DATABASE_CONFIG = {
    # AWS RDS
    BuildType.SERVER : {
        'db_name': 'project1',
        'port': 3306,
        'host': 'mydatabase.cvc2dcwg4ut0.ap-northeast-2.rds.amazonaws.com',
        'user': 'jaruda',
        'pw': 'Jkk100458'
    },
    # AWS EC2 Docker
    BuildType.LOCAL : {
        'db_name': 'project1',
        'port': 3306,
        'host': '3.38.205.101',
        'user': 'root',
        'pw': 'password'
    },
    # test
    BuildType.DEVELOP : {
        'db_name': 'project1',
        'port': 3306,
        'host': '192.168.1.69',
        'user': 'root',
        'pw': 'password'
    },
}.get(BUILD_TYPE, BuildType.NONE)


SWAGGER_CONFIG = {
    "title": "SWAGGER TEST API",
    "uiversion": 3,
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'swagger_test_api',
            "route": '/swagger_test_api_spec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/help", # http swagger url /help or /docs
    "specs_route": "/help/"
}


SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Swagger Test API",
        "description": "Api for test",
        "version": "1.0.0",        
        "openapi_version": "3.0.2",
        "contact": {
            "name": "project source",
            "url": "https://github.com/jaruda-88/project1_back-end"
        }
    },
    "components": {
        "schemas": {
            "DefaultResponse": {
                "properties": {
                    "resultCode": {
                        "description": "httpstatus code number",
                        "type": "integer"
                    },
                    "resultMsg": {
                        "description": "response contents",
                        "type": "string"
                    }
                }
            }            
        },
        "parameters": {
            "TokenParam": {
                "description": "Authorization header using JWT token",  
                "type": "token",
                "name": "Authorization",
                "in": "header",
            }
        }
    }
}
