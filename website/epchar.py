from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature
from flask_login import current_user, login_required
from .check_ruleset import *
from . import db
import json

epchar = Blueprint('epchar', __name__)


## CHARACTERS
@epchar.route("/")
def char():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("characters.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Races")
def races():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    # print(cruleset.races)
    return(render_template("races.html", user=current_user, frulesets=frulesets, cruleset=cruleset, ability=''))

@epchar.route("/Races/Create", methods=["GET", "POST"])
@login_required
def createRace():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create a race in a ruleset that is not yours.")
        else:
            data = json.loads(request.data)
            new_race = Race(
                rulesetid = cruleset.id,
                name = data["name"],
                flavor = data["flavor"],
                strasi = data["str"],
                dexasi = data["dex"],
                conasi = data["con"],
                intasi = data["int"],
                wisasi = data["wis"],
                chaasi = data["cha"],
                asi_text = data["asi_text"],
                size = data["size"],
                size_text = data["size_text"],
                walk = data["walk"],
                swim = data["swim"],
                fly = data["fly"],
                burrow = data["burrow"],
                base_height = data["base_height"],
                height_num = data["height_num"],
                height_die = data["height_die"],
                base_weight = data["base_weight"],
                weight_num = data["weight_num"],
                weight_die = data["weight_die"]
            )
            db.session.add(new_race)
            db.session.commit()
            new_race = Race.query.filter_by(
                name = data["name"], 
                rulesetid = cruleset.id
            ).first()
            for feature in data["features"]:
                new_feature = RaceFeature(
                    raceid = new_race.id,
                    name = feature["name"],
                    text = feature["text"]
                )
                db.session.add(new_feature)
            db.session.commit()
            if(data["has_subraces"]):
                for subrace in data["subraces"]:
                    new_subrace = Subrace(
                        raceid = new_race.id,
                        name = subrace["name"],
                        text = subrace["text"]
                    )
                    db.session.add(new_subrace)
                    db.session.commit()
                    new_subrace = Subrace.query.filter_by(
                        raceid = new_race.id,
                        name = subrace["name"],
                        text = subrace["text"]
                    ).first()
                    for feature in subrace["features"]:
                        new_feature = SubraceFeature(
                            raceid = new_subrace.id,
                            name = feature["name"],
                            text = feature["text"]
                        )
                        db.session.add(new_feature)
                    db.session.commit()
            return(redirect(url_for("epchar.createRace")))
    return(render_template("create-race.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Races/<string:race>")
def race():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("race.html", user=current_user, frulesets = frulesets, cruleset=cruleset))

@epchar.route("/Backgrounds")
def backgrounds():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("backgrounds.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Feats")
def feats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("feats.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Stats")
def stats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("stats.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Name")
def name():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("name.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Step-by-Step")
def stepByStep():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("step-by-step.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
