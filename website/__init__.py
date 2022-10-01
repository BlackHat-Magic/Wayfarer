from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# import json

def start():
    app = Flask(__name__)
    keyfile = open("session.key")
    key = keyfile.read()
    keyfile.close()

    from .epauth import epauth
    from .epchar import epchar
    from .epmain import epmain
    from .epqref import epqref
    from .eprule import eprule
    from .eptool import eptool

    app.register_blueprint(epauth, url_prefix="/")
    app.register_blueprint(epchar, url_prefix="/Character")
    app.register_blueprint(epmain, url_prefix="/")
    app.register_blueprint(epqref, url_prefix="/Quick-Reference")
    app.register_blueprint(eprule, url_prefix="/Rules")
    app.register_blueprint(eptool, url_prefix="/Tools")

    return app

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#db = SQLAlchemy(app)
