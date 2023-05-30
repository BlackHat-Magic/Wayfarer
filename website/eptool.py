from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from .models import Ruleset
from flask_login import login_required, current_user
from .uservalidation import *

eptool = Blueprint('eptool', __name__)

## TOOLS
@eptool.route("/")
def tools():
    return(redirect(url_for("epmain.home", ruleset=ruleset)))

@eptool.route("/VTT")
def vtt():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/NPC-Gen")
def npcGen():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Backstory-Gen")
def backstoryGen():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/CR-Calc")
def crCalc():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Encounter-Gen")
def encounterGen():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Loot-Gen")
def lootGen():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Stat-Gen")
def statGen():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )
