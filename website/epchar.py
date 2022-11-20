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
                result = jsonify({"code": 1})
                return(result)
            elif(len(data["name"]) > 127):
                result = jsonify({"code": 2})
                return(result)
            elif(len(data["flavor"]) > 16383):
                result = jsonify({"code": 3})
                return(result)
            elif("<" in data["name"] or "<" in data["flavor"]):
                result = jsonify({"code": 4})
                return(result)
            elif("javascript" in data["name"] or "javascript" in data["flavor"]):
                result = jsonify({"code": 5})
                return(result)
            elif("-" in data["name"]):
                result = jsonify({"code": 15})
                return(result)
            for feature in data["features"]:
                if(len(feature["name"]) < 1):
                    result = jsonify({"code": 6})
                    return(result)
                elif(len(feature["name"]) > 127):
                    result = jsonify({"code": 7})
                    return(result)
                elif(len(feature["text"]) > 16383):
                    result = jsonify({"code": 8})
                    return(result)
                elif("<" in feature["name"] or "<" in feature["text"]):
                    result = jsonify({"code": 4})
                    return(result)
                elif("javascript" in feature["name"] or "javascript" in feature["text"]):
                    result = jsonify({"code": 5})
                    return(result)
            if(data["has_subraces"]):
                for subrace in data["subraces"]:
                    if(len(subrace["name"]) < 1):
                        result = jsonify({"code": 9})
                        return(result)
                    elif(len(subrace["name"]) > 127):
                        result = jsonify({"code": 10})
                        return(result)
                    elif(len(subrace["text"]) > 16383):
                        result = jsonify({"code": 11})
                        return(result)
                    elif("<" in subrace["name"] or "<" in subrace["text"]):
                        result = jsonify({"code": 4})
                        return(result)
                    elif("javascript" in feature["name"] or "javascript" in feature["text"]):
                        result = jsonify({"code": 5})
                        return(result)
                    for feature in subrace["features"]:
                        if(len(feature["name"]) < 1):
                            result = jsonify({"code": 12})
                            return(result)
                        elif(len(feature["name"]) > 127):
                            result = jsonify({"code": 13})
                            return(result)
                        elif(len(feature["text"]) > 16383):
                            result = jsonify({"code": 14})
                            return(result)
                        elif("<" in feature["name"] or "<" in feature["text"]):
                            result = jsonify({"code": 4})
                            return(result)
                        elif("javascript" in feature["name"] or "javascript" in feature["text"]):
                            result = jsonify({"code": 5})
                            return(result)
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
                weight_die = data["weight_die"],
                subrace_flavor = data["subrace_flavor"]
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
            return("0")
    return(render_template("create-race.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Races/<string:race>")
def race(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    display = Race.query.filter_by(rulesetid=cruleset.id, name=race).first()
    return(render_template("race.html", user=current_user, frulesets=frulesets, cruleset=cruleset, race=display))

@epchar.route("/Backgrounds")
def backgrounds():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("backgrounds.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Backgrounds/Create", methods=["GET", "POST"])
@login_required
def createBackground():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create backgrounds for a ruleset that is not your own.")
            return("1")
        else:
            print("fuck")
            data = json.loads(request.data)
            if(len(data["name"]) < 1):
                flash("You must specify a background name.")
                return("1")
            elif(len(data["name"]) > 127):
                flash("Background name must be fewer than 128 characters.")
                return("1")
            elif(len(data["skills"]) > 255 or len(data["tools"]) > 255 or len(data["lang"]) > 255):
                flash("Skills, tools, and languages must be fewer than 256 characters each.")
                return("1")
            elif(len(data["equipment"]) > 511):
                flash("Equipment must be fewer than 512 characters.")
                return("1")
            elif(len(data["text"]) > 16383):
                flash("Text must be fewer than 16384 characters.")
                return("1")
            elif("-" in data["name"]):
                flash("Dashes (\"-\") are not allowed in the background name.")
                return("1")
            elif("<" in data["text"] or "<" in data["name"]):
                flash("Open angle brackets(\"<\") are not allowed.")
                return("1")
            elif("javascript" in data["text"] or "javascript" in data["name"]):
                flash("Cross-site scripting attacks are not allowed.")
                return("1")
            else:
                for feature in data["features"]:
                    if(len(feature["name"]) < 1):
                        flash("You must specify a feature name.")
                        return("1")
                    elif(len(feature["name"]) > 127):
                        flash("Feature name must be fewer than 128 characters.")
                        return("1")
                    elif(len(feature["text"]) > 16383):
                        flash("Text must be fewer than 16383 characters.")
                        return("1")
                    elif("<" in feature["name"] or "<" in feature["text"]):
                        flash("Open angle brackets(\"<\") are not allowed.")
                        return("1")
                    elif("javascript" in feature["name"] or "javascript" in feature["text"]):
                        flash("Cross-site scripting attacks are not allowed.")
                        return("1")
                new_background = Background(
                    rulesetid = cruleset.id,
                    name = data["name"],
                    skills = data["skills"],
                    tools = data["tools"],
                    languages = data["languages"],
                    equipment = data["equipment"],
                    text = data["text"]
                )
                db.session.add(new_background)
                db.session.commit()

                new_background = db.query.filter_by(
                    name = data["name"],
                    rulesetid = cruleset.id
                ).first()
                for feature in data["features"]:
                    new_feature = BackgroundFeature(
                        backgroundid = new_background.id,
                        name = feature["name"],
                        text = feature["text"]
                    )
                    db.session.add(new_feature)
                db.session.commit()
                flash("Background created!")
                return("0")
    return(render_template("create-background.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

@epchar.route("/Backgrounds/<string:background>")
def background():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(render_template("background.html", user=current_user, frulesets=frulesets, cruleset=cruleset))

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
