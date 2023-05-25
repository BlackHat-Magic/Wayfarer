from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from .models import Ruleset
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import current_user, login_required
from .uservalidation import *
import json

epmain = Blueprint("epmain", __name__)

# MAIN DOES NOT NEED SUBDOMAINS; FIX THIS

@epmain.route("/", subdomain="<ruleset>")
def home(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "index.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Home"
        )
    )

@epmain.route("/My-Rulesets", subdomain="<ruleset>")
@login_required
def myRulesets(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "my-rulesets.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="My Rulesets"
        )
    )

@epmain.route("/Create-Ruleset", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createRuleset(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        try:
            shareable = bool(request.form.get("shareable"))
        except:
            shareable = False
        name = request.form.get("name")
        if(len(name) < 1):
            flash("You must specify a ruleset name.", "red")
        elif(len(name) > 127):
            flash("Ruleset name must be fewer than 128 characters.", "red")
        elif("<" in name):
            flash("Opening angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in name):
            flash("Cross-site scripting attacks are not allowed.", "red")
        else:
            if(current_user.username == "admin"):
                is_admin = True
            else:
                is_admin = False
            new_ruleset = Ruleset(userid=current_user.id, is_shareable=shareable, name=name, is_admin=is_admin)
            db.session.add(new_ruleset)
            db.session.commit()
            flash("Ruleset created!", "green")
            return(redirect(url_for("epmain.myRulesets")))
    return(
        render_template(
            "create-ruleset.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Create a Ruleset"
        )
    )

@epmain.route("/Manage-Ruleset/<string:rulesetid>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def manageRuleset(rulesetid, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        ruleset = Ruleset.query.filter_by(id=rulesetid).first()
        print("got ruleset " + ruleset.name)

        name = request.form.get("name")
        if(request.form.get("shareable").casefold() == "true"):
            shareable = True
        else:
            shareable = False
        if(len(name) < 1):
            flash("You must specify a ruleset name.", "red")
        elif(len(name) > 127):
            flash("Ruleset name must be fewer than 128 characters.", "red")
        elif("<" in name):
            flash("Opening angle brackets (\"<\") are not allowerd.", "red")
        elif("javascript" in name):
            flash("Cross-site scripting attacks are not allowed.", "red")
        else:
            ruleset.name = name
            ruleset.is_shareable = shareable
            db.session.commit()
            flash("Success", "green")
            return(redirect(url_for("epmain.myRulesets")))
    else:
        ruleset = Ruleset.query.filter_by(id=rulesetid).first()
    return(
        render_template(
            "manage-ruleset.html", 
            ruleset=ruleset, 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Manage Ruleset"
        )
    )

@epmain.route("/Delete-Ruleset/", methods=["POST"], subdomain="<ruleset>")
@login_required
def deleteRuleset(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(current_user.id == ruleset.userid):
        db.session.delete(ruleset)
        if(current_user.current_ruleset == ruleset.id):
            current_user.current_ruleset = Ruleset.query.filter_by(is_admin=True).first()
        db.session.commit()
        flash("Ruleset deleted.", "orange")
    else:
        flash("This is not your ruleset.", "red")
    return(redirect("epmain.myRulesets"))

@epmain.route("/Add-Ruleset/", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def addRuleset(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        ruleset = request.form.get("rulesetid")
        if(not Ruleset.query.filter_by(id=int(ruleset)).first()):
            flash("Ruleset does not exist.", "red")
        elif(not Ruleset.query.filter_by(id=int(ruleset)).first().is_shareable):
            flash("Ruleset is not shareable.", "red")
        elif(Ruleset.query.filter_by(id=int(ruleset)).first().userid == current_user.id):
            flash("You cannot add your own ruleset as a foreign ruleset.", "red")
        elif(current_user.foreign_ruleset):
            if(ruleset in current_user.foreign_ruleset.split(",")):
                flash("You've already added that ruleset.", "red")
            else:
                current_user.foreign_ruleset.append("," + ruleset)
                db.session.commit()
                flash("Added ruleset.", "green")
                return(redirect(url_for("epmain.myRulesets")))
        else:
            current_user.foreign_ruleset = ruleset
            db.session.commit()
            flash("Added ruleset.", "green")
            return(redirect(url_for("epmain.myRulesets")))
    return(
        render_template(
            "add-ruleset.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Add a Friend's Ruleset"
        )
    )

@epmain.route("/Remove-Ruleset", methods=["POST"], subdomain="<ruleset>")
@login_required
def removeRuleset(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    flash("Removed Ruleset.", "orange")
    return(redirect(url_for("epmain.myRulesets")))

@epmain.route("/Change-Ruleset", methods=["POST"])
@login_required
def changeRuleset():
    rulesetid = json.loads(request.data)["rulesetid"]
    current_user.current_ruleset = rulesetid
    db.session.commit()
    flash("Ruleset changed.", "green")
    return("")

@epmain.route("/My-Account", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def myAccount(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        username = request.form.get("username")
        email = request.form.get("email")
        cpasswd = request.form.get("cpasswd")
        npasswd1 = request.form.get("npasswd1")
        npasswd2 = request.form.get("npasswd2")
        user = User.query.filter_by(username = username).first()
        if (len(username) < 1):
            username = current_user.username
        if(len(email) < 1):
            email = current_user.email
        if(len(npasswd1) < 1):
            npasswd1 = "eternity-freezing-mama"
            npasswd2 = "eternity-freezing-mama"
        if(len(username) < 4):
            flash("Username must be at least 4 characters", "red")
        elif(user):
            flash("Username already in use. Please pick another username.", "red")
        elif(len(email) < 5):
            flash("Email is not valid.", "red")
        elif(len(username) > 255):
            flash("Username must be fewer than 256 characters.", "red")
        elif(not check_password_hash(current_user.password, cpasswd)):
            flash("Incorrect password", "red")
        elif(len(npasswd1) < 8):
            flash("Password must be at least 8 characters.", "red")
        elif(npasswd1 != npasswd2):
            flash("Passwords do not match", "red")
        else:
            current_user.username = username
            current_user.email = email
            if(npasswd1 != "eternity-freezing-mama"):
                current_user.password = generate_password_hash(npasswd1, method="sha256")
            flash("Changes saved.", "green")
            return(redirect(url_for("epmain.home")))
    return(
        render_template(
            "my-account.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="My Account"
        )
    )
