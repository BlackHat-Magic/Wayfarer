from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, jsonify, flash
from .models import Ruleset, Skill, Action, Condition
from flask_login import login_user, current_user, login_required
from .check_ruleset import *
from . import db
import json

eprefs = Blueprint('eprefs', __name__)

## QUICK REFERENCE
@eprefs.route("/")
def refs():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("quick-reference.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Actions")
def actions():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    actions = []
    for action in Action.query.filter_by(rulesetid = cruleset.id):
        actions.append(action)
    return(render_template("actions.html", user=current_user, frulesets=frulesets, cruleset=cruleset, actions=actions))

@eprefs.route("/Actions/Create", methods=["GET", "POST"])
@login_required
def createAction():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create actions for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            time = request.form.get("time")
            if(len(name) < 1):
                flash("You must specify an action name.")
            elif(len(name) > 127):
                flash("Action name must be fewer than 128 characters.")
            elif(len(time) > 127):
                flash("Action time must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Action text must be fewer than 16383 characters")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_action = Action(
                    rulesetid = cruleset.id,
                    name = name,
                    time = time,
                    text = text
                )
                db.session.add(new_action)
                db.session.commit()
                flash("Action created!")
                return(redirect(url_for("eprefs.actions")))
    return(render_template("create-action.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Conditions")
def conditions():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    conditions = []
    for condition in Condition.query.filter_by(rulesetid = cruleset.id):
        conditions.append(condition)
    return(render_template("conditions.html", user=current_user, frulesets=frulesets, cruleset=cruleset, conditions=conditions))

@eprefs.route("/Conditions/Create", methods=["GET", "POST"])
@login_required
def createCondition():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create conditions for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            if(len(name) < 1):
                flash("You must specify an action name.")
            elif(len(name) > 127):
                flash("Action name must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Action text must be fewer than 16383 characters")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_action = Condition(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_action)
                db.session.commit()
                flash("Condition created!")
                return(redirect(url_for("eprefs.conditions")))
    return(render_template("create-condition.html", user=current_user, frulesets=frulesets, cruleset=cruleset,))

@eprefs.route("/Items")
def items():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("items.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Magic-Items")
def magicItems():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("magic-items.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Languages")
def refsLang():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("refs-lang.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Spells")
def spells():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("spells.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Vehicles")
def vehicles():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("vehicles.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Recipes")
def recipes():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("recipes.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Skills")
def skills():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    abilitydict = {
        "N/A": "N/A",
        "STR": "Strength",
        "DEX": "Dexterity",
        "CON": "Constitution",
        "INT": "Intelligence",
        "WIS": "Wisdom",
        "CHA": "Charisma"
    }
    return(render_template("skills.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Skills/Create", methods=["GET", "POST"])
@login_required
def createSkill():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        if(current_user.id != cruleset.id):
            flash("You cannot create a skill for a ruleset that is not your own.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            ability = request.form.get("ability")
            if(ability == ""):
                ability = "STR"
            if(len(name) < 1):
                flash("You must specify a skill name.")
            elif(len(name) > 63):
                flash("Skill name must be fewer than 64 characters.")
            elif(len(text) > 16383):
                flash("Skill description must be fewer than 16384 characters.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            elif("<" in text):
                flash("Open angle brackets(\"<\") are not allowed.")
            else:
                new_skill = Skill(
                    rulesetid = cruleset.id,
                    name = name,
                    ability_score = ability,
                    description = text
                )
                db.session.add(new_skill)
                db.session.commit()
                flash("Skill created!")
                return(redirect(url_for("eprefs.skills")))
    return(render_template("create-skill.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@eprefs.route("/Skills/Delete/<int:rid>")
@login_required
def deleteSkill(rid):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(current_user.id != cruleset.userid):
        flash("You cannod delete skills from rulesets that are not your own.")
        return(redirect(url_for("eprefs.skills")))
    else:
        skill = Skill.query.filter_by(id=rid, rulesetid = cruleset.id).first()
        db.session.delete(skill)
        db.session.commit()
        flash("Skill deleted.")
        return(redirect(url_for("eprefs.skills")))
