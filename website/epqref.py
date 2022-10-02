from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user

epqref = Blueprint('epqref', __name__)

## QUICK REFERENCE
@epqref.route("/")
def qref():
    return(render_template("quick-reference.html", user=current_user))

@epqref.route("/Actions")
def actions():
    return(render_template("actions.html", user=current_user))

@epqref.route("/Conditions")
def conditions():
    return(render_template("conditions.html", user=current_user))

@epqref.route("/Items")
def items():
    return(render_template("items.html", user=current_user))

@epqref.route("/Magic-Items")
def magicItems():
    return(render_template("magic-items.html", user=current_user))

@epqref.route("/Languages")
def qrefLang():
    return(render_template("qref-lang.html", user=current_user))

@epqref.route("/Spells")
def spells():
    return(render_template("spells.html", user=current_user))

@epqref.route("/Vehicles")
def vehicles():
    return(render_template("vehicles.html", user=current_user))

@epqref.route("/Recipes")
def recipes():
    return(render_template("recipes.html", user=current_user))
