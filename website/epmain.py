from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash
from .models import Ruleset
from . import db
from flask_login import current_user, login_required
from .check_ruleset import *
import json

epmain = Blueprint("epmain", __name__)

@epmain.route("/")
def home():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(
        render_template(
            "index.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset
        )
    )

@epmain.route("/Get-Current-Ruleset")
def get():
    return(getCurrentRuleset(current_user).name)

@epmain.route("/My-Rulesets")
@login_required
def myRulesets():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    return(
        render_template(
            "my-rulesets.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset
        )
    )

@epmain.route("/Create-Ruleset", methods=["GET", "POST"])
@login_required
def createRuleset():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        try:
            shareable = bool(request.form.get("shareable"))
        except:
            shareable = False
        name = request.form.get("name")
        if(len(name) < 1):
            flash("You must specify a ruleset name.")
        elif(len(name) > 127):
            flash("Ruleset name must be fewer than 128 characters.")
        elif("<" in name or ">" in name):
            flash("Angle brackets (\"<\" and \">\") are not allowerd.")
        elif("javascript" in name):
            flash("Cross-site scripting attacks are not allowed.")
        else:
            new_ruleset = Ruleset(userid=current_user.id, is_shareable=shareable, name=name)
            db.session.add(new_ruleset)
            db.session.commit()
            flash("Ruleset created!")
            return(redirect(url_for("epmain.myRulesets")))
    return(
        render_template(
            "create-ruleset.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset
        )
    )

@epmain.route("/Manage-Ruleset/<int:rulesetid>", methods=["GET", "POST"])
@login_required
def manageRuleset(rulesetid):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        ruleset = Ruleset.query.filter_by(id=rulesetid).first()
        print("got ruleset " + ruleset.name)

        name = request.form.get("name")
        if(request.form.get("shareable").casefold() == "true"):
            shareable = True
        else:
            shareable = False
        if(len(name) < 1):
            flash("You must specify a ruleset name.")
        elif(len(name) > 127):
            flash("Ruleset name must be fewer than 128 characters.")
        elif("<" in name or ">" in name):
            flash("Angle brackets (\"<\" and \">\") are not allowerd.")
        elif("javascript" in name):
            flash("Cross-site scripting attacks are not allowed.")
        else:
            ruleset.name = name
            ruleset.is_shareable = shareable
            db.session.commit()
            flash("Success")
            return(redirect(url_for("epmain.myRulesets")))
    else:
        ruleset = Ruleset.query.filter_by(id=rulesetid).first()
    return(
        render_template(
            "manage-ruleset.html", 
            user=current_user, 
            ruleset=ruleset, 
            frulesets=frulesets, 
            cruleset=cruleset
        )
    )

@epmain.route("/Delete-Ruleset/", methods=["POST"])
@login_required
def deleteRuleset():
    instruction = json.loads(request.data)
    rulesetid = instruction["rulesetid"]
    ruleset = Ruleset.query.filter_by(id = rulesetid).first()
    if(current_user.id == ruleset.userid):
        db.session.delete(ruleset)
        db.session.commit()
        flash("Ruleset deleted.")
    else:
        flash("This is not your ruleset.")
    return(redirect("epmain.myRulesets"))

@epmain.route("/Add-Ruleset/", methods=["GET", "POST"])
@login_required
def addRuleset():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    if(request.method == "POST"):
        ruleset = request.form.get("rulesetid")
        if(not Ruleset.query.filter_by(id=int(ruleset)).first()):
            flash("Ruleset does not exist.")
        elif(not Ruleset.query.filter_by(id=int(ruleset)).first().is_shareable):
            flash("Ruleset is not shareable.")
        elif(Ruleset.query.filter_by(id=int(ruleset)).first().userid == current_user.id):
            flash("You cannot add your own ruleset as a foreign ruleset.")
        elif(current_user.foreign_ruleset):
            if(ruleset in current_user.foreign_ruleset.split(",")):
                flash("You've already added that ruleset.")
            else:
                current_user.foreign_ruleset.append("," + ruleset)
                db.session.commit()
                flash("Added ruleset.")
                return(redirect(url_for("epmain.myRulesets")))
        else:
            current_user.foreign_ruleset = ruleset
            db.session.commit()
            flash("Added ruleset.")
            return(redirect(url_for("epmain.myRulesets")))
    return(
        render_template(
            "add-ruleset.html",
            user=current_user,
            frulesets=frulesets,
            cruleset=cruleset
        )
    )

