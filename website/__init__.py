from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# import json

db = SQLAlchemy()
DB_NAME = "database.db"

def start():
    app = Flask(__name__)
    keyfile = open("session.key")
    key = keyfile.read()
    keyfile.close()
    app.config["SECRET_KEY"] = key
    app.config["SQLALCHEMY_DATABASE_URI"] =  f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .epauth import epauth
    from .epchar import epchar
    from .epmain import epmain
    from .eprefs import eprefs
    from .eprule import eprule
    from .eptool import eptool

    app.register_blueprint(epauth, url_prefix="/")
    app.register_blueprint(epchar, url_prefix="/Character")
    app.register_blueprint(epmain, url_prefix="/")
    app.register_blueprint(eprefs, url_prefix="/Reference")
    app.register_blueprint(eprule, url_prefix="/Rules")
    app.register_blueprint(eptool, url_prefix="/Tools")

    from .models import User, Ruleset, Category, Rule, Language, Item, MagicItem, Condition, Skill, Action, Race, RaceFeature, Subrace, SubraceFeature, Feat, Background, BackgroundFeature, Playerclass, ClassFeature, Subclass, SubclassFeature, Monster, MonsterAbility, Character

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "epauth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return(User.query.get(int(id)))

    return app

def create_database(app):
    if(not path.exists("website/" + DB_NAME)):
        db.create_all(app=app)
        print("Created Database")
