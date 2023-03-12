from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .models import Skill, ItemTag, Property

def itemTag(request, cruleset, tag, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create item tags for rulesets that are not your own", "red")
    elif(instruction == "duplicate"):
        new_tag = ItemTag(
            rulesetid = cruleset.id,
            name = f"{tag.name} Duplicate",
            text = tag.text
        )
        db.session.add(new_tag)
        db.session.commit()
        flash("Item Tag Duplicated!", "green")
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a tag name.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif(len(name) > 127):
            flash("Tag name must be fewer than 128 characters.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif(len(text) > 16383):
            flash("Tag description must be fewer than 16384 characters.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag")))
        else:
            if(instruction == "create"):
                new_tag = ItemTag(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_tag)
                db.session.commit()
                flash("Item Tag created!", "green")
            else:
                tag.name = name
                tag.text = text
                db.session.commit()
                flash("Changes Saved!", "green")
    return(redirect(url_for("eprefs.tags")))

def itemProperty(request, cruleset, tproperty, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create weapon properties for rulesets that are not your own", "red")
    elif(instruction == "duplicate"):
        new_property = Property(
            rulesetid = cruleset.id,
            name = f"{tproperty.name} Duplicate",
            text = tproperty.text
        )
        db.session.add(new_property)
        db.session.commit()
        flash("Item Property Duplicated!", "green")
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a tag name.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif(len(name) > 127):
            flash("Tag name must be fewer than 128 characters.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif(len(text) > 16383):
            flash("Tag description must be fewer than 16384 characters.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag")))
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag")))
        else:
            if(instruction == "create"):
                new_property = Property(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_property)
                db.session.commit()
                flash("Item tag created!", "green")
            else:
                tproperty.name = name
                tproperty.text = text
                db.session.commit()
    return(redirect(url_for("eprefs.properties")))

def skill(request, cruleset, skill, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create skills for rulesets that are not your own.", "red")
    elif(instruction == "duplicate"):
        new_skill = Skill(
            rulesetid = cruleset.id,
            name = f"{skill.name} Duplicate",
            ability_score = skill.ability_score,
            description = skill.description
        )
        db.session.add(new_skill)
        db.session.commit()
        flash("Skill duplicated!", "green")
    else:
        name = request.form.get("name")
        ability_score = request.form.get("ability")
        description = request.form.get("text")
        if(not ability_score):
            ability_score = None
        if(len(name) < 1):
            flash("You must specify a skill name.", "red")
            return(redirect(url_for("eprefs.createSkill")))
        elif(len(name) > 63):
            flash("Skill name must be fewer than 64 characters.", "red")
            return(redirect(url_for("eprefs.createSkill")))
        elif(len(description) > 16383):
            flash("Skill description must be fewer than 16384 characters.", "red")
            return(redirect(url_for("eprefs.createSkill")))
        elif("javascript" in description):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("eprefs.createSkill")))
        elif("<" in description):
            flash("Open angle brackets(\"<\") are not allowed.", "red")
            return(redirect(url_for("eprefs.createSkill")))
        else:
            if(instruction == "edit"):
                skill.name = name
                skill.ability_score = ability_score
                skill.description = description
                flash("Changes Saved!", "green")
            else:
                new_skill = Skill(
                    rulesetid = cruleset.id,
                    name = name,
                    ability_score = ability_score,
                    description = description
                )
                db.session.add(new_skill)
                db.session.commit()
                flash("Skill created!", "green")
    return(redirect(url_for("eprefs.skills")))