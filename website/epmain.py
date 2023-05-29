from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from .models import Ruleset
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import current_user, login_required
from .postformsmain import *
from .uservalidation import *
import json

epmain = Blueprint("epmain", __name__)

# MAIN DOES NOT NEED SUBDOMAINS; FIX THIS

@epmain.route("/")
def noRulesetHome():
    return(noRuleset(current_user, "epmain.home"))
@epmain.route("/", subdomain="<ruleset>")
def home(ruleset):
    print("hello")
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "index.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Home"
        )
    )

@epmain.route("/My-Rulesets")
@login_required
def noRulesetMyRulesets():
    return(noRuleset(current_user, "epmain.myRulesets"))
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

@epmain.route("/Create-Ruleset")
@login_required
def noRulesetCreateRuleset():
    return(noRuleset(current_user, "epmain.createRuleset"))
@epmain.route("/Create-Ruleset", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createRuleset(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        base = request.form.get("base")
        if(base == "" or base == "None"):
            return(makeRuleset(request, None, "create"))
        else:
            ruleset = Ruleset.query.filter_by(id=base).first_or_404()
            return(makeRuleset(request, ruleset, "duplicate"))
    return(
        render_template(
            "create-ruleset.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Create a Ruleset"
        )
    )

@epmain.route("/Manage-Ruleset/<string:rulesetid>")
@login_required
def noRulesetManageRuleset(rulesetid):
    return(noRuleset(current_user, "epmain.manageRuleset", rulesetid=rulesetid))
@epmain.route("/Manage-Ruleset/<string:rulesetid>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def manageRuleset(rulesetid, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    target_ruleset = Ruleset.query.filter_by(id=rulesetid).first()
    if(request.method == "POST"):
        return(makeRuleset(request, target_ruleset, "edit"))
    return(
        render_template(
            "create-ruleset.html", 
            ruleset=target_ruleset, 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title=f"Manage Ruleset: {target_ruleset.name}"
        )
    )

@epmain.route("/Delete-Ruleset/<string:rulesetid>")
@login_required
def noRulesetDeleteRuleset(rulesetid):
    return(noRuleset(current_user, "epmain.deleteRuleset", rulesetid=rulesetid))
@epmain.route("/Delete-Ruleset/<rulesetid>", subdomain="<ruleset>")
@login_required
def deleteRuleset(ruleset, rulesetid):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(current_user.id == ruleset.userid):
        db.session.delete(ruleset)
        if(current_user.current_ruleset == ruleset.id):
            current_user.current_ruleset = Ruleset.query.filter_by(is_admin=True).first().id
            cruleset = Ruleset.query.filter_by(is_admin=True).first().identifier
        db.session.commit()
        flash("Ruleset deleted.", "orange")
    else:
        flash("This is not your ruleset.", "red")
    return(redirect("epmain.home", ruleset=cruleset))

@epmain.route("/Add-Ruleset")
@login_required
def noRulesetAddRuleset():
    return(noRuleset(current_user, "epmain.addRuleset"))
@epmain.route("/Add-Ruleset", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def addRuleset(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        rulesetid = request.form.get("rulesetid")
        target_ruleset = Ruleset.query.filter_by(id=rulesetid).first()
        if(not target_ruleset):
            flash("Ruleset does not exist.", "red")
        elif(target_ruleset.visibility < 1):
            flash("Ruleset is private.", "red")
        elif(target_ruleset.userid == current_user.id):
            flash("You cannot add your own ruleset as a foreign ruleset.", "red")
        elif(target_ruleset.id in current_user.foreign_ruleset):
            if(target_ruleset.id in current_user.foreign_ruleset.split(",")):
                flash("You've already added that ruleset.", "red")
        else:
            current_user.foreign_ruleset += target_ruleset.id
            target_ruleset.viewers += current_user.id
            db.session.commit()
            flash("Added ruleset.", "green")
            return(redirect(url_for("epmain.home")))
    return(
        render_template(
            "add-ruleset.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Add a Friend's Ruleset"
        )
    )

@epmain.route("/Remove-Ruleset")
@login_required
def noRulesetRemoveRuleset():
    return(noRuleset(current_user, "epmain.removeRuleset"))
@epmain.route("/Remove-Ruleset", methods=["POST"], subdomain="<ruleset>")
@login_required
def removeRuleset(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(current_user.current_ruleset == rulesetid):
        current_user.current_ruleset = adminrulesets[0].id
    else:
        current_user.foreign_ruleset.remove(rulesetid)
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

@epmain.route("/My-Account")
@login_required
def noRulesetMyAccount():
    return(noRuleset(current_user, "epmain.myAccount"))
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
