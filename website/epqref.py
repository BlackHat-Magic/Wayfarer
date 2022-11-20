from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, jsonify, flash
from .models import Ruleset, Skill
from flask_login import login_user, current_user, login_required
from .check_ruleset import *
from . import db
import json

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

@epqref.route("/Skills")
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

@epqref.route("/Skills/Create", methods=["GET", "POST"])
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
                return(redirect(url_for("epqref.skills")))
    return(render_template("create-skill.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epqref.route("/Skills/Delete/<int:rid>")
@login_required
def deleteSkill(rid):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(current_user.id != cruleset.userid):
        flash("You cannod delete skills from rulesets that are not your own.")
        return(redirect(url_for("epqref.skills")))
    else:
        skill = Skill.query.filter_by(id=rid, rulesetid = cruleset.id).first()
        db.session.delete(skill)
        db.session.commit()
        flash("Skill deleted.")
        return(redirect(url_for("epqref.skills")))
