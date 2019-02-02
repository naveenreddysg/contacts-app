from db import session
from utils.util import pwd_to_hash, model_to_dict
from sqlalchemy import or_
from models.contacts_model import ContactModel
from mappers.contacts_mapper import ContactsMapper


import datetime


class ContactService:
    session_info = None

    def mapping(self, model, req_data):

        if model.id is None:
            model.name = req_data["name"]
            model.email = req_data["email"]
            model.phone = req_data["phone"]
            model.mobile = req_data["mobile"]
            model.createdOn = datetime.datetime.now()
        model.updatedOn = datetime.datetime.now()
        ContactsMapper(model, req_data).model_mapping()

    def is_validate(self, model, is_new):
        query = session.query(ContactModel). \
            filter(
            (ContactModel.email == model.email)
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
        return session.query(ContactModel).filter_by(id=_id).first()

    def save(self, req_data):
        contact = None
        _id = req_data.get('id')
        print(_id)
        if _id is not None:
            contact = self.model(_id)
        if contact is None:
            contact = ContactModel()
        self.mapping(contact, req_data)

        if self.is_validate(contact, False if _id else True):
            session.add(contact)
            session.commit()
            return {'message': 'Saved Successfully', 'id': contact.id}
        else:
            raise Exception('Record already exists')

    def search(self, searchParm):

        query = session.query(ContactModel)
        query = query.filter(or_(
            ContactModel.name.like('%' + searchParm + '%'),
            ContactModel.email.like('%' + searchParm + '%'),
            ContactModel.mobile.like('%' + searchParm + '%'),
            ContactModel.phone.like('%' + searchParm + '%')
            )
        )
        res_data = query.limit(9999).all()
        res_data = list(map(model_to_dict, res_data))
        return res_data

    def delete(self, id):
        if id is None:
            raise Exception("id required to delete data")
        else:
            contact = ContactModel.query.get(id)
            session.delete(contact)
            session.commit()
            return {'message': 'deleted Successfully', 'id': id}