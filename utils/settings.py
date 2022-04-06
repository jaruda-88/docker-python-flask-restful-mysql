#settings


BUILD = { 
    'type' : 'server',
    'db_host' : { "server" : 'mydatabase.cvc2dcwg4ut0.ap-northeast-2.rds.amazonaws.com', 'local' : '3.38.135.214', 'develop' : '192.168.1.69' },
    'db_user' : { "server" : 'jaruda', 'local' : 'root', 'develop' : 'root' },
    'db_pw' : { "server" : 'Jkk100458', 'local' : 'password', 'develop' : 'password' }
 }


DATABASE_CONFIG = {
    'HOST' : BUILD['db_host'].get(BUILD['type'], 'None'),
    'USER' : BUILD['db_user'].get(BUILD['type'], 'None'),
    'PASSWORD' : BUILD['db_pw'].get(BUILD['type'], 'None'),
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
                "in": "header"
            }
        }
    }
}
