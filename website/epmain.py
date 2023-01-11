from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
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
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "index.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Home"
        )
    )

@epmain.route("/Get-Current-Ruleset")
def get():
    # data = json.loads(request.data)
    # cruleset = getCurrentRuleset(current_user, data["local"])
    cruleset = getCurrentRuleset(current_user)
    ruleset = jsonify({
        "id": cruleset.id,
        "name": cruleset.name
    })
    return(ruleset)

@epmain.route("/My-Rulesets")
@login_required
def myRulesets():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "my-rulesets.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="My Rulesets"
        )
    )

@epmain.route("/Create-Ruleset", methods=["GET", "POST"])
@login_required
def createRuleset():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
        elif("<" in name):
            flash("Opening angle brackets (\"<\") are not allowerd.")
        elif("javascript" in name):
            flash("Cross-site scripting attacks are not allowed.")
        else:
            if(current_user.username == "admin"):
                is_admin = True
            else:
                is_admin = False
            new_ruleset = Ruleset(userid=current_user.id, is_shareable=shareable, name=name, is_admin=is_admin)
            db.session.add(new_ruleset)
            db.session.commit()
            flash("Ruleset created!")
            return(redirect(url_for("epmain.myRulesets")))
    return(
        render_template(
            "create-ruleset.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Create a Ruleset"
        )
    )

@epmain.route("/Manage-Ruleset/<int:rulesetid>", methods=["GET", "POST"])
@login_required
def manageRuleset(rulesetid):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
        elif("<" in name):
            flash("Opening angle brackets (\"<\") are not allowerd.")
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
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Manage Ruleset"
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
        if(current_user.current_ruleset == ruleset.id):
            current_user.current_ruleset = 1
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
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Add a Friend's Ruleset"
        )
    )

@epmain.route("/Remove-Ruleset", methods=["POST"])
@login_required
def removeRuleset():
    instruction = json.loads(request.data)
    rulesetid = instruction["rulesetid"]
    ruleset = Ruleset.query.filter_by(id = rulesetid).first()
    if(current_user.current_ruleset == rulesetid):
        current_user.current_ruleset = 1 
    if(current_user.foreign_ruleset == str(ruleset.id)):
        current_user.foreign_ruleset = ""
        db.session.commit()
    else:
        oldforeign = current_user.foreign_ruleset.split(",")
        oldforeign.remove(str(rulesetid))
        newruleset = []
        newruleset[0] = oldforeign[0]
        index = 1
        for i in range(len(oldforeign) - 1):
            newruleset.append(i)
        current_user.foreign_ruleset = newruleset
        db.session.commit()
    flash("Removed Ruleset.")
    return(redirect(url_for("epmain.myRulesets")))

@epmain.route("/Change-Ruleset", methods=["POST"])
@login_required
def changeRuleset():
    rulesetid = json.loads(request.data)["rulesetid"]
    current_user.current_ruleset = rulesetid
    db.session.commit()
    return("")
