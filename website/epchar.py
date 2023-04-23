from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature, Background, BackgroundFeature, Feat, Item, Playerclass, AbilityScore, ClassColumn, SubclassColumn, ClassFeature, Playerclass, Subclass, SubclassFeature
from flask_login import current_user, login_required
from .check_ruleset import *
from .postformschar import *
from . import db
import json

epchar = Blueprint('epchar', __name__)

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
    race = Race.query.filter_by(rulesetid=cruleset.id, name=race).first()
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
    target_race = Race.query.filter_by(name=race, rulesetid=cruleset.id).first()
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
            title=f"Edit {target_race.name}",
            race=target_race
        )
    )

@epchar.route("/Races/Delete/<string:race>")
@login_required
def deleteRace(race):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    race = Race.query.filter_by(rulesetid=cruleset.id, name=race).first()
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
        return(makebackground(request, cruleset, None, "create"))
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

@epchar.route("/Backgrounds/Duplicate/<string:tbackground>")
@login_required
def duplicateBackground(tbackground):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tbackground = Background.query.filter_by(rulesetid = cruleset.id, name=tbackground).first()
    if(not tbackground):
        flash("Background does not exist.")
        return(redirect(url_for("epchar.backgrounds")))
    return(makebackground(request, cruleset, tbackground, "duplicate"))

@epchar.route("/Backgrounds/Edit/<string:tbackground>", methods=["GET", "POST"])
@login_required
def editBackground(tbackground):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tbackground = Background.query.filter_by(rulesetid = cruleset.id, name=tbackground).first()
    tools = []
    for tool in Item.query.filter_by(rulesetid = cruleset.id, proficiency = True):
        tools.append(tool)
    if(not tbackground):
        flash("Background does not exist.")
        return(redirect(url_for("epchar.backgrounds")))
    elif(request.method == "POST"):
        return(makebackground(request, cruleset, tbackground, "edit"))
    return(
        render_template(
            "create-background.html",
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            tools=tools, 
            title=f"Edit {tbackground.name}",
            tbackground=tbackground
        )
    )

@epchar.route("/Backgrounds/Delete/<string:tbackground>")
@login_required
def deleteBackground(tbackground):
    cruleset = getCurrentRuleset(current_user)
    tbackground = Background.query.filter_by(rulesetid = cruleset.id, name=tbackground).first()
    if(not tbackground):
        flash("Background does not exist.", "red")
    elif(current_user.id != cruleset.userid):
        flash("You cannot delete backgrounds in rulesets that are not your own.", "red")
    else:
        db.session.delete(tbackground)
        db.session.commit()
        flash("Background deleted.", "orange")
    return(redirect(url_for("epchar.backgrounds")))

@epchar.route("/Background/<string:background>")
def background(background):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    background = Background.query.filter_by(rulesetid = cruleset.id, name = background).first()
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
        return(makefeat(request, cruleset, None, "create"))
    return(
        render_template(
            "create-feat.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Create a Feat"
        )
    )

@epchar.route("/Feats/Duplicate/<string:tfeat>")
@login_required
def duplicateFeat(tfeat):
    cruleset = getCurrentRuleset(current_user)
    tfeat = Feat.query.filter_by(rulesetid=cruleset.id, name=tfeat).first()
    if(not tfeat):
        flash("Feat does not exist.", "red")
    else:
        return(makefeat(None, cruleset, tfeat, "duplicate"))
    return(redirect(url_for("epchar.feats")))

@epchar.route("/Feats/Edit/<string:tfeat>", methods=["GET", "POST"])
@login_required
def editFeat(tfeat):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tfeat = Feat.query.filter_by(rulesetid=cruleset.id, name=tfeat).first()
    if(not tfeat):
        flash("Feat does not exist.", "red")
    elif(request.method == "POST"):
        return(makefeat(request, cruleset, tfeat, "edit"))
    return(
        render_template(
            "create-feat.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title=f"Edit {tfeat.name}",
            tfeat=tfeat
        )
    )

@epchar.route("/Feats/Delete/<string:tfeat>")
@login_required
def deleteFeat(tfeat):
    cruleset = getCurrentRuleset(current_user)
    tfeat = Feat.query.filter_by(rulesetid=cruleset.id, name=tfeat).first()
    if(not tfeat):
        flash("Feat does not exist.", "red")
    elif(current_user.id != cruleset.userid):
        flash("You cannot delete feats in rulesets that are not your own.", "red")
    else:
        db.session.delete(tfeat)
        db.session.commit()
        flash("Feat deleted.", "orange")
    return(redirect(url_for("epchar.feats")))

@epchar.route("/Feat/<string:feat>")
def feat(feat):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    feat = Feat.query.filter_by(rulesetid = cruleset.id, name = feat).first()
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
        return(abilityScore(request, cruleset, None, "create"))
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
    ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score).first()
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
    ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score).first()
    if(not ability_score):
        flash("Ability Score does not exist.", "red")
    else:
        result = abilityScore(None, cruleset, ability_score, "duplicate")
    return(redirect(url_for("epchar.stats")))

@epchar.route("/Ability-Scores/Delete/<string:score>")
@login_required
def deleteStat(score):
    cruleset = getCurrentRuleset(current_user)
    if(current_user.id != cruleset.userid):
        flash("You cannot delete Ability Scores in rulesets that are not your own.", "red")
    else:
        ability_score = AbilityScore.query.filter_by(rulesetid=cruleset.id, name=score).first()
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
            return(redirect(url_for("epchar.classes")))
        else:
            return(makeclass(request, cruleset, None, "create"))
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

@epchar.route("/Classes/Duplicate/<string:tclass>")
@login_required
def duplicateClass(tclass):
    cruleset = getCurrentRuleset(current_user)
    tclass = Class.query.filter_by(rulesetid=cruleset.id, name=tclass).first()
    if(not tclass):
        flash("Class does not exist", "red")
    else:
        return(makeclass(None, cruleset, tclass, "duplicate"))

@epchar.route("/Classes/Edit/<string:tclass>", methods=["GET", "POST"])
@login_required
def editClass(tclass):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tclass = Playerclass.query.filter_by(rulesetid=cruleset.id, name=tclass).first()
    if(request.method == "POST"):
        if(not tclass):
            flash("Class does not exist", "red")
            return(redirect(url_for("epchar.classes")))
        else:
            return(makeclass(request, cruleset, tclass, "edit"))
    return(
        render_template(
            "create-class.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title=f"Edit {tclass.name}",
            tclass=tclass
        )
    )

@epchar.route("/Class/<string:selectedclass>")
def classPage(selectedclass):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    selectedclass = Playerclass.query.filter_by(name=selectedclass).first()
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