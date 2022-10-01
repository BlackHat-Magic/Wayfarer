from flask import Blueprint, Flask, render_template, redirect, url_for, request, session

epqref = Blueprint('epqref', __name__)

## QUICK REFERENCE
@epqref.route("/")
def qref():
    return(render_template("quick-reference.html"))

@epqref.route("/Actions")
def actions():
    return(render_template("actions.html"))

@epqref.route("/Conditions")
def conditions():
    return(render_template("conditions.html"))

@epqref.route("/Items")
def items():
    return(render_template("items.html"))

@epqref.route("/Magic-Items")
def magicItems():
    return(render_template("magic-items.html"))

@epqref.route("/Languages")
def qrefLang():
    return(render_template("qref-lang.html"))

@epqref.route("/Spells")
def spells():
    return(render_template("spells.html"))

@epqref.route("/Vehicles")
def vehicles():
    return(render_template("vehicles.html"))

@epqref.route("/Recipes")
def recipes():
    return(render_template("recipes.html"))
