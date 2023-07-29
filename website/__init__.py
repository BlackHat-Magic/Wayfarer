from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import openai, os
# import json

load_dotenv()
db = SQLAlchemy()
DB_NAME = "database.db"
openai.api_key = os.getenv("OPENAI_API_KEY")

def start():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
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

    from .models import User, Ruleset, Category, Rule, Language, ItemTag, Property, Item, Condition, Skill, Action, Race, RaceFeature, Subrace, SubraceFeature, Feat, Spell, Background, BackgroundFeature, Playerclass, ClassFeature, Subclass, SubclassFeature

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "epauth.noRulesetLogin"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return(User.query.get(id))

    return app

def create_database(app):
    if(not path.exists("website/" + DB_NAME)):
        with app.app_context():
            db.create_all(app=app)
            from .models import User, Ruleset
            admin_user = User(
                username = os.getenv("DEFAULT_USERNAME"),
                password = generate_password_hash(os.getenv("DEFAULT_PASSWORD"), method="sha256"),
                is_admin = True
            )
            db.session.add(admin_user)
            admin_ruleset = Ruleset(
                identifier = "admin",
                is_admin = True,
                user = admin_user,
                viewers = [admin_user.id],
                editors = [admin_user.id],
                visibility = 2,
                name = "admin",
                description = "default admin ruleset"
            )
            db.session.add(admin_ruleset)
            admin_user.current_ruleset = admin_ruleset.id
            db.session.commit()
        print("Created Database")
