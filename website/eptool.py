from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, stream_with_context
from .models import Ruleset
from flask_login import login_required, current_user
from .uservalidation import *

eptool = Blueprint('eptool', __name__)

## TOOLS
@eptool.route("/", subdomain="<ruleset>")
def tools(ruleset):
    return(redirect(url_for("epmain.home", ruleset=ruleset)))

@eptool.route("/VTT", subdomain="<ruleset>")
def vtt(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/NPC-Gen", subdomain="<ruleset>")
def npcGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "gen-npc.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Generate NPCs"
        )
    )

@eptool.route("/Backstory-Gen", subdomain="<ruleset>")
def backstoryGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/CR-Calc", subdomain="<ruleset>")
def crCalc(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Encounter-Gen", subdomain="<ruleset>")
def encounterGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Loot-Gen", subdomain="<ruleset>")
def lootGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Stat-Gen", subdomain="<ruleset>")
def statGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )
