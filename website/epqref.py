from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from .models import Ruleset
from flask_login import login_user, current_user
from .check_ruleset import *

epqref = Blueprint('epqref', __name__)

## QUICK REFERENCE
@epqref.route("/")
def qref():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("quick-reference.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Actions")
def actions():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("actions.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Conditions")
def conditions():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("conditions.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Items")
def items():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("items.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Magic-Items")
def magicItems():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("magic-items.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Languages")
def qrefLang():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("qref-lang.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Spells")
def spells():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("spells.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Vehicles")
def vehicles():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("vehicles.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Recipes")
def recipes():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("recipes.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
