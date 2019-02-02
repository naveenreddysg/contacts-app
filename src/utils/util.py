from sqlalchemy.orm.mapper import class_mapper
from sqlalchemy import inspect
import time, secrets, string
from bcrypt import hashpw, gensalt
from cryptography.fernet import Fernet
from random import randint

SECRET_KEY = "PILVO-ASSIGNMENT-CONTACT-BOOK-APP"


def model_to_dict(obj, visited_children=None, back_relationships=None):
    if visited_children is None:
        visited_children = set()
    if back_relationships is None:
        back_relationships = set()
    serialized_data = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
    relationships = class_mapper(obj.__class__).relationships
    visitable_relationships = [(name, rel) for name, rel in relationships.items() if name not in back_relationships]
    for name, relation in visitable_relationships:
        if relation.backref:
            back_relationships.add(relation.backref)
        relationship_children = getattr(obj, name)
        if relationship_children is not None:
            if relation.uselist:
                children = []
                for child in [c for c in relationship_children if c not in visited_children]:
                    visited_children.add(child)
                    children.append(model_to_dict(child, visited_children, back_relationships))
                serialized_data[name] = children
            else:
                serialized_data[name] = model_to_dict(relationship_children, visited_children, back_relationships)
    return serialized_data


def pwd_to_hash(password):
    hashed = hashpw(password.encode(), gensalt())
    return hashed


def pwd_check(password, pwd_from_db):
    if hashpw(password.encode(), pwd_from_db) == pwd_from_db:
        return True
    else:
        return False