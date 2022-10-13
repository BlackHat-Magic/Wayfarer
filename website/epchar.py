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
            if(len(data["name"]) < 1):
                return('1')
            elif(len(data["name"]) > 127):
                return('2')
            elif(len(data["flavor"]) > 16383):
                return('3')
            elif("<" in data["name"] or ">" in data["name"] or "<" in data["flavor"] or ">" in data["flavor"]):
                return('4')
            elif("javascript" in data["name"] or "javascript" in data["flavor"]):
                return('5')
            for feature in data["features"]:
                if(len(feature["name"]) < 1):
                    return('6')
                elif(len(feature["name"]) > 127):
                    return('7')
                elif(len(feature["text"]) > 16383):
                    return('8')
                elif("<" in feature["name"] or ">" in feature["name"] or "<" in feature["text"] or ">" in feature["text"]):
                    return('4')
                elif("javascript" in feature["name"] or "javascript" in feature["text"]):
                    return('5')
            if(data["has_subraces"]):
                for subrace in data["subraces"]:
                    if(len(subrace["name"]) < 1):
                        return('9')
                    elif(len(subrace["name"]) > 127):
                        return('10')
                    elif(len(subrace["text"]) > 16383):
                        return('11')
                    elif("<" in subrace["name"] or ">" in subrace["name"] or "<" in subrace["text"] or ">" in subrace["text"]):
                        return('4')
                    elif("javascript" in feature["name"] or "javascript" in feature["text"]):
                        return('5')
                    for feature in subrace["features"]:
                        if(len(feature["name"]) < 1):
                            return('12')
                        elif(len(feature["name"]) > 127):
                            return('13')
                        elif(len(feature["text"]) > 16383):
                            return('14')
                        elif("<" in feature["name"] or ">" in feature["name"] or "<" in feature["text"] or ">" in feature["text"]):
                            return('4')
                        elif("javascript" in feature["name"] or "javascript" in feature["text"]):
                            return('5')
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
            return(0)
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
