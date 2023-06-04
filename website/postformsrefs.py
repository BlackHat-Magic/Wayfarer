from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .jsonparsers import *
from .models import Skill, ItemTag, Property, Language, Item, Action, Condition, Disease, Status, Spell
import sys, pickle

def makeAction(request, cruleset, action, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} actions in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.actions", ruleset=cruleset.identifier)))
    elif(instruction == "duplicate"):
        new_action = Action(
            rulesetid = cruleset.id,
            name = f"{action.name} Duplicate",
            time = action.time,
            text = action.text
        )
        db.session.add(new_action)
        db.session.commit()
        flash("Action duplicated!")
    else:
        name = request.form.get("name")
        time = request.form.get("time")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify an action name.", "red")
        elif(len(name) > 127):
            flash("Action name must be fewer than 128 characters.", "red")
        elif(len(time) > 127):
            flash("Action time must be fewer than 128 characters.", "red")
        elif(len(text) > 16383):
            flash("Action text must be fewer than 16383 characters", "red")
        elif(instruction == "create"):
            new_action = Action(
                rulesetid = cruleset.id,
                name = name,
                time = time,
                text = text
            )
            db.session.add(new_action)
            db.session.commit()
            flash("Action created!", "green")
            return(redirect(url_for("eprefs.actions", ruleset=cruleset.identifier)))
        else:
            action.name = name
            action.time = time
            action.text = text
            db.session.commit()
            flash("Changes saved!", "green")
            return(redirect(url_for("eprefs.actions", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createAction", ruleset=cruleset.identifier)))

def actionImporter(actions, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import actions into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.actions", ruleset=cruleset.identifier)))
    try:
        for i, action in enumerate(actions):
            name = action["name"]
            time = action["time"]
            text = action["text"]
            
            if(len(name) < 1):
                flash(f"Action at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(time) > 127):
                flash(f"{name} time too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_action = Action(
                ruleset = cruleset,
                name = name,
                time = time,
                text = text
            )
            db.session.add(new_action)
        db.session.commit()
        flash("Actions imported!", "green")
        return(redirect(url_for("eprefs.actions", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importActions", ruleset=cruleset.identifier)))

def makeCondition(request, cruleset, condition, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} conditions in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.conditions", ruleset=cruleset.identifier)))
    elif(instruction == "duplicate"):
        new_condition = Condition(
            rulesetid = cruleset.id,
            name = f"{condition.name} Duplicate",
            text = condition.text
        )
        db.session.add(new_condition)
        db.session.commit()
        flash("Condition duplicated!", "green")
        return(redirect(url_for("eprefs.conditions", ruleset=cruleset.identifier)))
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a condition name.", "red")
        elif(len(name) > 127):
            flash("Condition name must be fewer than 128 characters.", "red")
        elif(len(text) > 16383):
            flash("Condition description must be fewer than 16384 characters", "red")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif(instruction == "create"):
            new_condition = Condition(
                rulesetid = cruleset.id,
                name = name,
                text = text
            )
            db.session.add(new_condition)
            db.session.commit()
            flash("Condition created!")
            return(redirect(url_for("eprefs.conditions", ruleset=cruleset.identifier)))
        else:
            condition.name = name
            condition.text = text
            db.session.commit()
            flash("Changes saved!")
            return(redirect(url_for("eprefs.conditions", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createCondition", ruleset=cruleset.identifier)))

def conditionImporter(conditions, cruleset, subtype):
    if(current_user.id != cruleset.userid):
        flash("You cannot import import conditions into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.conditions", ruleset=cruleset.identifier)))
    try:
        for i, condition in enumerate(conditions):
            name = condition["name"]
            text = condition["text"]
            if(len(name) < 1):
                flash(f"{subtype.capitalize()} at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 chatacters); skipping...", "orange")
                continue
            if(subtype == "condition"):
                new_condition = Condition(
                    ruleset = cruleset,
                    name = name,
                    text = text
                )
            elif(subtype == "disease"):
                new_condition = Disease(
                    ruleset = cruleset,
                    name = name,
                    text = text
                )
            else:
                new_condition = Status(
                    ruleset = cruleset,
                    name = name,
                    text = text
                )
            db.session.add(new_condition)
        db.session.commit()
        flash(f"{subtype.capitalize()} imported!", "green")
        return(redirect(url_for("eprefs.conditions", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importConditions", ruleset=cruleset.identifier)))

def makeDisease(request, cruleset, disease, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} diseases in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.diseases", ruleset=cruleset.identifier)))
    elif(instruction == "duplicate"):
        new_disease = Disease(
            rulesetid = cruleset.id,
            name = f"{disease.name} Duplicate",
            text = disease.text
        )
        db.session.add(new_disease)
        db.session.commit()
        flash("Disease duplicated!", "green")
        return(redirect(url_for("eprefs.diseases", ruleset=cruleset.identifier)))
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a disease name.", "red")
        elif(len(name) > 127):
            flash("Disease name must be fewer than 128 characters.", "red")
        elif(len(text) > 16383):
            flash("Disease description must be fewer than 16384 characters", "red")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif(instruction == "create"):
            new_disease = Disease(
                rulesetid = cruleset.id,
                name = name,
                text = text
            )
            db.session.add(new_disease)
            db.session.commit()
            flash("Disease created!")
            return(redirect(url_for("eprefs.diseases", ruleset=cruleset.identifier)))
        else:
            disease.name = name
            disease.text = text
            db.session.commit()
            flash("Changes saved!")
            return(redirect(url_for("eprefs.diseases", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createdisease", ruleset=cruleset.identifier)))

def makeStatus(request, cruleset, status, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} statuses in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.statuses", ruleset=cruleset.identifier)))
    elif(instruction == "duplicate"):
        new_status = Status(
            rulesetid = cruleset.id,
            name = f"{status.name} Duplicate",
            text = status.text
        )
        db.session.add(new_status)
        db.session.commit()
        flash("Status duplicated!", "green")
        return(redirect(url_for("eprefs.statuses", ruleset=cruleset.identifier)))
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a status name.", "red")
        elif(len(name) > 127):
            flash("Status name must be fewer than 128 characters.", "red")
        elif(len(text) > 16383):
            flash("Status description must be fewer than 16384 characters", "red")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif(instruction == "create"):
            new_status = Status(
                rulesetid = cruleset.id,
                name = name,
                text = text
            )
            db.session.add(new_status)
            db.session.commit()
            flash("Status created!")
            return(redirect(url_for("eprefs.statuses", ruleset=cruleset.identifier)))
        else:
            status.name = name
            status.text = text
            db.session.commit()
            flash("Changes saved!")
            return(redirect(url_for("eprefs.statuses", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createStatus", ruleset=cruleset.identifier)))

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
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif(len(name) > 127):
            flash("Tag name must be fewer than 128 characters.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif(len(text) > 16383):
            flash("Tag description must be fewer than 16384 characters.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
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
    return(redirect(url_for("eprefs.tags", ruleset=cruleset.identifier)))

def tagImporter(tags, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import item tags into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.tags", ruleset=cruleset.identifier)))
    try:
        for i, tag in enumerate(tags):
            name = tag["name"]
            text = tag["text"]
            if(len(name) < 1):
                flash(f"Tag at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_tag = ItemTag(
                ruleset = cruleset,
                name = name,
                text = text
            )
            db.session.add(new_tag)
        db.session.commit()
        flash("Tags imported!", "green")
        return(redirect(url_for("eprefs.tags", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importTags", ruleset=cruleset.identifier)))

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
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif(len(name) > 127):
            flash("Tag name must be fewer than 128 characters.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif(len(text) > 16383):
            flash("Tag description must be fewer than 16384 characters.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("eprefs.createTag", ruleset=cruleset.identifier)))
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
    return(redirect(url_for("eprefs.properties", ruleset=cruleset.identifier)))

def propertyImporter(properties, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import item properties into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.tags", ruleset=cruleset.identifier)))
    try:
        for i, itemproperty in enumerate(properties):
            name = itemproperty["name"]
            text = itemproperty["text"]
            if(len(name) < 1):
                flash(f"Property at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_property = Property(
                ruleset = cruleset,
                name = name,
                text = text
            )
            db.session.add(new_property)
        db.session.commit()
        flash("Properties imported!", "green")
        return(redirect(url_for("eprefs.properties", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importProperties", ruleset=cruleset.identifier)))

def makeItem(request, cruleset, item, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot ceeate skills for rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.items", ruleset=cruleset.identifier)))
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
        return(redirect(url_for("eprefs.items", ruleset=cruleset.identifier)))
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
        elif(instruction=="create"):
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
            db.session.commit()
            flash("Item created!", "green")
            return(redirect(url_for("eprefs.items", ruleset=cruleset.identifier)))
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
            db.session.commit()
            flash("Changes saved!", "green")
            return(redirect(url_for("eprefs.items", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createItem", ruleset=cruleset.identifier)))

def itemImporter(items, base, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import items into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.items", ruleset=cruleset.identifier)))
    try:
        for i, item in enumerate(items):
            name = item["name"]
            is_magical = item["is_magical"]
            rarity = item["rarity"]
            tier = item["tier"]
            attunement = item["attunement"]
            tags = item["tags"]
            proficiency = item["proficiency"]
            cost = item["cost"]
            weight = item["weight"]
            text = item["text"]
            images = item["images"]
            is_armor = item["is_armor"]
            stealth = item["stealth"]
            strength = item["strength"]
            armor_class = item["armor_class"]
            add_dex = item["add_dex"]
            is_weapon = item["is_weapon"]
            die_num = item["die_num"]
            damage_die = item["damage_die"]
            damage_types = item["damage_types"]
            weapon_properties = item["weapon_properties"]

            if(len(name) < 1):
                flash(f"Item at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(tags)) > 16384):
                flash(f"{name} has too many tags (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(images)) > 16384):
                flash(f"{name} has too many images (maximum raw data size of list of links 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(damage_types))):
                flash(f"{name} has too many damage types (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(weapon_properties))):
                flash(f"{name} has too many weapon properties (maximum raw data size 16KiB); skipping...", "orange")
                continue
            new_item = Item(
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
                images = images,
                is_armor = is_armor,
                stealth = stealth,
                strength = strength,
                armor_class = armor_class,
                add_dex = add_dex,
                is_weapon = is_weapon,
                die_num = die_num,
                damage_die = damage_die,
                damage_types = damage_types,
                weapon_properties = weapon_properties
            )
            db.session.add(new_item)

        db.session.commit()
        flash("Items Imported!", "green")
        return(redirect(url_for("eprefs.items", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importItems", ruleset=cruleset.identifier)))

def makeLanguage(request, cruleset, language, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create languages for rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.languages", ruleset=cruleset.identifier)))
    elif(instruction == "duplicate"):
        new_language = Language(
            rulesetid=cruleset.id,
            name=f"{language.name} Duplicate",
            text=language.text
        )
        db.session.add(new_language)
        db.session.commit()
        flash("Language duplicated!", "green")
        return(redirect(url_for("eprefs.languages", ruleset=cruleset.identifier)))
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a language name.", "red")
        elif(len(name) > 127):
            flash("Language name must be fewer than 128 characters.", "red")
        elif(len(text) > 16383):
            flash("Language description must be fewer than 16384 characters.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif("<" in text):
            flash("Open angle brackets(\"<\") are not allowed.", "red")
        elif(instruction == "edit"):
            language.name = name
            language.text = text
            db.session.commit()
            flash("Changes Saved!", "green")
            return(redirect(url_for("eprefs.languages", ruleset=cruleset.identifier)))
        else:
            new_language = Language(
                rulesetid = cruleset.id,
                name = name,
                text = text
            )
            db.session.add(new_language)
            db.session.commit()
            flash("Language created!", "green")
            return(redirect(url_for("eprefs.languages", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createLanguage", ruleset=cruleset.identifier)))

def languageImporter(languages, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import languages into rulesets that are not your own.", "red")
        return(redirect(url_for('eprefs.languages', ruleset=cruleset.identifier)))
    try:
        for i, language in enumerate(languages):
            name = language["name"]
            text = language["text"]
            if(len(name) < 1):
                flash(f"Language at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_language = Language(
                ruleset = cruleset,
                name = name,
                text = text
            )
            db.session.add(new_language)
        db.session.commit()
        flash("Languages Imported!", "green")
        return(redirect(url_for("eprefs.languages", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON.; unable to import.", "red")
        return(redirect(url_for("eprefs.importLanguages", ruleset=cruleset.identifier)))

def makeSpell(request, cruleset, spell, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} spells in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.spells", ruleset=cruleset.identifier)))
    elif(instruction == "duplicate"):
        new_spell = Spell(
            rulesetid = cruleset.userid,
            name = f"{spell.name} Duplicate",
            school = spell.school,
            level = spell.level,
            casting_time = spell.casting_time,
            spell_range = spell.spell_range,
            vebal = spell.verbal,
            somatic = spell.somatic,
            material = spell.material,
            material_specific = spell.material_specific,
            consumes_material = spell.consumes_material,
            concentration = spell.concentration,
            duration = spell.duration,
            text = spell.text
        )
        db.session.add(new_spell)
        db.session.commit()
        flash("Spell duplicated!", "green")
        return(redirect(url_for("eprefs.spells", ruleset=cruleset.identifier)))
    else:
        name = request.form.get("name")
        school = request.form.get("school")
        level = request.form.get("level")
        casting_time = request.form.get("time")
        spell_range = request.form.get("range")
        if(request.form.get("verbal")):
            verbal = True
        else:
            verbal = False
        if(request.form.get("somatic")):
            somatic = True
        else:
            somatic = False
        if(request.form.get("material")):
            material = True
            material_specific = request.form.get("material_specific")
            if(request.form.get("consumes_material")):
                consumes_material = True
            else:
                consumes_material = False
        else:
            material = False
            material_specific = None
            consumes_material = None
        concentration = request.form.get("concentration")
        duration = request.form.get("duration")
        text = request.form.get("text")
        if(len(name) > 127):
            flash("Spell name must be fewer than 127 characters.", "red")
        elif(len(name) < 1):
            flash("You must specify a spell name.", "red")
        elif(len(text) > 16383):
            flash("Spell description must be fewer than 16383 characters.", "red")
        elif(material):
            if(len(material_specific) > 255):
                flash("Spell material components must be fewer than 256 characters.", "red")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif(instruction == "create"):
            new_spell = Spell(
                rulesetid = cruleset.id,
                name = name,
                school = school,
                level = level,
                casting_time = casting_time,
                spell_range = spell_range,
                verbal = verbal,
                somatic = somatic,
                material = material,
                material_specific = material_specific,
                consumes_material = consumes_material,
                concentration = concentration,
                duration = duration,
                text = text
            )
            db.session.add(new_spell)
            db.session.commit()
            flash("Spell created!", "green")
            return(redirect(url_for("eprefs.spells", ruleset=cruleset.identifier)))
        else:
            spell.name = name
            spell.school = school
            spell.level = level
            spell.casting_time = casting_time
            spell.spell_range = spell_range
            spell.verbal = verbal
            spell.somatic = somatic
            spell.material = material
            spell.material_specific = material_specific
            spell.consumes_material = consumes_material
            spell.concentration = concentration
            spell.duration = duration
            spell.text = text
            db.session.commit()
            flash("Changes saved!", "green")
            return(redirect(url_for("eprefs.spells", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createSpell", ruleset=cruleset.identifier)))

def spellImporter(spells, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import spells into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.spells", ruleset=cruleset.identifier)))
    try:
        for i, spell in enumerate(spells):
            name = spell["name"]
            schools = spell["schools"]
            level = spell["levels"]
            casting_time = spell["casting_time"]
            spell_range = spell["spell_range"]
            verbal = spell["verbal"]
            somatic = spell["somatic"]
            material = spell["material"]
            material_specific = spell["material_specific"]
            consumes_material = spell["consumes_material"]
            concentration = spell["concentration"]
            duration = spell["duration"]
            text = spell["text"]
            if(len(name) < 1):
                flash(f"Spell at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(schools))):
                flash(f"{name} has too many spell schools (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(len(material_specific) > 255):
                flash(f"{name} spell material too long (maximum 255 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_spell = Spell(
                ruleset = cruleset,
                name = name,
                schools = schools,
                level = level,
                casting_time = casting_time,
                spell_range = spell_range,
                verbal = verbal,
                somatic = somatic,
                material = material,
                material_specific = material_specific,
                consumes_material = consumes_material,
                concentration = concentration,
                duration = duration,
                text = text
            )
            db.session.add(new_spell)
        db.session.commit()
        flash("Spells imported!", "green")
        return(redirect(url_for("eprefs.spells", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importSpells", ruleset=cruleset.identifier)))

def makeRecipe(request, cruleset, recipe, instruction):
    if(current_user.id != cruleset.id):
        flash(f"You cannot {instruction} recipes in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.recipes", ruleset=cruleset.identifier)))
    elif(instruction == "duplicate"):
        new_recipe = Recipe(
            rulesetid = cruleset.id,
            name = recipe.name,
            text = recipe.text
        )
        db.session.add(new_recipe)
        db.session.commit()
        flash("Recipe duplicated!", "green")
        return(redirect(url_for("eprefs.recipes", ruleset=cruleset.identifier)))
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        if(len(name) < 1):
            flash("You must specify a recipe name.", "red")
        elif(len(name) > 127):
            flash("Recipe name must be fewer than 127 characters.", "red")
        elif(len(text) > 16383):
            flash("Recipe text must be fewer than 16384 characters.", "red")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif(instruction == "create"):
            new_recipe = Recipe(
                rulesetid = cruleset.id,
                name = name,
                text = text
            )
            db.session.add(new_recipe)
            db.session.commit()
            flash("Recipe created!", "green")
            return(redirect(url_for("eprefs.recipes", ruleset=cruleset.identifier)))
        else:
            recipe.name = name
            recipe.text = text
            db.session.commit()
            flash("Changes saved!", "green")
            return(redirect(url_for("eprefs.recipes", ruleset=cruleset.identifier)))
        return(redirect(url_for("eprefs.createRecipe", ruleset=cruleset.identifier)))

def recipeImporter(recipes, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import recipes into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.recipes", ruleset=cruleset.identifier)))
    try:
        for i, recipe in enumerate(recipes):
            name = recipe["name"]
            text = recipe["text"]
            images = recipe["images"]
            if(len(name) < 1):
                flash(f"Recipe at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_recipe = Recipe(
                ruleset = cruleset,
                name = name,
                text = text,
                images = images
            )
            db.session.add(new_recipe)
        db.session.commit()
        flash("Recipes imported!", "green")
        return(redirect(url_for("eprefs.recipes", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importRecipes", ruleset=cruleset.identifier)))

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
            return(redirect(url_for("eprefs.createSkill", ruleset=cruleset.identifier)))
        elif(len(name) > 63):
            flash("Skill name must be fewer than 64 characters.", "red")
            return(redirect(url_for("eprefs.createSkill", ruleset=cruleset.identifier)))
        elif(len(description) > 16383):
            flash("Skill description must be fewer than 16384 characters.", "red")
            return(redirect(url_for("eprefs.createSkill", ruleset=cruleset.identifier)))
        elif("javascript" in description):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("eprefs.createSkill", ruleset=cruleset.identifier)))
        elif("<" in description):
            flash("Open angle brackets(\"<\") are not allowed.", "red")
            return(redirect(url_for("eprefs.createSkill", ruleset=cruleset.identifier)))
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
    return(redirect(url_for("eprefs.skills", ruleset=cruleset.identifier)))

def skillImporter(skills, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import skills into rulests that are not your own.", "red")
        return(redirect(url_for("eprefs.skills", ruleset=cruleset.identifier)))
    try:
        for i, skill in enumerate(skills):
            name = skill["name"]
            ability_score = skill["ability_score"]
            description = skill["description"]
            if(len(name) < 1):
                flash(f"Skill at index {i} has no name; skipping...", "orange")
                continue
            elif(len(ability_score) != 3):
                flash(f"{name} has improperly formatted ability score; skipping...", "orange")
                continue
            elif(len(description) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_skill = Skill(
                ruleset = cruleset,
                name = name,
                ability_score = ability_score,
                description = description
            )
            db.session.add(new_skill)
        db.session.commit()
        flash("Skills imported!", "green")
        return(redirect(url_for("eprefs.skills", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importSkills", ruleset=cruleset.identifier)))