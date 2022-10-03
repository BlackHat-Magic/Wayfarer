from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user

eprule = Blueprint('eprule', __name__)

## RULES
@eprule.route("/")
def rules():
    return(render_template("rules.html", user=current_user))
