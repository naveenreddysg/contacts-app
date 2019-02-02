from db import session
from utils.util import pwd_to_hash, model_to_dict
from sqlalchemy import or_
from models.profile_model import  ProfileModel
from mappers.profile_mapper import ProfileMapper


import datetime


class ProfileService:
    session_info = None

    def mapping(self, model, req_data):

        if model.id is None:
            model.name = req_data["name"]
            model.email = req_data["email"]
            model.password = pwd_to_hash(req_data["password"])
            model.createdOn = datetime.datetime.now()
        model.updatedOn = datetime.datetime.now()
        ProfileMapper(model, req_data).model_mapping()

    def is_validate(self, model, is_new):
        query = session.query(ProfileModel). \
            filter(
            (ProfileModel.email == model.email)
        )
        data_list = query.all()
        if data_list:
            if is_new:
                print("true")
                return False
            else:
                for item in data_list:
                    print("item", item)
                    if item.id != model.id:
                        print("item.id", item.id)
                        print("model.id", model.id)
                        return False
        return True

    def model(self, _id):
        return session.query(ProfileModel).filter_by(id=_id).first()

    def save(self, req_data):
        profile = None
        _id = req_data.get('id')
        print(_id)
        if _id is not None:
            profile = self.model(_id)
        if profile is None:
            profile = ProfileModel()
        self.mapping(profile, req_data)

        if self.is_validate(profile, False if _id else True):
            session.add(profile)
            session.commit()
            return {'message': 'Saved Successfully', 'id': profile.id}
        else:
            raise Exception('Record already exists')

    def search(self, searchParm):

        query = session.query(ProfileModel)
        query = query.filter(or_(
            ProfileModel.name.like('%' + searchParm + '%'),
            ProfileModel.email.like('%' + searchParm + '%'))
        )
        res_data = query.limit(9999).all()
        res_data = list(map(model_to_dict, res_data))
        return res_data

    def delete(self, id):
        if id is None:
            raise Exception("id required to delete data")
        else:
            profile = ProfileModel.query.get(id)
            session.delete(profile)
            session.commit()
            return {'message': 'deleted Successfully', 'id': id}