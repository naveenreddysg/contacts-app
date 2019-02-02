from flask import Blueprint
from flask import request, jsonify, json, abort
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.contact_service import ContactService, ContactModel
from utils.util import model_to_dict
from db import session

contact_service = ContactService()
blueprint = Blueprint("contact", __name__)


@blueprint.route("/contact", methods=["PUT"])
@jwt_required()
@swag_from('../../spec/contact/update.yml')
def contact_update():
    try:
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        if req_data.get("id") is None:
            raise Exception("id required to update date")
        else:
            res_data = contact_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/contact", methods=["POST"])
@jwt_required()
@swag_from('../../spec/contact/create.yml')
def contact_post():
    try:
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = contact_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/contact", methods=["GET"])
@jwt_required()
@swag_from('../../spec/contact/get.yml')
def contact_get():
    try:
        _id = request.args['id']
        res_data = contact_service.model(_id)
        res_json = {'status': 1, 'data': model_to_dict(res_data)}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/contact", methods=["DELETE"])
@jwt_required()
@swag_from('../../spec/contact/delete.yml')
def contact_delete():
    try:
        contact_service.session_info = current_identity
        id = request.args['id']
        res_data = contact_service.delete(id)
        print(res_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/searchcontact", methods=["GET"])
@jwt_required()
@swag_from('../../spec/contact/search.yml')
def contact_search():
    try:
        searchParm = request.args['searchParm']
        res_data = contact_service.search(searchParm)
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


@blueprint.route('/contacts/search/page', methods=["GET"])
@jwt_required()
@swag_from('../../spec/contact/search.yml')
def view():
    try:

        searchParm = request.args['searchParm']
        return jsonify(contact_service.get_paginated_list(searchParm,
                    '/api/v2/events/page',
                    start=request.args.get('start', 1),
                    limit=request.args.get('limit', 10)
                ))
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
        return jsonify(res_json)

