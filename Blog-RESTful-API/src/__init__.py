from flask import Flask, jsonify, request, url_for, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, desc
from sqlalchemy.exc import *
from werkzeug.security import generate_password_hash, check_password_hash

from constant.http_response import *

from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, get_jwt_identity, jwt_required, current_user

from flasgger import Swagger, swag_from
from config_swagger.config import template, swagger_config

app = Flask(__name__)
db = SQLAlchemy(app)
CORS(app = app)
jwt = JWTManager(app = app)
Swagger(app = app, config= swagger_config, template= template)

app.config['SECRET-KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog_api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

app.config['JWT_SECRET_KEY'] = 'secret'

app.config['SWAGGER'] = {
    'title' : 'Blog API',
    'uiversion' : 3
}







