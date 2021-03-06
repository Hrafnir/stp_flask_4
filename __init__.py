from flask import Flask
from flask_login import LoginManager
from admin import *



def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)
    admin.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app

