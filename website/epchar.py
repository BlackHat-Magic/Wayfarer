from flask import Blueprint, Flask, render_template, redirect, url_for, request, session

epchar = Blueprint('epchar', __name__)

## CHARACTERS
@epchar.route("/")
def char():
    return(render_template("characters.html"))

@epchar.route("/Races")
def races():
    return(render_template("races.html"))

@epchar.route("/Backgrounds")
def backgrounds():
    return(render_template("backgrounds.html"))

@epchar.route("/Feats")
def feats():
    return(render_template("feats.html"))

@epchar.route("/Other")
def other():
    return(render_template("other.html"))

@epchar.route("/Stats")
def stats():
    return(render_template("stats.html"))

@epchar.route("/Backstory")
def backstory():
    return(render_template("backstory.html"))

@epchar.route("/Name")
def name():
    return(render_template("name.html"))
