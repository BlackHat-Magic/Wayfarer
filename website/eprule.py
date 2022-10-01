from flask import Blueprint, Flask, render_template, redirect, url_for, request, session

eprule = Blueprint('eprule', __name__)

## RULES
@eprule.route("/")
def rules():
    return(render_template("rules.html"))

@eprule.route("/House-Rules")
def houseRules():
    return(render_template("house-rules.html"))

@eprule.route("/Higher-Levels")
def higherLevels():
    return(render_template("higher-levels.html"))

@eprule.route("/Languages")
def languages():
    return(render_template("languages.html"))

@eprule.route("/Multiclassing")
def multiclassing():
    return(render_template("multiclassing.html"))

@eprule.route("/Step-by-Step")
def stepByStep():
    return(render_template("step-by-step.html"))



