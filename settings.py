#settings

BUILD = "local"


DATABASE_CONFIG = {
    'HOST' : '3.38.135.214' if BUILD == "server" else "192.168.1.69",
    'USER' : 'root',
    'PASSWORD' : 'password',
    'DB' : 'project1',
    'PORT' : 3306,
}


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
    }
    # "securityDefinitions": {
    #     "Kakao": {
    #         "type": "apiKey",
    #         "name": "Authorization",
    #         "in": "header",
    #         "description": "Authorization header using JWT token"
    #     }
    # },
    # "security": [
    #     {
    #         "JWT": [ ]
    #     }
    # ]
}