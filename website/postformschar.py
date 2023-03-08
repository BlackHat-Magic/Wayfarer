from flask import render_template, redirect, url_for, request, session, flash, jsonify
from . import db
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature, Background, BackgroundFeature, Feat, Item, Playerclass, AbilityScore, ClassColumn, SubclassColumn, ClassFeature, Playerclass, Subclass, SubclassFeature

def abilityScore(request, cruleset, ability_score):
    name = request.form.get("name")
    abbr = request.form.get("abbr")
    order = request.form.get("order")
    text = request.form.get("text")
    bad = False
    if(order):
        try:
            order = int(order)
        except:
            flash("Ability Score Order must be a number.")
            bad = True
    if(len(name) < 1):
        flash("You must specify an Ability Score name.", "red")
    elif(len(name) > 127):
        flash("Ability Score name must be fewer than 128 characters.", "red")
    elif(len(abbr) != 3):
        flash("Ability Score abbreviation must be 3 characters.", "red")
    elif(len(text) > 16383):
        flash("Ability Score description must be fewer than 16384 characters.", "red")
    elif("<" in text):
        flash("Open angle brackets (\"<\") are not allowed.", "red")
    elif("javascript" in text):
        flash("Cross-site scripting attacks are not allowed.", "red")
    elif(not bad):
        if(not ability_score):
            new_ability_score = AbilityScore(
                rulesetid = cruleset.id,
                name = name,
                abbr = abbr,
                order = order,
                text = text
            )
            db.session.add(new_ability_score)
            db.session.commit()
            flash("Ability Score created!", "green")
        else:
            ability_score.name = name
            ability_score.abbr = abbr
            ability_score.order=order
            ability_score.text = text
            db.session.commit()
            flash("Changes saved!", "green")
        return(redirect(url_for("epchar.stats")))
    return(False)