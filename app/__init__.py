from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
from flask_mail import Mail
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login' # type: ignore

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)
    

    db.init_app(app)

    # routes i custom error routes here

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app