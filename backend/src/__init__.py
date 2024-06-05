from flask import Flask
from datetime import timedelta
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
import json


def create_app(debug:bool = True) -> Flask:

    secret_name = "prod/postgres"
    region_name = "eu-north-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    secret_dict = json.loads(secret)

    username = secret_dict.get('username')
    password = secret_dict.get('password')
    host = secret_dict.get('host')
    secret_key = secret_dict.get('secretkey')
    bucket = secret_dict.get("bucket")

    app = Flask(__name__, static_url_path="/")
    app.config["DEBUG"] = debug
    app.config["SECRET_KEY"] = str(secret_key)
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{username}:{password}@{host}'
    CORS(app, resources={r"/*": {"origins": f"{bucket}/*"}})


    #extensions
    from backend.extensions import db, jwt, bcrypt
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    #create database
    from backend import models
    with app.app_context():
        db.create_all()
    
    #register blueprints
    from backend.routes import routesBP
    app.register_blueprint(routesBP)

    return app