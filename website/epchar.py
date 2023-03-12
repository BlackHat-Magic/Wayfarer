from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature, Background, BackgroundFeature, Feat, Item, Playerclass, AbilityScore, ClassColumn, SubclassColumn, ClassFeature, Playerclass, Subclass, SubclassFeature
from flask_login import current_user, login_required
from .check_ruleset import *
from .postformschar import *
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
    races = Race.query.filter_by(rulesetid=cruleset.id).order_by(Race.name)
    return(
        render_template(
            "races.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            ability='', 
            adminrulesets=adminrulesets, 
            title="Races",
            races=races
        )
    )

@epchar.route("/Races/Create", methods=["GET", "POST"])
@login_required
def createRace():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        result = makerace(request, cruleset, None, "create")
        if(result != False):
            return(result)
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

@epchar.route("/Races/Duplicate/<string:race>")
@login_required
def duplicateRace(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    race = Race.query.filter_by(rulesetid=cruleset.id, name=race.replace("-", " ")).first()
    if(not race):
        flash("Race does not exist.", "red")
        return(redirect(url_for("epchar.races")))
    result = makerace(request, cruleset, race, "duplicate")
    return(result)

@epchar.route("/Races/Edit/<string:race>", methods=["GET", "POST"])
@login_required
def editRace(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    target_race = Race.query.filter_by(name=race.replace("-", " "), rulesetid=cruleset.id).first()
    if(not target_race):
        flash("Race does not exist.", "red")
    elif(request.method == "POST"):
        result = makerace(request, cruleset, target_race, "edit")
        if(result != False):
            return(result)
    return(
        render_template(
            "create-race.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Race",
            race=target_race
        )
    )

@epchar.route("/Races/Delete/<string:race>")
@login_required
def deleteRace(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    race = Race.query.filter_by(rulesetid=cruleset.id, name=race.replace("-", " ")).first()
    if(not race):
        flash("Race does not exist.", "red")
    elif(current_user.id != cruleset.userid):
        flash("You cannot delete races in rulesets that are not yours.", "red")
    else:
        for feature in race.race_features:
            db.session.delete(feature)
        for subrace in race.subraces:
            for feature in subrace.subrace_features:
                db.session.delete(feature)
            db.session.delete(subrace)
        db.session.delete(race)
        db.session.commit()
        flash("Race deleted.", "orange")
    return(redirect(url_for("epchar.races")))

@epchar.route("/Race/<string:race>")
def race(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    display = Race.query.filter_by(rulesetid=cruleset.id, name=race.replace("-", " ")).first()
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
                flash("You must specify a background name.", "red")
            elif(len("name") > 127):
                flash("Background name must be fewer than 128 characters.", "red")
            elif(len("text") > 16383):
                flash("Text must be fewer than 16384 characters.", "red")
            elif("-" in "name"):
                flash("Dashes (\"-\") are not allowed in the background name.", "red")
            elif("<" in "text"):
                flash("Open angle brackets(\"<\") are not allowed.", "red")
            elif("javascript" in "text"):
                flash("Cross-site scripting attacks are not allowed.", "red")
            else:
                for index, feature in enumerate(featurenames):
                    if(len(feature) < 1):
                        flash("You must specify a feature name.", "red")
                    elif(len(feature) > 127):
                        flash("Feature name must be fewer than 128 characters.", "red")
                    elif(len(featuretexts[index]) > 16383):
                        flash("Text must be fewer than 16383 characters.", "red")
                    elif("<" in featuretexts[index]):
                        flash("Open angle brackets(\"<\") are not allowed.", "red")
                    elif("javascript" in featuretexts[index]):
                        flash("Cross-site scripting attacks are not allowed.", "red")
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
                flash("Background created!", "green")
                return(redirect(url_for("epchar.backgrounds")))
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
                flash("You must specify a feat name.", "red")
            elif(len(name) > 127):
                flash("Feat name must be fewer than 128 characters.", "red")
            elif(len(prereq) > 255):
                flash("Feat Prerequisite must be fewer than 256 characters.", "red")
            elif(len(text) > 16383):
                flash("Feat description must be fewer than 16384 characters.", "red")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.", "red")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.", "red")
            else:
                new_feat = Feat(
                    rulesetid = cruleset.id,
                    name = name,
                    prerequisite = prereq,
                    text = text
                )
                db.session.add(new_feat)
                db.session.commit()
                flash("Feat created!", "green")
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
    scores = AbilityScore.query.filter_by(rulesetid=cruleset.id).order_by(AbilityScore.order)
    return(
        render_template(
            "stats.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            scores=scores,
            title="Ability Scores"
        )
    )

@epchar.route("/Ability-Scores/Create", methods=["GET", "POST"])
@login_required
def createStat():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method=="POST"):
        result = abilityScore(request, cruleset, None)
        if(result != False):
            return(result)
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

@epchar.route("/Ability-Scores/Edit/<string:score>", methods=["GET", "POST"])
@login_required
def editStat(score):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score.replace("-", " ")).first()
    if(not ability_score):
        flash("Ability Score does not exist.", "red")
        return(redirect(url_for("epchar.stats")))
    elif(request.method=="POST"):
        result = abilityScore(request, cruleset, ability_score, "edit")
        if(result != False):
            return(result)
    return(
        render_template(
            "create-stat.html",
            user=current_user,
            frulesets=frulesets,
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Create an Ability Score",
            score=ability_score
        )
    )

@epchar.route("/Ability-Scores/Duplicate/<string:score>")
@login_required
def duplicateStat(score):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score.replace("-", " ")).first()
    if(not ability_score):
        flash("Ability Score does not exist.", "red")
    else:
        result = abilityScore(None, cruleset, ability_score, "duplicate")
        return(result)

@epchar.route("/Ability-Scores/Delete/<string:score>")
@login_required
def deleteStat(score):
    cruleset = getCurrentRuleset(current_user)
    if(current_user.id != cruleset.userid):
        flash("You cannot delete Ability Scores in rulesets that are not your own.", "red")
    else:
        ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score.replace("-", " ")).first()
        if(not ability_score):
            flash("Ability Score does not exist.", "red")
        else:
            db.session.delete(ability_score)
            db.session.commit()
            flash("Ability Score deleted.", "orange")
    return(redirect(url_for("epchar.stats")))

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
            flash("You cannot create classes for rulesets that are not yours.", "red")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            hitdie = request.form.get("hitdie")
            proficiencies = request.form.getlist("proficiency")
            skills = request.form.getlist("skill")
            saves = request.form.getlist("save")
            for i in range(len(saves)):
                if(saves[i] == "true"):
                    saves[i] = True
                else:
                    saves[i] = False
            print(saves)
            equipment = request.form.get("equipment")
            gold_nums = request.form.get("gold_nums")
            try:
                gold_nums = int(gold_nums)
            except:
                flash("Number of dice rolled for starting gold must be a number.", "red")
            gold_dice = request.form.get("gold_dice")
            gold_mult = request.form.get("gold_mult")
            try:
                gold_mult = int(gold_mult)
            except:
                flash("Starting gold multiplier must be a number.", "red")
            multiclass_prereq = request.form.get("prereq")
            multiclass_profic = request.form.getlist("multiprofic")
            subclass_name = request.form.get("subclass_name")
            subclass_level = int(request.form.get("subclasslevel"))
            levels = request.form.get("levels")
            try:
                levels = int(levels)
            except:
                flash("Max level must be a number.", "red")
            if(len(name) < 1):
                flash("You must specify a class name.", "red")
            elif(len(name) > 127):
                flash("Class name must be fewer than 128 characters.", "red")
            elif(len(text) > 16383):
                flash("Class description must be fewer than 16383 characters.", "red")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.", "red")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.", "red")
            elif(len(equipment) > 1023):
                flash("Class equipment must be fewer than 1024 characters.", "red")
            elif(len(multiclass_prereq) > 1023):
                flash("Multiclassing prerequisites must be fewer than 1024 characters.", "red")
            elif("<" in multiclass_prereq):
                flash("Open angle brackets (\"<\") are not allowed.", "red")
            elif("javascript" in multiclass_prereq):
                flash("Cross-site scripting attacks are not allowed.", "red")
            elif(len(subclass_name) > 127):
                flash("Subclass title must be fewer than 128 characters.", "red")
            else:
                bad = False
                for i, column in enumerate(request.form.getlist("columnname")):
                    if(bad):
                        break
                    if(len(column) < 1):
                        bad = True
                        flash("Each custom column must have a name.", "red")
                    elif(len(column) > 127):
                        bad = True
                        flash("Custom column names must be fewer than 128 characters.", "red")
                    for value in request.form.getlist(f"column{i}value"):
                        if(bad):
                            break
                        elif(len(value) > 127):
                            bad = True
                            flash("Custom column values must be fewer than 128 characters.", "red")
                for i, feature in enumerate(request.form.getlist("class_feature_name")):
                    if(bad):
                        break
                    try:
                        testint = int(request.form.getlist("level")[i])
                    except:
                        bad = True
                        flash("Feature levels must be numbers.", "red")
                    if(len(feature) < 1):
                        bad = True
                        flash("You must specify a name for each class feature", "red")
                    elif(len(feature) > 127):
                        bad = True
                        flash("Class feature names must be fewer than 128 characters", "red")
                    elif(len(request.form.getlist("class_feature_text")[i]) > 16383):
                        bad = True
                        flash("Class feature text must be fewer than 128 characters", "red")
                    elif("<" in request.form.getlist("class_feature_text")[i]):
                        bad = True
                        flash("Open angle brackets (\"<\") are not allowed.", "red")
                    elif("javascript" in request.form.getlist("class_feature_text")[i]):
                        bad = True
                        flash("Cross-site scripting attacks are not allowed.", "red")
                for i, subclass in enumerate(request.form.getlist("subclass_name")):
                    if(bad):
                        break
                    if(len(subclass) < 1):
                        bad = True
                        flash("You must specify a name for each subclass.", "red")
                    elif(len(subclass) > 127):
                        bad = True
                        flash("Subclass names must be fewer than 128 characters.", "red")
                    elif(len(request.form.getlist("subclass_text")[i]) > 16383):
                        bad = True
                        flash("Subclass descriptions must be fewer than 16383 characters.", "red")
                    elif("<" in request.form.getlist("subclass_text")[i]):
                        bad = True
                        flash("Open angle brackets (\"<\") are not allowed.", "red")
                    elif("javascript" in request.form.getlist("subclass_text")[i]):
                        bad = True
                        flash("Cross-site scripting attacks are not allowed.", "red")
                    for j, feature in enumerate(request.form.getlist(f"subclass_{i}_feature_name")):
                        if(bad):
                            break
                        try:
                            testint = int(request.form.getlist(f"subclass_{i}_feature_level")[j])
                        except:
                            bad = True
                            flash("Subclass feature levels must be numbers.", "red")
                        if(len(feature) < 1):
                            bad = True
                            flash("You must specify a name for each subclass feature.", "red")
                        elif(len(feature) > 127):
                            bad = True
                            flash("Subclass feature names must be fewer than 128 characters.", "red")
                        elif(len(request.form.getlist(f"subclass_{i}_feature_text")[j]) > 16383):
                            bad = True
                            flash("Subclass feature descriptions must be fewer than 16383 characters.", "red")
                        elif("<" in request.form.getlist(f"subclass_{i}_feature_text")[j]):
                            bad = True
                            flash("Open angle brackets (\"<\") are not allowed.", "red")
                        elif("javascript" in request.form.getlist(f"subclass_{i}_feature_text")[j]):
                            bad = True
                            flash("Cross-site scripting attacks are not allowed.", "red")
                    for j, column in enumerate(request.form.getlist(f"subclass{i}columnname")):
                        if(bad):
                            break
                        if(len(column) < 1):
                            bad = True
                            flash("You must specify a name for each subclass' custom columns.", "red")
                        elif(len(column) > 127):
                            bad = True
                            flash("Each subclass' custom column names must be fewer than 128 characters.", "red")
                        for value in request.form.getlist(f"subclass{i}column{j}value"):
                            if(len(value) > 127):
                                bad = True
                                flash("Each subclass' custom column values must be fewer than 128 characters.", "red")

                if(not bad):
                    new_class = Playerclass(
                        rulesetid = cruleset.id,
                        name = name,
                        hitdie = hitdie,
                        proficiencies = proficiencies,
                        saves = saves,
                        equipment = equipment,
                        gold_nums = gold_nums,
                        gold_dice = gold_dice,
                        gold_mult = gold_mult,
                        multiclass_prereq = multiclass_prereq,
                        multiclass_profic = multiclass_profic,
                        subclass_name = subclass_name,
                        subclass_level = subclass_level,
                        levels = levels,
                        text = text,
                        skills = skills
                    )
                    db.session.add(new_class)
                    db.session.commit()
                    classid = Playerclass.query.filter_by(name=name, text=text, rulesetid=cruleset.id).first().id

                    for i, column in enumerate(request.form.getlist("columnname")):
                        new_column = ClassColumn(
                            classid = classid,
                            name = column,
                            data = request.form.getlist(f"column{i}value")
                        )
                        db.session.add(new_column)

                    for i, feature in enumerate(request.form.getlist("class_feature_name")):
                        new_feature = ClassFeature(
                            classid = classid,
                            level_obtained = request.form.getlist("level")[i],
                            name = feature,
                            text = request.form.getlist("class_feature_text")[i]
                        )
                        db.session.add(new_feature)
                    
                    for i, sublcass in enumerate(request.form.getlist("subclass_name")):
                        new_subclass = Subclass(
                            classid = classid,
                            name = subclass,
                            text = request.form.getlist("subclass_text")[i],
                            caster_type = request.form.getlist("castertype")[i],
                        )
                        db.session.add(new_subclass)
                        db.session.commit()
                        new_subclass = Subclass.query.filter_by(classid = classid, name = subclass).first()

                        for j, feature in enumerate(request.form.getlist(f"subclass_{i}_feature_name")):
                            new_subclass_feature = SubclassFeature(
                                subclassid = new_subclass.id,
                                level_obtained = request.form.getlist(f"subclass_{i}_feature_level")[j],
                                name = feature,
                                text = request.form.getlist(f"subclass_{i}_feature_text")[j]
                            )
                            db.session.add(new_subclass_feature)
                        for j, column in enumerate(request.form.getlist(f"subclass{i}columnname")):
                            new_subclass_column = SubclassColumn(
                                subclassid = new_subclass.id,
                                name = column,
                                data = request.form.getlist(f"subclass{i}column{j}value")
                            )
                            db.session.add(new_subclass_column)
                    db.session.commit()
                    flash("Class Created!", "green")
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

@epchar.route("/Class/<string:selectedclass>")
def classPage(selectedclass):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    selectedclass = Playerclass.query.filter_by(name=selectedclass.replace("-", " ")).first()
    return(
        render_template(
            "class.html",
            user=current_user,
            frulesets=frulesets,
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title=selectedclass.name + " Class",
            playerclass=selectedclass
        )
    )
