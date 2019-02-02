from main import profile, contact
from utils import security_user


def register_blueprints(app):
    app.register_blueprint(security_user.blueprint)
    app.register_blueprint(profile.blueprint)
    app.register_blueprint(contact.blueprint)
