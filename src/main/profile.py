from flask import Blueprint
from flask import request, jsonify, json
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.profile_service import ProfileService, ProfileModel
from utils.util import model_to_dict, pwd_to_hash
from db import session

profile_service = ProfileService()
blueprint = Blueprint("profile", __name__)


@blueprint.route("/profile", methods=["PUT"])
@jwt_required()
@swag_from('../../spec/profile/create.yml')
def profile_update():
    try:
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        if req_data.get("id") is None:
            raise Exception("id required to update date")
        else:
            res_data = profile_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/profile", methods=["POST"])
# @jwt_required()
@swag_from('../../spec/profile/create.yml')
def profile_post():
    try:
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = profile_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/profile", methods=["GET"])
@jwt_required()
@swag_from('../../spec/profile/get.yml')
def profile_get():
    try:
        _id = request.args['id']
        res_data = profile_service.model(_id)
        res_json = {'status': 1, 'data': model_to_dict(res_data)}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/profile", methods=["DELETE"])
@jwt_required()
@swag_from('../../spec/profile/delete.yml')
def profile_delete():
    try:
        profile_service.session_info = current_identity
        id = request.args['id']
        res_data = profile_service.delete(id)
        print(res_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/searchprofile", methods=["GET"])
@jwt_required()
@swag_from('../../spec/profile/search.yml')
def profile_search():
    try:
        profile_service.session_info = current_identity
        searchParm = request.args['searchParm']
        res_data = profile_service.search(searchParm)
        # print(res_data)
        res_json = {'status': 1, 'data': res_data}
        # print(res_json)
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/resetpassword", methods=["PUT"])
# @jwt_required()
@swag_from('../../spec/app/reset_password.yml')
def reset_password():
    try:
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        data = model_to_dict(session.query(ProfileModel).filter_by(email=req_data["email"]).first())
        data["password"] = pwd_to_hash(req_data["password"])
        res_data = profile_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)