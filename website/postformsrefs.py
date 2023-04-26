from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .models import Skill, ItemTag, Property, Language, Item

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

def makeItem(request, cruleset, item, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot ceeate skills for rulesets that are not your own.", "red")
    elif(instruction == "duplicate"):
        new_item = Item(
            rulesetid = cruleset.id,
            name = f"{item.name} Duplicate",
            is_magical = item.is_magical,
            rarity = item.rarity,
            tier = item.tier,
            attunement = item.attunement,
            tags = item.tags,
            proficiency = item.proficiency,
            cost = item.cost,
            weight = item.weight,
            text = item.text,
            is_armor = item.is_armor,
            armor_class = item.armor_class,
            add_dex = item.add_dex,
            max_dex = item.max_dex,
            is_weapon = item.is_weapon,
            die_num = item.die_num,
            damage_die = item.damage_die,
            damage_type = item.damage_type,
            weapon_properties = item.weapon_properties
        )
        db.session.add(new_item)
        db.session.commit()
        flash("ITem Duplicated!", "green")
        return(redirect(url_for("eprefs.items")))
    else:
        name = request.form.get("name")
        is_magical = request.form.get("ismagical")
        if(is_magical):
            is_magical = True
            tier = request.form.get("tier")
            rarity = request.form.get("rarity")
            attunement = request.form.get("attunement")
            if(attunement):
                attunement = True
            else:
                attunement = False
        else:
            is_magical = False
            tier = None
            rarity = None
            attunement = None
        tags = request.form.getlist("tag")
        proficiency = request.form.get("proficiency")
        if(proficiency):
            proficiency = True
        else:
            proficiency = False
        cost = request.form.get("cost")
        weight = request.form.get("weight")
        text = request.form.get("text")
        is_armor = request.form.get("isarmor")
        if(is_armor):
            is_armor = True
            armor_class = request.form.get("armorclass")
            add_dex = request.form.get("adddex")
            if(add_dex):
                add_dex = True
                max_dex = request.form.get("maxdex")
            else:
                add_dex = False
                max_dex = None
        else:
            is_armor = False
            armor_class = None
            add_dex = None
            max_dex = None
        is_weapon = request.form.get("isweapon")
        if(is_weapon):
            is_weapon = True
            die_num = request.form.get("dienum")
            damage_die = request.form.get("damagedie")
            damage_type = request.form.get("damagetype")
            weapon_properties = request.form.getlist("property")
        else:
            is_weapon = False
            die_num = None
            damage_die = None
            damage_type = None
            weapon_properties = []
        if(len(name) < 1):
            flash("You must specify an item name.", "red")
        elif(len(name) > 127):
            flash("Item name must be fewer than 128 characters.", "red")
        elif(len(cost) > 31):
            flash("Item cost must be fewer than 32 characters.", "red")
        elif(len(tags) > 127):
            flash("Too many item tags specified (sorry).", "red")
        elif(len(text) > 16383):
            flash("Item text must be fewer than 16384 characters.", "red")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif(len(weapon_properties) > 255):
            flash("Weapon Properties must be fewer than 256 characters.", "red")
        else:
            if(instruction=="create"):
                new_item = Item(
                    rulesetid = cruleset.id,
                    name = name,
                    is_magical = is_magical,
                    rarity = rarity,
                    tier = tier,
                    attunement = attunement,
                    tags = tags,
                    proficiency = proficiency,
                    cost = cost,
                    weight = weight,
                    text = text,
                    is_armor = is_armor,
                    armor_class = armor_class,
                    add_dex = add_dex,
                    max_dex = max_dex,
                    is_weapon = is_weapon,
                    die_num = die_num,
                    damage_die = damage_die,
                    damage_type = damage_type,
                    weapon_properties = weapon_properties
                )
                db.session.add(new_item)
                flash("Item created.", "green")
            else:
                item.name = name
                item.is_magical = is_magical
                item.rarity = rarity
                item.tier = tier
                item.attunement = attunement
                item.tags = tags
                item.proficiency = proficiency
                item.cost = cost
                item.weight = weight
                item.text = text
                item.is_armor = is_armor
                item.armor_class = armor_class
                item.add_dex = add_dex
                item.max_dex = max_dex
                item.is_weapon = is_weapon
                item.die_num = die_num
                item.damage_die = damage_die
                item.damage_type = damage_type
                item.weapon_properties = weapon_properties
                flash("Changes saved!", "green")
            db.session.commit()
            return(redirect(url_for("eprefs.items")))
    return(False)

def makeLanguage(request, cruleset, language, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create languages for rulesets that are not your own.", "red")
    elif(instruction == "duplicate"):
        new_language = Language(
            rulesetid=cruleset.id,
            name=f"{language.name} Duplicate",
            text=language.text
        )
        db.session.add(new_language)
        db.session.commit()
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a language name.", "red")
            return(redirect(url_for("eprefs.createLanguage")))
        elif(len(name) > 127):
            flash("Language name must be fewer than 128 characters.", "red")
            return(redirect(url_for("eprefs.createLanguage")))
        elif(len(text) > 16383):
            flash("Language description must be fewer than 16384 characters.", "red")
            return(redirect(url_for("eprefs.createLanguage")))
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("eprefs.createLanguage")))
        elif("<" in text):
            flash("Open angle brackets(\"<\") are not allowed.", "red")
            return(redirect(url_for("eprefs.createLanguage")))
        else:
            if(instruction == "edit"):
                language.name = name
                language.text = text
                db.session.commit()
                flash("Changes Saved!", "green")
            else:
                new_language = Language(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_language)
                db.session.commit()
                flash("Language created!", "green")
    return(redirect(url_for("eprefs.refsLang")))

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
                flash("Skill created!", "green")
            db.session.commit()
    return(redirect(url_for("eprefs.skills")))