from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user
from . import db

epchar = Blueprint('epchar', __name__)

## CHARACTERS
@epchar.route("/")
def char():
    return(render_template("characters.html", user=current_user, frulesets = rulesets))

@epchar.route("/Races")
def races():
    return(render_template("races.html", user=current_user))

@epchar.route("/Backgrounds")
def backgrounds():
    return(render_template("backgrounds.html", user=current_user))

@epchar.route("/Feats")
def feats():
    return(render_template("feats.html", user=current_user))

@epchar.route("/Stats")
def stats():
    return(render_template("stats.html", user=current_user))

@epchar.route("/Name")
def name():
    return(render_template("name.html", user=current_user))

@epchar.route("/Step-by-Step")
def stepByStep():
    return(render_template("step-by-step.html", user=current_user))
