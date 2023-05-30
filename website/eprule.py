from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash
from .models import Ruleset, Category, Rule
from . import db
from flask_login import current_user, login_required
from .uservalidation import *

eprule = Blueprint('eprule', __name__)

## RULES
@eprule.route("/")
def noRulesetRules():
    return(noRuleset(current_user, "eprule.rules"))
@eprule.route("/", subdomain="<ruleset>")
def rules(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    pinnedrules = []
    for category in cruleset.categories:
        for rule in category.rules:
            if(rule.pinned):
                pinnedrules.append(rule)
    return(
        render_template(
            "rules.html", 
            cruleset=cruleset, 
            prules=pinnedrules, 
            adminrulesets=adminrulesets,
            title="Pinned Rules"
        )
    )

@eprule.route("/Create")
@login_required
def noRulesetCreateRule():
    return(noRuleset(current_user, "eprule.createRule"))
@eprule.route("/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createRule(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create rules for rulesets that are not your own.", "red")
        else:
            name = request.form.get("name")
            category = request.form.get("category")
            text = request.form.get("text")
            if(len(name) < 1) :
                flash("You must specify a rule name.", "red")
            elif(len(name) > 127):
                flash("Rule name must be fewer than 128 characters.", "red")
            elif(len(text) < 1):
                flash("You must specify rule text.", "red")
            elif(len(text) > 16383):
                flash("Rule text must be fewer than 16384 characters", "red")
            elif("<" in text or "<" in name):
                flash("Opening angle brackets (\"<\") are not allowed.", "red")
            elif("javascript" in name or "javascript" in text):
                flash("Cross-site scripting attacks are not allowed.", "red")
            else:
                new_rule = Rule(name=name, rule_categoryid=cruleset.id, text=text)
                db.session.add(new_rule)
                db.session.commit()
                flash("Rule created.", "green")
                return(redirect(url_for("eprule.rules", ruleset=ruleset)))
    if(len(cruleset.categories) < 1):
        flash("You must have at least one category to add the rule to.")
        return(redirect(url_for("eprule.createCategory", ruleset=ruleset)))
    
    return(
        render_template(
            "create-rule.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Rule"
        )
    )

@eprule.route("/Create-Category")
@login_required
def noRulesetCreateCategory():
    return(noRuleset(current_user, "eprule.createCategory"))
@eprule.route("/Create-Category", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createCategory(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(len(current_user.rulesets) < 1):
        flash("The current ruleset must have at least one ruleset to add the category to.", "red")
        return(redirect(url_for("epmain.createRuleset", ruleset=ruleset)))
    elif(cruleset.id == 1 and current_user.id != 1):
        flash("You cannot edit the default ruleset.", "red")
    elif(request.method == "POST"):
        name = request.form.get("name")
        if(len(name) < 1):
            flash("You must specify a name for the rule category.", "red")
        elif(len(name) > 127):
            flash("Category name must be fewer than 128 chatacters.", "red")
        elif("<" in name):
            flash("Opening angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in name):
            flash("Cross-site scripting attacks are not allowed.", "red")
        else:
            new_category = Category(name=request.form.get("name"), rulesetid=cruleset.id, pinned=False)
            db.session.add(new_category)
            db.session.commit()
            flash("Rule category created.", "green")
            return(redirect(url_for("eprule.rules", ruleset=ruleset)))
    return(
        render_template(
            "create-category.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Rule Category"
        )
    )

@eprule.route("/<string:categoryname>")
def noRulesetCategoryRoute(categoryname):
    return(noRuleset(current_user, "eprule.CategoryRoute"))
@eprule.route("/<string:categoryname>", subdomain="<ruleset>")
def CategoryRoute(categoryname, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    categoryname = categoryname
    rules = Category.query.filter_by(name=categoryname, rulesetid=cruleset.id).first().rules
    return(
        render_template(
            "category.html", 
            cruleset=cruleset, 
            rules=rules, 
            title=categoryname, 
            adminrulesets=adminrulesets
        )
    )
