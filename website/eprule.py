from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash
from .models import Ruleset, Category, Rule
from . import db
from flask_login import current_user, login_required
from .check_ruleset import *

eprule = Blueprint('eprule', __name__)

## RULES
@eprule.route("/")
def rules():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    pinnedrules = []
    for category in cruleset.categories:
        for rule in category.rules:
            if(rule.pinned):
                pinnedrules.append(rule)
    return(render_template("rules.html", user=current_user, frulesets=frulesets, cruleset=cruleset, prules=pinnedrules, adminrulesets=adminrulesets))

@eprule.route("/Create", methods=["GET", "POST"])
@login_required
def createRule():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create rules for rulesets that are not your own.")
        else:
            name = request.form.get("name")
            category = request.form.get("category")
            text = request.form.get("text")
            if(len(name) < 1) :
                flash("You must specify a rule name.")
            elif(len(name) > 127):
                flash("Rule name must be fewer than 128 characters.")
            elif(len(text) < 1):
                flash("You must specify rule text.")
            elif(len(text) > 16383):
                flash("Rule text must be fewer than 16384 characters")
            elif("<" in text or "<" in name):
                flash("Opening angle brackets (\"<\") are not allowed.")
            elif("javascript" in name or "javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_rule = Rule(name=name, rule_categoryid=cruleset.id, text=text)
                db.session.add(new_rule)
                db.session.commit()
                flash("Rule created.")
                return(redirect(url_for("eprule.rules")))
    if(len(cruleset.categories) < 1):
        flash("You must have at least one category to add the rule to.")
        return(redirect(url_for("eprule.createCategory")))
    
    return(render_template("create-rule.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@eprule.route("/Create-Category", methods=["GET", "POST"])
@login_required
def createCategory():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(len(current_user.rulesets) < 1):
        flash("The current ruleset must have at least one ruleset to add the category to.")
        return(redirect(url_for("epmain.createRuleset")))
    elif(cruleset.id == 1 and current_user.id != 1):
        flash("You cannot edit the default ruleset.")
    elif(request.method == "POST"):
        name = request.form.get("name")
        if(len(name) < 1):
            flash("You must specify a name for the rule category.")
        elif(len(name) > 127):
            flash("Category name must be fewer than 128 chatacters.")
        elif("<" in name):
            flash("Opening angle brackets (\"<\") are not allowed.")
        elif("javascript" in name):
            flash("Cross-site scripting attacks are not allowed.")
        elif("-" in name):
            flash("Dashes (\"-\") are not allowed in category name.")
        else:
            new_category = Category(name=request.form.get("name"), rulesetid=cruleset.id, pinned=False)
            db.session.add(new_category)
            db.session.commit()
            flash("Rule category created.")
            return(redirect(url_for("eprule.rules")))
    return(render_template("create-category.html", user=current_user, frulesets=frulesets, cruleset=cruleset, adminrulesets=adminrulesets))

@eprule.route("/<string:categoryname>")
def CategoryRoute(categoryname):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    categoryname = categoryname.replace("-", " ")
    rules = Category.query.filter_by(name=categoryname, rulesetid=cruleset.id).first().rules
    return(render_template("category.html", user=current_user, frulesets=frulesets, cruleset=cruleset, rules=rules, heading=categoryname, adminrulesets=adminrulesets))
