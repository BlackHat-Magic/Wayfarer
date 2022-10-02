from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user

eprule = Blueprint('eprule', __name__)

## RULES
@eprule.route("/")
def rules():
    return(render_template("rules.html", user=current_user))

@eprule.route("/House-Rules")
def houseRules():
    return(render_template("house-rules.html", user=current_user))

@eprule.route("/Higher-Levels")
def higherLevels():
    return(render_template("higher-levels.html", user=current_user))

@eprule.route("/Languages")
def languages():
    return(render_template("languages.html", user=current_user))

@eprule.route("/Multiclassing")
def multiclassing():
    return(render_template("multiclassing.html", user=current_user))

@eprule.route("/Step-by-Step")
def stepByStep():
    return(render_template("step-by-step.html", user=current_user))



