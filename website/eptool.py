from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from .models import Ruleset
from flask_login import login_required, current_user
from .check_ruleset import *

eptool = Blueprint('eptool', __name__)

## TOOLS
@eptool.route("/")
def tools():
    return(redirect(url_for("epmain.home")))

@eptool.route("/VTT")
def vtt():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("vtt.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eptool.route("/NPC-Gen")
def npcGen():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("npc-gen.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eptool.route("/Backstory-Gen")
def backstoryGen():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("backstory-gen.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eptool.route("/CR-Calc")
def crCalc():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("cr-calc.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eptool.route("/Encounter-Gen")
def encounterGen():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("encounter-gen.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eptool.route("/Loot-Gen")
def lootGen():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("loot-gen.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eptool.route("/Stat-Gen")
def statGen():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("stat-gen.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eptool.route("/Backstory")
def backstory():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("backstory.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
