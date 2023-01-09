from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature, Background, BackgroundFeature, Feat, Item, Playerclass
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
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(render_template("characters.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Races")
def races():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(render_template("races.html", user=current_user, frulesets=frulesets, cruleset=cruleset, ability='', adminrulesets=adminrulesets))

@epchar.route("/Races/Create", methods=["GET", "POST"])
@login_required
def createRace():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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

@epchar.route("/Race/<string:race>")
def race(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    display = Race.query.filter_by(rulesetid=cruleset.id, name=race).first()
    return(render_template("race.html", user=current_user, frulesets=frulesets, cruleset=cruleset, race=display, adminrulesets=adminrulesets))

@epchar.route("/Backgrounds")
def backgrounds():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(render_template("backgrounds.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Backgrounds/Create", methods=["GET", "POST"])
@login_required
def createBackground():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tools = []
    for tool in Item.query.filter_by(rulesetid = cruleset.id, is_tool = True):
        tools.append(tool)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create backgrounds for a ruleset that is not your own.")
            return("1")
        else:
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
                skills = ""
                for skill in data["skills"]:
                    if(len(skills) < 1):
                        skills += skill
                    else:
                        skills += f", {skill}"
                new_background = Background(
                    rulesetid = cruleset.id,
                    name = data["name"],
                    skills = skills,
                    tools = data["tools"],
                    languages = data["lang"],
                    equipment = data["equipment"],
                    text = data["text"]
                )
                db.session.add(new_background)
                db.session.commit()

                new_background = Background.query.filter_by(
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
    return(render_template("create-background.html", user=current_user, frulesets=frulesets, cruleset=cruleset, tools=tools))

@epchar.route("/Background/<string:background>")
def background(background):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    background = Background.query.filter_by(rulesetid = cruleset.id, name = background.replace("-", " ")).first()
    return(render_template("background.html", user=current_user, frulesets=frulesets, cruleset=cruleset, background=background, adminrulesets=adminrulesets))

@epchar.route("/Feats")
def feats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(render_template("feats.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Feats/Create", methods=["GET", "POST"])
@login_required
def createFeat():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create feats for rulesets that are not your own.")
        else:
            name = request.form.get("name")
            prereq = request.form.get("prereq")
            strasi = request.form.get("strasi")
            dexasi = request.form.get("dexasi")
            conasi = request.form.get("conasi")
            intasi = request.form.get("intasi")
            wisasi = request.form.get("wisasi")
            chaasi = request.form.get("chaasi")
            text = request.form.get("text")
            if(len(name) < 1):
                flash("You must specify a feat name.")
            elif(len(name) > 127):
                flash("Feat name must be fewer than 128 characters.")
            elif(len(prereq) > 255):
                flash("Feat Prerequisite must be fewer than 256 characters.")
            elif(len(text) > 16383):
                flash("Feat description must be fewer than 16384 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                try:
                    strasi = int(strasi)
                    dexasi = int(dexasi)
                    conasi = int(conasi)
                    intasi = int(intasi)
                    wisasi = int(wisasi)
                    chaasi = int(chaasi)
                except:
                    flash("Ability Score Improvements must all be integers.")
                    return(render_template("create-feat.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                new_feat = Feat(
                    rulesetid = cruleset.id,
                    name = name,
                    prerequisite = prereq,
                    strasi = strasi,
                    dexasi = dexasi,
                    conasi = conasi,
                    intasi = intasi,
                    wisasi = wisasi,
                    chaasi = chaasi,
                    text = text
                )
                db.session.add(new_feat)
                db.session.commit()
                flash("Feat created!")
                return(redirect(url_for("epchar.feats")))

    return(render_template("create-feat.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Feat/<string:feat>")
def feat(feat):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    feat = Feat.query.filter_by(rulesetid = cruleset.id, name = feat.replace("-", " ")).first()
    return(render_template("feat.html", user=current_user, frulesets=frulesets, cruleset=cruleset, feat=feat, adminrulesets=adminrulesets))

@epchar.route("/Ability-Scores")
def stats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(render_template("stats.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Ability-Scores/Edit", methods=["GET", "POST"])
@login_required
def editStats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot edit rulesets that are not your own.")
        else:
            text = request.form.get("text")
            if(len(text) > 65534):
                flash("Text must be fewer than 65535 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                cruleset.ability_scores = text
                db.session.commit()
                flash("Changes saved.")
                return(redirect(url_for("epchar.stats")))
    return(render_template("edit-stats.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Classes")
def classes():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(render_template("classes.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Classes/Create", methods=["GET", "POST"])
@login_required
def createClass():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create classes for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            hitdie = request.form.get("hitdie")
            proficiencies = request.form.get("proficiencies")
            saves = 0
            if(request.form.get("str")):
                saves += 32
            if(request.form.get("dex")):
                saves += 16
            if(request.form.get("con")):
                saves += 8
            if(request.form.get("int")):
                saves += 4
            if(request.form.get("wis")):
                saves += 2
            if(request.form.get("cha")):
                saves += 1
            skills = request.form.get("skills")
            equipment = request.form.get("equipment")
            gold_nums = request.form.get("gold_nums")
            gold_dice = request.form.get("gold_dice")
            gold_mult = request.form.get("gold_mult")
            multiclass_prereq = request.form.get("prereq")
            multiclass_skills = request.form.get("skills")
            subclass_name = request.form.get("subclass_name")
            if(len(subclass_name) == 0):
                subclass_name = "Subclass"
            text = request.form.get("text")
            class_features = []
            subclasses = []
            if(len(name) < 1):
                flash("You must specify a class name.")
            elif(len(name) > 127):
                flash("Class name must be fewer than 128 characters.")
            elif(len(equipment) > 1023):
                flash("Class equipment must be fewer than 1024 characters.")
            elif(len(gmulticlass_prereq) > 1023):
                flash("Class prerequisites must be fewer than 1024 characters")
            elif(len(subclass_name) > 127):
                flash("Subclass name must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Class description must be fewer than 16384 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                for index, featurename in request.form.getlist("class_feature_name"):
                    level = request.form.getlist("level")[index]
                    featuretext = request.form.getlist("class_feature_text")[index]
                    if(len(featurename) < 1):
                        flash("Each class feature must have a name.")
                        return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                    elif(len(featurename) > 127):
                        flash("Class feature names must be fewer than 128 characters.")
                        return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                    elif(len(featuretext) > 16383):
                        flash("Class feature descriptions must be fewer than 16383 characters.")
                        return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                    elif("<" in featuretext):
                        flash("Open angle brackets (\"<\") are not allowed.")
                    elif("javascript" in featuretext):
                        flash("Cross-site scripting attacks are not allowed.")
                    else:
                        class_features.append({
                            "name": featurename,
                            "level": level,
                            "text": featuretext
                        })
                for index, subclassname in request.form.getlist("subclass_name"):
                    subclasstext = request.form.getlist("subclass_text")[index]
                    caster_type = request.form.getlist("caster_type")[index]
                    if(len(subclassname) < 1):
                        flash("Each subclass must have a name.")
                        return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                    elif(len(subclassname) > 127):
                        flash("Subclass names must be fewer than 128 characters.")
                        return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                    elif(len(subclasstext) > 16383):
                        flash("Subclass descriptions must be fewer than 16384 characters.")
                        return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                    elif("<" in subclasstext):
                        flash("Open angle brackets (\"<\") are not allowed.")
                    elif("javascript" in subclass):
                        flash("Cross-site scripting attacks are not allowed.")
                    else:
                        subclass_features = []
                        for index2, subfeaturename in request.form.getlist(f"subclass_feature_{index}_name"):
                            level = request.form.getlist(f"subclass_feature_{index}_level")[index2]
                            stext = request.form.getlist(f"subclass_feature_{index}_text")
                            if(len(subfeaturename) < 1):
                                flash("Each subclass feature must have a name.")
                                return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                            elif(len(subfeaturename) > 127):
                                flash("Subclass feature names must be fewer than 128 characters.")
                                return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                            elif(len(stext) > 16383):
                                flash("Subclass feature descriptions must be fewer than 16384 characters.")
                                return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset))
                            else:
                                subclass_features.append({
                                    "name": subfeaturename,
                                    "level": level,
                                    "text": stext
                                })
                        subclasses.append({
                            "name": subclassname,
                            "text": subclass,
                            "caster_type": caster_type,
                            "features": subclass_features
                        })
                new_class = Playerclass(
                    rulesetid = cruleset.id,
                    name = name,
                    hitdie = hitdie,
                    proficiencies = proficiencies,
                    saves = saves,
                    skills = skills,
                    equipment = equipment,
                    gold_nums = gold_nums,
                    gold_dice = gold_dice,
                    gold_mult = gold_mult,
                    multiclass_prereq = multiclass_prereq,
                    multiclass_skills = multiclass_skills,
                    subclass_name = subclass_name,
                    text = text
                )
                db.session.add(new_class)
                db.session.commit()

                new_class = Playerclass.query.filter_by(rulesetid = cruleset.id, name = name).first()

                for feature in class_features:
                    new_feature = ClassFeature(
                        classid = new_class.id,
                        level_obtained = feature["level"],
                        name = feature["name"],
                        text = feature["text"]
                    )
                    db.session.add(new_feature)
                    db.session.commit()
                
                for subclass in subclasses:
                    new_subclass = Subclass(
                        classid = new_class.id,
                        name = subclass["name"],
                        caster_type = subclass["caster_type"],
                        text = subclass["text"]
                    )
                    db.session.add(new_subclass)
                    db.session.commit()

                    new_subclass = Subclass.query.filter_by(classid = new_class.id, name = subclass["name"]).first()

                    for feature in subclass["features"]:
                        new_feature = SubclassFeature(
                            subclassid = new_subclass.id,
                            name = feature["name"],
                            level_obtained = feature["level"],
                            text = feature["text"]
                        )
                        db.session.add(new_feature)
                        db.session.commit()
                flash("Class created!")
                return(redirect(url_for("epchar.classes")))
                        
    return(render_template("create-class.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Step-by-Step")
def stepByStep():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(render_template("step-by-step.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@epchar.route("/Step-by-Step/Edit", methods=["GET", "POST"])
@login_required
def editStepByStep():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot edit rulesets that are not your own.")
        else:
            text = request.form.get("text")
            if(len(text) > 65534):
                flash("Text must be fewer than 65535 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                cruleset.step_by_step_characters = text
                db.session.commit()
                print(cruleset.step_by_step_characters)
                flash("Change saved")
                return(redirect(url_for("epchar.stepByStep")))
    return(render_template("edit-step-by-step.html", user=current_user, frulesets = frulesets, cruleset = cruleset, adminrulesets=adminrulesets))