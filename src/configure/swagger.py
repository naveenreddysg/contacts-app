from flasgger import Swagger


def swagger(app):
    app.config['SWAGGER'] = {
        'uiversion': 3,
        "title": "Contacts-app",
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
    }
    Swagger(app,  template={
        "swagger": "3.0",
        "headers": [
        ],
        "consumes": [
            "application/json",
            "application/x-www-form-urlencoded",
        ],
        "produces": [
            "application/json",
        ],
        "securityDefinitions": {
            "jwt": {
                "type": 'apiKey',
                "name": 'Authorization',
                "in": 'header'
            }
        },
        "security": [
            {"jwt": []}
        ]
    })