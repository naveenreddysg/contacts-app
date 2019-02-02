from flasgger import swag_from
from flask import request, jsonify, json
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from db import db
from sqlalchemy import text, or_
from utils.util import pwd_check, pwd_to_hash, model_to_dict
from models.profile_model import ProfileModel

from flask import Blueprint

blueprint = Blueprint("security_user", __name__)

class JwtIdentify(object):
    def __init__(self, id):
        self.id = id


@swag_from('../../spec/app/auth.yml')
@blueprint.route("/auth", methods=['POST'])
def post():
    print("inside post")
    pass

def authenticate(username, password):
    print("inside post authenticate")
    data = db.session.query(ProfileModel).filter(
        or_(ProfileModel.email==username)).first()
    if data is not None:
        data = model_to_dict(data)
        if pwd_check(password, data['password'].encode()):
            user = {
                "id": data["id"],
                "email": data["email"],
                "name": data["name"]
            }
            return JwtIdentify(user)
        else:
            return None

def identity(payload):
    jwt_identity = payload['identity']
    print ("++++++++++++++++++")
    print (jwt_identity)
    print("++++++++++++++++++")
    return jwt_identity