from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify, send_file
from .models import *
from flask_login import current_user, login_required
from .postformschar import *
from .uservalidation import *
from . import db
import json, io

epchar = Blueprint('epchar', __name__)

# character root endpoints
# redirect no subdomain
@epchar.route("/")
def noRulesetChar():
    return(noRuleset(current_user, "epmain.home"))
# subdomain
@epchar.route("/", subdomain="<ruleset>")
def char(ruleset):
    return(redirect(url_for("epmain.home", ruleset=ruleset)))

# races endpoints
# redirect no subdomain
@epchar.route("/Races")
def noRulesetRaces():
    return(noRuleset(current_user, "epchar.races"))
# subdomain
@epchar.route("/Races", subdomain="<ruleset>")
def races(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    races = Race.query.filter_by(rulesetid=cruleset.id).order_by(Race.name)
    ability_scores = AbilityScore.query.filter_by(rulesetid = cruleset.id).order_by(AbilityScore.order)
    return(
        render_template(
            "races.html", 
            user=current_user, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Races",
            races=races,
            ability_scores = ability_scores
        )
    )

# create races endpoint
@epchar.route("/Races/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createRace(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to create race; return result of creation function
    if(request.method == "POST"):
        return(makeRace(request, cruleset, None, "create"))
    # else display race creation page
    return(
        render_template(
            "create-race.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Race"
        )
    )

# race duplication endpoint
@epchar.route("/Races/Duplicate/<string:race>", subdomain="<ruleset>")
@login_required
def duplicateRace(race, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    race = Race.query.filter_by(rulesetid=cruleset.id, name=race).first_or_404()
    return(makeRace(request, cruleset, race, "duplicate"))

# race edit endpoint
@epchar.route("/Races/Edit/<string:race>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editRace(race, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    target_race = Race.query.filter_by(name=race, rulesetid=cruleset.id).first_or_404()
    # if post request, attempt to edit race; return result of edit function
    if(request.method == "POST"):
        result = makeRace(request, cruleset, target_race, "edit")
        if(result != False):
            return(result)
    # else display race edit page (altered version of creation page)
    return(
        render_template(
            "create-race.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {target_race.name}",
            race=target_race
        )
    )

# race deletion endpoint
@epchar.route("/Races/Delete/<string:race>", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def deleteRace(race, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    race = Race.query.filter_by(rulesetid=cruleset.id, name=race).first_or_404()
    # if user does not own ruleset, deny access and redirect
    if(current_user.id != cruleset.userid):
        flash("You cannot delete races in rulesets that are not yours.", "red")
        return(redirect(url_for("epchar.races", ruleset=ruleset)))
    # if post request, delete race, race features, subraces, subrace features, redirect
    if(request.method == "POST"):
        for feature in race.race_features:
            db.session.delete(feature)
        for subrace in race.subraces:
            for feature in subrace.subrace_features:
                db.session.delete(feature)
            db.session.delete(subrace)
        db.session.delete(race)
        db.session.commit()
        flash("Race deleted.", "orange")
        return(redirect(url_for("epchar.races", ruleset=ruleset)))
    # else return race deletion confirmation page
    return(
        render_template(
            "delete-race.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title = f"Delete {race.name}?",
            race = race
        )
    )

# race import endpoint
@epchar.route("/Races/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importRaces(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to import races, return result of import function
    if(request.method == "POST"):
        races = json.loads(request.form.get("parsed"))
        return(raceImporter(races, cruleset))
    # else return race import page
    return(
        render_template(
            "import-race.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Import Races",
        )
    )

# race export endpoint
@epchar.route("/Races/Export/", subdomain="<ruleset>")
def exportRaces(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # get list of dict version of every race object in current ruleset
    races = [race.to_dict() for race in cruleset.races]
    # convert to json
    json_data = json.dumps(races)

    # allocate memory
    mem = io.BytesIO()
    # write json data to memory
    mem.write(json_data.encode('utf-8'))
    # navigate to start of allocated memory (im not actually 100% sure; I don't really do memory management lol)
    mem.seek(0)

    # return file
    return(
        send_file(
            mem, 
            download_name="races.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

# race view endpint
# redirect no subdomain
@epchar.route("/Races/<string:race>")
def noRulesetRace(race):
    return(noRuleset(current_user, "epchar.race"))
# subdomain
@epchar.route("/Race/<string:race>", subdomain="<ruleset>")
def race(race, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    display = Race.query.filter_by(rulesetid=cruleset.id, name=race).first()
    return(
        render_template(
            "race.html", 
            cruleset=cruleset, 
            race=display, 
            adminrulesets=adminrulesets, 
            title=race
        )
    )

# backgrounds endpoint
# redirect no subdomain
@epchar.route("/Backgrounds")
def noRulesetBackgrounds():
    return(noRuleset(current_user, "epchar.backgrounds"))
# subdomain
@epchar.route("/Backgrounds", subdomain="<ruleset>")
def backgrounds(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "backgrounds.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Backgrounds"
        )
    )

# backgrounds creation endpoint
@epchar.route("/Backgrounds/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createBackground(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to create new background; return result of creation function
    if(request.method == "POST"):
        return(makebackground(request, cruleset, None, "create"))
    # else gather all tools that players can have proficiency with in current ruleset
    tools = []
    for tool in Item.query.filter_by(rulesetid = cruleset.id, proficiency = True):
        tools.append(tool)
    # then return background creation page, passing tools as an argument to be appended to a dropdown menu
    return(
        render_template(
            "create-background.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            tools=tools, 
            title="Create a Background"
        )
    )

# background duplication endpoint
@epchar.route("/Backgrounds/Duplicate/<string:background>", subdomain="<ruleset>")
@login_required
def duplicateBackground(background, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    background = Background.query.filter_by(rulesetid = cruleset.id, name=background).first_or_404()
    return(makebackground(request, cruleset, background, "duplicate"))

# background edit endpoint
@epchar.route("/Backgrounds/Edit/<string:background>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editBackground(background, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    background = Background.query.filter_by(rulesetid = cruleset.id, name=background).first_or_404()
    # if post request, attempt to edit background; return result of edit function
    if(request.method == "POST"):
        return(makebackground(request, cruleset, background, "edit"))
    # else gather all tools that players can have proficiency with in current ruleset
    tools = []
    for tool in Item.query.filter_by(rulesetid = cruleset.id, proficiency = True):
        tools.append(tool)
    # then return background edit page (modified creation page)
    return(
        render_template(
            "create-background.html",
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            tools=tools, 
            title=f"Edit {background.name}",
            background=background
        )
    )

# background deletion endpoint
@epchar.route("/Backgrounds/Delete/<string:background>", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def deleteBackground(background, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    background = Background.query.filter_by(rulesetid = cruleset.id, name=background).first_or_404()
    # if user does not own ruleset, deny access and redirect
    if(current_user.id != cruleset.userid):
        flash("You cannot delete backgrounds in rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.backgrounds", ruleset=ruleset)))
    # if post requestm delete background features and background; redirect
    if(request.method == "POST"):
        for feature in background.background_features:
            db.session.delete(feature)
        db.session.delete(background)
        db.session.commit()
        flash("Background deleted.", "orange")
        return(redirect(url_for("epchar.backgrounds", ruleset=ruleset)))
    # else return deletion confirmation screen
    return(
        render_template(
            "delete-background.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title = f"Delete {background.name}?",
            background = background
        )
    )

# background import endpoint
@epchar.route("/Backgrounds/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importBackgrounds(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to import backgrounds; return result of import function
    if(request.method=="POST"):
        return(backgroundImporter(json.loads(request.form.get("parsed_features")), json.loads(request.form.get("parsed_flavor")), cruleset))
    # else return import page
    return(
        render_template(
            "import-background.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Import Backgrounds",
            textone="Background Features (backgrounds.js)",
            texttwo="Background Flavor Text (fluff-backgrounds.js)"
        )
    )

# background export endpoint
@epchar.route("/Backgrounds/Export/", subdomain="<ruleset>")
def exportBackgrounds(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # get list of dict versions of all background objects in current ruleset
    backgrounds = [background.to_dict() for background in cruleset.backgrounds]
    # convert to json
    json_data = json.dumps(backgrounds)

    # write to memory
    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    # return file
    return(
        send_file(
            mem, 
            download_name="backgrounds.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

# background view endpoints
# redirect no subdomain
@epchar.route("/Background/<string:background>")
def noRulesetBackground(background):
    return(noRuleset(current_user, "epmain.background", background=background))
# subdomain
@epchar.route("/Background/<string:background>", subdomain="<ruleset>")
def background(background, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    background = Background.query.filter_by(rulesetid = cruleset.id, name = background).first_or_404()
    return(
        render_template(
            "background.html", 
            cruleset=cruleset, 
            background=background, 
            adminrulesets=adminrulesets, 
            title=background.name
        )
    )

# feats endpoints
# redirect no subdomain
@epchar.route("/Feats")
def noRulesetFeats():
    return(noRuleset(current_user, "epmain.feats"))
# subdomain
@epchar.route("/Feats", subdomain="<ruleset>")
def feats(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "feats.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Feats"
        )
    )

# feat creation endpoint
@epchar.route("/Feats/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createFeat(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to create feat; return result of creation function
    if(request.method == "POST"):
        return(makefeat(request, cruleset, None, "create"))
    # else return feat creation page
    return(
        render_template(
            "create-feat.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Create a Feat"
        )
    )

# feat duplication endpoint
@epchar.route("/Feats/Duplicate/<string:feat>", subdomain="<ruleset>")
@login_required
def duplicateFeat(feat, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    feat = Feat.query.filter_by(rulesetid=cruleset.id, name=feat).first_or_404()
    if(current_user.id != cruleset.userid):
        return(makefeat(None, cruleset, feat, "duplicate"))
    return(redirect(url_for("epchar.feats", ruleset=ruleset)))

# feat edit endpoint
@epchar.route("/Feats/Edit/<string:feat>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editFeat(feat, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    feat = Feat.query.filter_by(rulesetid=cruleset.id, name=feat).first_or_404()
    # if post request, attempt to edit feat; return result of edit function
    if(request.method == "POST"):
        return(makefeat(request, cruleset, feat, "edit"))
    # else return feat edit page
    return(
        render_template(
            "create-feat.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title=f"Edit {feat.name}",
            feat=feat
        )
    )

# feat deletion endpoint
@epchar.route("/Feats/Delete/<string:feat>", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def deleteFeat(feat, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    feat = Feat.query.filter_by(rulesetid = cruleset.id, name = feat).first_or_404()
    # if user does not own current ruleset, deny access and redirect
    if(current_user.id != cruleset.userid):
        flash("You cannot delete feats in rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.feats", ruleset=ruleset)))
    # if post request, delete feat
    if(request.method == "POST"):
        db.session.delete(feat)
        db.session.commit()
        flash("Feat deleted.", "orange")
        return(redirect(url_for("epchar.feats", ruleset=ruleset)))
    # else return deletion confirmation page
    return(
        render_template(
            "delete-feat.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title=f"Delete {feat.name}?",
            feat=feat
        )
    )

# feat import endpoint
@epchar.route("/Feats/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importFeats(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to import feats; return result of import function
    if(request.method=="POST"):
        return(featImporter(json.loads(request.form.get("parsed")), cruleset))
    # else return import page
    return(
        render_template(
            "import-feat.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Import Feats",
            text="Feats (feats.json)"
        )
    )

# feat export endpoint
@epchar.route("/Feats/Export/", subdomain="<ruleset>")
def exportFeats(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # get list of dict version of feat objects in current ruleset
    feats = [feat.to_dict() for feat in cruleset.feats]
    # convert to json
    json_data = json.dumps(feats)

    # write to memory
    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    # return file
    return(
        send_file(
            mem, 
            download_name="feats.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

# feat view endpoints
# redirect no subdomain
@epchar.route("/Feat/<string:feat>")
def noRulesetFeat(feat):
    return(noRuleset(current_user, "epchar.feat", feat=feat))
# subdomain
@epchar.route("/Feat/<string:feat>", subdomain="<ruleset>")
def feat(feat, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    feat = Feat.query.filter_by(rulesetid = cruleset.id, name = feat).first_or_404()
    return(
        render_template(
            "feat.html", 
            cruleset=cruleset, 
            feat=feat, 
            adminrulesets=adminrulesets, 
            title=feat.name
        )
    )

# ability score endpoints
# redirect no subdomain
@epchar.route("/Ability-Scores")
def noRulesetAbilityScores():
    return(noRuleset(current_user, "epchar.stats"))
# subdomain
@epchar.route("/Ability-Scores", subdomain="<ruleset>")
def stats(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    scores = AbilityScore.query.filter_by(rulesetid=cruleset.id).order_by(AbilityScore.order)
    return(
        render_template(
            "stats.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            scores=scores,
            title="Ability Scores"
        )
    )

# ability score creation endpoint
@epchar.route("/Ability-Scores/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createStat(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to create new ability score; return result of creation function
    if(request.method=="POST"):
        return(abilityScore(request, cruleset, None, "create"))
    # else return ability score creation page
    return(
        render_template(
            "create-stat.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Create an Ability Score"
        )
    )

# ability score edit endpoint
@epchar.route("/Ability-Scores/Edit/<string:score>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editStat(score, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score).first_or_404()
    # if post request, attempt to edit ability score; return result of creation function
    if(request.method=="POST"):
        result = abilityScore(request, cruleset, ability_score, "edit")
        if(result != False):
            return(result)
    # else return ability score edit page
    return(
        render_template(
            "create-stat.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Create an Ability Score",
            score=ability_score
        )
    )

# ability score duplication endpoint
@epchar.route("/Ability-Scores/Duplicate/<string:score>", subdomain="<ruleset>")
@login_required
def duplicateStat(score, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score).first_or_404()
    return(abilityScore(None, cruleset, ability_score, "duplicate"))

# ability score deletion endpoint
@epchar.route("/Ability-Scores/Delete/<string:score>", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def deleteStat(score, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score).first_or_404()
    # if user does not own current ruleset, deny access and redirect
    if(current_user.id != cruleset.userid):
        flash("You cannot delete Ability Scores in rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.stats", ruleset=ruleset)))
    # if post request, delete ability score
    if(request.method == "POST"):
        db.session.delete(ability_score)
        db.session.commit()
        flash("Ability Score deleted.", "orange")
    # else return ability score deletion confirmation page
    return(
        render_template(
            "delete-stat.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title = f"Delete {ability_score.name}?",
            ability_score = ability_score
        )
    )

# ability score import endpoint
@epchar.route("/Ability-Scores/Import", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def importStats(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to import ability scores; return result of import function
    if(request.method == "POST"):
        ability_scores = json.loads(request.form.get("parsed"))
        return(abilityScoreImporter(ability_scores, cruleset))
    # else return ability score import page
    return(
        render_template(
            "import-stat.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Ability Scores",
        )
    )

# ability score export endpoint
@epchar.route("/Ability-Scores/Export", subdomain="<ruleset>")
def exportStats(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # get list of dict version of ability score objects in current ruleset
    stats = [stat.to_dict() for stat in cruleset.ability_scores]
    # convert to json
    json_data = json.dumps(stats)

    # write to memory
    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    # return file
    return(
        send_file(
            mem, 
            download_name="ability-scores.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

# class endpoints
# redirect no subdomain
@epchar.route("/Classes")
def noRulesetClasses():
    return(noRuleset(current_user, "epchar.classes"))
# subdomain
@epchar.route("/Classes", subdomain="<ruleset>")
def classes(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "classes.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Classes"
        )
    )

# create class endpoint
@epchar.route("/Classes/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createClass(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to create class; return result of creation function
    if(request.method == "POST"):
        return(makeclass(request, cruleset, None, "create", adminrulesets))
    # else return class creation page
    return(
        render_template(
            "create-class.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Create a Class",
        )
    )

# class duplication endpoint
@epchar.route("/Classes/Duplicate/<string:tclass>", subdomain="<ruleset>")
@login_required
def duplicateClass(tclass, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tclass = Class.query.filter_by(rulesetid=cruleset.id, name=tclass).first_or_404()
    return(makeclass(None, cruleset, tclass, "duplicate"))

# class edit endpoint
@epchar.route("/Classes/Edit/<string:tclass>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editClass(tclass, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tclass = Playerclass.query.filter_by(rulesetid=cruleset.id, name=tclass).first_or_404()
    # if post request, attempt to edit class; return result of edit function
    if(request.method == "POST"):
        return(makeclass(request, cruleset, tclass, "edit"))
    # else return class edit page
    return(
        render_template(
            "create-class.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title=f"Edit {tclass.name}",
            tclass=tclass
        )
    )

# class delete endpoint
@epchar.route("/Classes/Delete/<string:tclass>", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def deleteClass(tclass):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tclass = Playerclass.query.filter_by(rulesetid=cruleset.id, name=tclass).first_or_404()
    # if current user doesn't own current ruleset, deny access and redirect
    if(current_user.id != cruleset.userid):
        flash("You cannot delete Ability Scores in rulesets that are not your own", "red")
        return(redirect(url_for("epchar.stats", ruleset=ruleset)))
    # if post request, delete class, class features, class columns, subclasses, subclass features, class columns
    if(request.method == "POST"):
        for feature in tclass.class_features:
            db.session.delete(feature)
        for column in tclass.columns:
            db.session.delete(column)
        for subclass in tclass.subclasses:
            for feature in subclass.subclass_features:
                db.session.delete(feature)
            for column in subclass.columns:
                db.session.delete(column)
            db.session.delete(subclass)
        db.session.delete(tclass)
        db.session.commit()
        flash("Class deleted.", "orange")
    # else return class deletion confirmation page
    return(
        render_template(
            "delete-class.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title = f"Delete {tclass.name}?",
            tclass = tclass
        )
    )

# class import endpoint
@epchar.route("/Classes/Import", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def importClasses(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # if post request, attempt to import classes; return result of creation function
    if(request.method == "POST"):
        tclass = json.loads(request.form.get("parsed"))
        return(classImporter(tclass, cruleset))
    # else return class import page
    return(
        render_template(
            "import-class.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Class",
        )
    )
# class view endpoints
# redirect no subdomain
@epchar.route("/Class/<string:selectedclass>")
def noRulesetClassPage(selectedclass):
    return(noRuleset(current_user, "epchar.classPage", selectedclass=selectedclass))
# subdomain
@epchar.route("/Class/<string:selectedclass>", subdomain="<ruleset>")
def classPage(selectedclass, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    selectedclass = Playerclass.query.filter_by(rulesetid=cruleset.id, name=selectedclass).first_or_404()
    return(
        render_template(
            "class.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title=selectedclass.name + " Class",
            playerclass=selectedclass
        )
    )
# class export endpoint
@epchar.route("/Classes/Export/", subdomain="<ruleset>")
def exportClasses(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # get list of dict version of class objects in current ruleset
    classes = [playerclass.to_dict() for playerclass in cruleset.classes]
    # convert to json
    json_data = json.dumps(classes)

    # write to memory
    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    # return file
    return(
        send_file(
            mem, 
            download_name="classes.json",
            mimetype="application/json",
            as_attachment=True
        )
    )
