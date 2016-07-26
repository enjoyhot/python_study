# -*- coding:utf8 -*-

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

login_manager = LoginManager()
login_manager.session_protection = 'strong' #provide different levels of security
# login_manager.login_view = 'auth.login' #set the endpoint for the login page


def create_app(config_name):
    '''
    application factory for creating the app and dynamically loading the configuration while running the app
    '''

    #import the configuration defined in config.py after creating the app object
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #initialize the extension object
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    #create blueprint and register it
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
