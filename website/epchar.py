from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash
from .models import Ruleset
from flask_login import current_user, login_required
from .check_ruleset import *
from . import db

epchar = Blueprint('epchar', __name__)


## CHARACTERS
@epchar.route("/")
def char():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("characters.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Races")
def races():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("races.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Backgrounds")
def backgrounds():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("backgrounds.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Feats")
def feats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("feats.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Stats")
def stats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("stats.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Name")
def name():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("name.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Step-by-Step")
def stepByStep():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("step-by-step.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
