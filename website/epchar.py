from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature, Background, BackgroundFeature, Feat, Item, Playerclass, AbilityScore
from flask_login import current_user, login_required
from .check_ruleset import *
from . import db
import json

epchar = Blueprint('epchar', __name__)


## CHARACTERS
@epchar.route("/")
def char():
    return(redirect(url_for("epmain.home")))

@epchar.route("/Races")
def races():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "races.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            ability='', 
            adminrulesets=adminrulesets, 
            title="Races"
        )
    )

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
            name = request.form.get("name")
            asis = request.form.getlist("asi")
            asi_override = request.form.get("asi_override")
            if(asi_override):
                asis = None
                asi_text = request.form.get("asi_text")
            else:
                # asis = request.form.getlist("asi")
                asi_text = None
            sizelib = [
                "Tiny", 
                "Small", 
                "Medium", 
                "Large", 
                "Huge", 
                "Gargantuan"
            ]
            size_override = request.form.get("size_override")
            if(size_override):
                size = None
                size_text = request.form.get("size_text")
            else:
                size = int(request.form.get("size"))
                size_text = None
            base_height = request.form.get("base_height")
            height_num = request.form.get("height_num")
            height_die = request.form.get("height_die")
            base_weight = request.form.get("base_weight")
            weight_num = request.form.get("weight_num")
            weight_die = request.form.get("weight_die")
            walk = request.form.get("walk")
            swim = request.form.get("swim")
            climb = request.form.get("climb")
            fly = request.form.get("fly")
            burrow = request.form.get("burrow")
            flavor = request.form.get("text")
            features = request.form.getlist("feature_name")
            feature_text = request.form.getlist("feature_text")
            has_subraces = request.form.get("has_subraces")
            if(has_subraces):
                subraces = []
                subrace_flavor = request.form.get("subrace_flavor")
                print(request.form.getlist("subrace_text"))
                for i, subrace in enumerate(request.form.getlist("subrace_name")):
                    subraces[i] = {
                        "name": subrace,
                        "text": request.form.getlist("subrace_text")[i],
                        "features": []
                    }
                    for i, feature in enumerate(request.form.getlist(f"{subrace}_feature_name")):
                        subraces[i]["features"].append({
                            "name": feature,
                            "text": request.form.getlist(f"{subrace}_feature_text")[i]
                        })
            else:
                subraces = None
                subrace_flavor = None
            if(len(name) < 1):
                flash("You must specify a race name.")
            elif(len(name) > 127):
                flash("Race name must be fewer than 128 characters.")
            elif(len(flavor) > 16383):
                flash("Race description must be fewer than 16384 characters.")
            elif("<" in flavor):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in flavor):
                flash("Cross-site scripting attacks are not allowed.")
            elif("-" in name):
                flash("Dashes (\"-\") are not allowed in race name.")
            for feature in features:
                if(len(feature) < 1):
                    flash("Each racial feature must have a name.")
                elif(len(feature) > 127):
                    flash("Racial feature names must be fewer than 128 characters.")
            for ftext in feature_text:
                if(len(ftext) > 16383):
                    flash("Racial feature text must be fewer than 16384 characters.")
                elif("<" in ftext):
                    flash("Open angle brackets (\"<\") are not allowed.")
                elif("javascript" in ftext):
                    flash("Cross-site scripting attacks are not allowed.")
            if(has_subraces):
                for subrace in subraces:
                    if(len(subrace["name"]) < 1):
                        flash("You must specify a name for each subrace.")
                    elif(len(subrace["name"]) > 127):
                        flash("Subrace names must be fewer than 128 characters.")
                    elif(len(subrace["text"]) > 16383):
                        flash("Subrace descriptions must be fewer than 16384 characters.")
                    elif("<" in subrace["text"]):
                        flash("Open angle brackets (\"<\") are not allowed.")
                    elif("javascript" in feature["text"]):
                        flash("Cross-site scripting attacks are not allowed.")
                    for feature in subrace["features"]:
                        if(len(feature["name"]) < 1):
                            flash("You must specify a name for each subrace features.")
                        elif(len(feature["name"]) > 127):
                            flash("Subrace feature names must be fewer than 128 characters.")
                        elif(len(feature["text"]) > 16383):
                            flash("Subrace feature text must be fewer than 16384 characters.")
                        elif("<" in feature["text"]):
                            flash("Open angle brackets (\"<\") are not allowed.")
                        elif("javascript" in feature["text"]):
                            flash("Cross-site scripting attacks are not allowed.")
            print(name)
            new_race = Race(
                rulesetid = cruleset.id,
                name = name,
                flavor = flavor,
                asis = asis,
                asi_text = asi_text,
                size = size,
                size_text = size_text,
                walk = walk,
                swim = swim,
                fly = fly,
                burrow = burrow,
                base_height = base_height,
                height_num = height_num,
                height_die = height_die,
                base_weight = base_weight,
                weight_num = weight_num,
                weight_die = weight_die,
                subrace_flavor = subrace_flavor
            )
            db.session.add(new_race)
            db.session.commit()
            new_race = Race.query.filter_by(
                name = name, 
                rulesetid = cruleset.id
            ).first()
            for i, feature in enumerate(features):
                new_feature = RaceFeature(
                    raceid = new_race.id,
                    name = feature,
                    text = feature_text[i]
                )
                db.session.add(new_feature)
            db.session.commit()
            if(has_subraces):
                for subrace in subraces:
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
            flash("Race created!")
            return(redirect(url_for("epchar.races")))
    return(
        render_template(
            "create-race.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Race"
        )
    )

@epchar.route("/Race/<string:race>")
def race(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    display = Race.query.filter_by(rulesetid=cruleset.id, name=race).first()
    return(
        render_template(
            "race.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            race=display, 
            adminrulesets=adminrulesets, 
            title=race
        )
    )

@epchar.route("/Backgrounds")
def backgrounds():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "backgrounds.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Backgrounds"
        )
    )

@epchar.route("/Backgrounds/Create", methods=["GET", "POST"])
@login_required
def createBackground():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tools = []
    for tool in Item.query.filter_by(rulesetid = cruleset.id, proficiency = True):
        tools.append(tool)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create backgrounds for a ruleset that is not your own.")
            return("1")
        else:
            name = request.form.get("name")
            skills = request.form.getlist("skill")
            tools = request.form.getlist("tool")
            languages = request.form.get("language")
            items = request.form.getlist("item")
            text = request.form.get("text")
            featurenames = request.form.getlist("featurename")
            featuretexts = request.form.getlist("featuretext")
            if(len("name") < 1):
                flash("You must specify a background name.")
            elif(len("name") > 127):
                flash("Background name must be fewer than 128 characters.")
            elif(len("text") > 16383):
                flash("Text must be fewer than 16384 characters.")
            elif("-" in "name"):
                flash("Dashes (\"-\") are not allowed in the background name.")
            elif("<" in "text"):
                flash("Open angle brackets(\"<\") are not allowed.")
            elif("javascript" in "text"):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                for index, feature in enumerate(featurenames):
                    if(len(feature) < 1):
                        flash("You must specify a feature name.")
                    elif(len(feature) > 127):
                        flash("Feature name must be fewer than 128 characters.")
                    elif(len(featuretexts[index]) > 16383):
                        flash("Text must be fewer than 16383 characters.")
                    elif("<" in featuretexts[index]):
                        flash("Open angle brackets(\"<\") are not allowed.")
                    elif("javascript" in featuretexts[index]):
                        flash("Cross-site scripting attacks are not allowed.")
                new_background = Background(
                    rulesetid = cruleset.id,
                    name = name,
                    skills = skills,
                    tools = tools,
                    languages = languages,
                    equipment = items,
                    text = text
                )
                db.session.add(new_background)
                db.session.commit()

                new_background = Background.query.filter_by(
                    name = name,
                    rulesetid = cruleset.id
                ).first()
                for index, feature in enumerate(featurenames):
                    new_feature = BackgroundFeature(
                        backgroundid = new_background.id,
                        name = feature,
                        text = featuretexts[index]
                    )
                    db.session.add(new_feature)
                db.session.commit()
                flash("Background created!")
    return(
        render_template(
            "create-background.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            tools=tools, 
            title="Create a Background"
        )
    )

@epchar.route("/Background/<string:background>")
def background(background):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    background = Background.query.filter_by(rulesetid = cruleset.id, name = background.replace("-", " ")).first()
    return(
        render_template(
            "background.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            background=background, 
            adminrulesets=adminrulesets, 
            title=background.name
        )
    )

@epchar.route("/Feats")
def feats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "feats.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Feats"
        )
    )

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
            text = request.form.get("text")
            prereq = request.form.get("prereq")
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
                new_feat = Feat(
                    rulesetid = cruleset.id,
                    name = name,
                    prerequisite = prereq,
                    text = text
                )
                db.session.add(new_feat)
                db.session.commit()
                flash("Feat created!")
                return(redirect(url_for("epchar.feats")))
    return(render_template("create-feat.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets, title="Create a Feat"))

@epchar.route("/Feat/<string:feat>")
def feat(feat):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    feat = Feat.query.filter_by(rulesetid = cruleset.id, name = feat.replace("-", " ")).first()
    return(
        render_template(
            "feat.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            feat=feat, 
            adminrulesets=adminrulesets, 
            title=feat.name
        )
    )

@epchar.route("/Ability-Scores")
def stats():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "stats.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Ability Scores"
        )
    )

@epchar.route("/Ability-Scores/Create", methods=["GET", "POST"])
def createStat():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        name = request.form.get("name")
        abbr = request.form.get("abbr")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify an Ability Score name.")
        elif(len(name) > 127):
            flash("Ability Score name must be fewer than 128 characters.")
        elif(len(abbr) != 3):
            flash("Ability Score abbreviation must be 3 characters.")
        elif(len(text) > 16383):
            flash("Ability Score description must be fewer than 16384 characters.")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.")
        else:
            new_ability_score = AbilityScore(
                rulesetid = cruleset.id,
                name = name,
                abbr = abbr,
                text = text
            )
            db.session.add(new_ability_score)
            db.session.commit()
            flash("Ability Score created!")
            return(redirect(url_for("epchar.stats")))
    return(
        render_template(
            "create-stat.html",
            user=current_user,
            frulesets=frulesets,
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Create an Ability Score"
        )
    )

@epchar.route("/Classes")
def classes():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "classes.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Classes"
        )
    )

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
    return(
        render_template(
            "create-class.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Create a Class"
        )
    )