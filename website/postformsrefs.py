from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .models import Skill, ItemTag, Property, Language, Item, Action, Condition, Disease, Status

def makeAction(request, cruleset, action, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} actions in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.actions")))
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
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
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
            return(redirect(url_for("eprefs.actions")))
        else:
            action.name = name
            action.time = time
            action.text = text
            db.session.commit()
            flash("Changes saved!", "green")
            return(redirect(url_for("eprefs.actions")))
        return(redirect(url_for("eprefs.createAction")))

def actionImporter(actions, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import actions into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.actions")))
    try:
        for action in actions["action"]:
            name = action["name"]
            print(name)
            if("time" in action.keys()):
                if(type(action["time"][0]) == dict):
                    time = f"{str(action['time'][0]['number'])} {action['time'][0]['unit'].casefold().capitalize()}"
                elif(type(action["time"][0]) == str):
                    time = action["time"][0]
            else:
                time = "Other"
            text = ""
            for entry in action["entries"]:
                if(type(entry) == str):
                    text += f"{entry}\n\n"
                else:
                    text += f"### {entry['name']}\n\n"
                    for section in entry["entries"]:
                        text += f"{section}\n\n"
            new_action = Action(
                rulesetid = cruleset.id,
                name = name,
                time = time,
                text = text
            )
            db.session.add(new_action)
        db.session.commit()
        flash("Actions imported!", "green")
        return(redirect(url_for("eprefs.actions")))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importActions")))

def makeCondition(request, cruleset, condition, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} conditions in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.conditions")))
    elif(instruction == "duplicate"):
        new_condition = Condition(
            rulesetid = cruleset.id,
            name = f"{condition.name} Duplicate",
            text = condition.text
        )
        db.session.add(new_condition)
        db.session.commit()
        flash("Condition duplicated!", "green")
        return(redirect(url_for("eprefs.conditions")))
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
            return(redirect(url_for("eprefs.conditions")))
        else:
            condition.name = name
            condition.text = text
            db.session.commit()
            flash("Changes saved!")
            return(redirect(url_for("eprefs.conditions")))
        return(redirect(url_for("eprefs.createCondition")))

def makeDisease(request, cruleset, disease, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} diseases in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.diseases")))
    elif(instruction == "duplicate"):
        new_disease = Disease(
            rulesetid = cruleset.id,
            name = f"{disease.name} Duplicate",
            text = disease.text
        )
        db.session.add(new_disease)
        db.session.commit()
        flash("Disease duplicated!", "green")
        return(redirect(url_for("eprefs.diseases")))
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
            return(redirect(url_for("eprefs.diseases")))
        else:
            disease.name = name
            disease.text = text
            db.session.commit()
            flash("Changes saved!")
            return(redirect(url_for("eprefs.diseases")))
        return(redirect(url_for("eprefs.createdisease")))

def makeStatus(request, cruleset, status, instruction):
    if(current_user.id != cruleset.userid):
        flash(f"You cannot {instruction} statuses in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.statuses")))
    elif(instruction == "duplicate"):
        new_status = Status(
            rulesetid = cruleset.id,
            name = f"{status.name} Duplicate",
            text = status.text
        )
        db.session.add(new_status)
        db.session.commit()
        flash("Status duplicated!", "green")
        return(redirect(url_for("eprefs.statuses")))
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
            return(redirect(url_for("eprefs.statuses")))
        else:
            status.name = name
            status.text = text
            db.session.commit()
            flash("Changes saved!")
            return(redirect(url_for("eprefs.statuses")))
        return(redirect(url_for("eprefs.createStatus")))

def conditionImporter(conditions, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import import conditions into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.conditions")))
    # try:
    if("condition" in conditions.keys()):
        for condition in conditions["condition"]:
            text = ""
            for entry in condition["entries"]:
                if(type(entry) == str):
                    text += f"{entry}\n\n"
                elif(entry["type"] == "list"):
                    for item in entry["items"]:
                        text += f" - {item}\n"
                    text += "\n"
                elif(entry["type"] == "table"):
                    text += "| "
                    for label in entry["colLabels"]:
                        text += f"{label} | "
                    text += "\n| "
                    for style in entry["colStyles"]:
                        if("center" or "left" in style):
                            text += ":"
                        text += "---"
                        if("center" or "right" in style):
                            text += ":"
                        text += " | "
                    for row in entry["rows"]:
                        text += "\n| "
                        for column in row:
                            text += str(column)
                            text += " | "

            new_condition = Condition(
                rulesetid = cruleset.id,
                name = condition["name"],
                text = text
            )
            db.session.add(new_condition)
    if("disease" in conditions.keys()):
        for disease in conditions["disease"]:
            text = ""
            for entry in disease["entries"]:
                if(type(entry) == str):
                    text += f"{entry}\n\n"
                elif(entry["type"] == "list"):
                    for item in entry["items"]:
                        text += f" - {item}\n"
                    text += "\n"
                elif(entry["type"] == "table"):
                    text += "| "
                    for label in entry["colLabels"]:
                        text += f"{label} | "
                    text += "\n| "
                    for style in entry["colStyles"]:
                        if("center" or "left" in style):
                            text += ":"
                        text += "---"
                        if("center" or "right" in style):
                            text += ":"
                        text += " | "
                    for row in entry["rows"]:
                        text += "\n| "
                        for column in row:
                            text += str(column)
                            text += " | "
                        text += "\n"

            new_disease = Disease(
                rulesetid = cruleset.id,
                name = disease["name"],
                text = text
            )
            db.session.add(new_disease)
    if("status" in conditions.keys()):
        for status in conditions["status"]:
            text = ""
            for entry in status["entries"]:
                if(type(entry) == str):
                    text += f"{entry}\n\n"
                elif(entry["type"] == "list"):
                    for item in entry["items"]:
                        text += f" - {item}\n"
                    text += "\n"
                elif(entry["type"] == "table"):
                    text += "| "
                    for label in entry["colLabels"]:
                        text += f"{label} | "
                    text += "\n| "
                    for style in entry["colStyles"]:
                        if("center" or "left" in style):
                            text += ":"
                        text += "---"
                        if("center" or "right" in style):
                            text += ":"
                        text += " | "
                    for row in entry["rows"]:
                        text += "\n| "
                        for column in row:
                            text += str(column)
                            text += " | "
                        text += "\n"

            new_status = Status(
                rulesetid = cruleset.id,
                name = status["name"],
                text = text
            )
            db.session.add(new_status)
    db.session.commit()
    flash("Conditions imported!", "green")
    return(redirect(url_for("eprefs.conditions")))
    # except:
    #     flash("Improperly formatted JSON; could not import.", "red")
    #     return(redirect(url_for("eprefs.importConditions")))

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

def itemImporter(items, base, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import items into rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.items")))
    try:
        for properties in base["itemProperty"]:
            if("entries" in properties.keys()):
                description = ""
                for entry in properties["entries"][0]["entries"]:
                    description += f"{entry}\n\n"
                new_property = Property(
                    rulesetid = cruleset.id,
                    name = properties["entries"][0]["name"].casefold().capitalize(),
                    text = description
                )
            else:
                new_property = Property(
                    rulesetid = cruleset.id,
                    name = properties["name"].casefold().capitalize(),
                    text = None
                )
            db.session.add(new_property)
        for types in base["itemType"]:
            description = ""
            if("name" in types.keys()):
                name = types["name"]
                for entry in types["entries"]:
                    if(type(entry) == str):
                        description += f"{entry}\n\n"
                    else:
                        description += f"## {entry['name']}\n\n---\n\n"
                        for paragraph in entry:
                            description += f"{paragraph}\n\n"
            else:
                name = types["entries"][0]["name"]
                for entry in types["entries"][0]["entries"]:
                    if(type(entry) == str):
                        description += f"{entry}\n\n"
                    else:
                        for paragraph in entries:
                            description += f"## {paragraph['name']}\n\n---\n\n"
                            for line in paragraph["entries"]:
                                description += f"{line}\n\n"
            new_property = ItemTag(
                rulesetid = cruleset.id,
                name = name,
                text = description
            )
            db.session.add(new_property)
        for item in base["baseitem"]:
            proficiency = False
            if(item["rarity"] != "none"):
                is_magical = True
                rarity = item["rarity"].casefold().capitalize()
            else:
                is_magical = False
                rarity = None
            tags = []
            if("type" in item.keys()):
                for types in base["itemType"]:
                    if(types["abbreviation"] == item["type"] or (type(item["type"] == list) and types["abbreviation"] in item["type"])):
                        if("name" in types.keys()):
                            tags.append(types["name"].casefold().capitalize())
                        else:
                            tags.append(types["entries"][0]["name"])
            if("weaponCategory" in item.keys()):
                tags.append(item["weaponCategory"].casefold().capitalize())
            if("weapon" in item.keys() or "armor" in item.keys()):
                proficiency = is_weapon = True
            else:
                is_weapon = False
            if("value" in item.keys()):
                cost = item["value"]
            else:
                cost = None
            text = ""
            if("entries" in item.keys()):
                for entry in item["entries"]:
                    if(type(entry) == str):
                        text += f"{entry}\n\n"
                    else:
                        for paragraph in entry["entries"]:
                            text += f"***{entry['name']}.*** {paragraph}\n\n"
            if("armor" in item.keys()):
                is_armor = True
                armor_class = item["ac"]
                proficiency = True
                if(item["type"] == "LA"):
                    tags.append("Light Armor")
                    add_dex = True
                    max_dex = 0
                elif(item["type"] == "MA"):
                    tags.append("Medium Armor")
                    add_dex = True
                    max_dex = 2
                else:
                    tags.append("Heavy Armor")
                    add_dex = False
                    max_dex = None
            else:
                is_armor = False
                armor_class = None
                add_dex = None
                max_dex = None
            dmg_dict = {
                "N": "Necrotic",
                "S": "Slashing",
                "B": "Bludgeoning",
                "A": "Acid",
                "C": "Cold",
                "R": "Radiant",
                "L": "Lightning",
                "T": "Thunder",
                "P": "Piercing"
            }
            # Piercing, Poison, Psychic, Fire, Force
            die_num = damage_die = damage_type = None
            if("weapon" in item.keys()):
                is_weapon = True
                if("dmg1" in item.keys()):
                    die_num, damage_die = item["dmg1"].split("d")[0], item["dmg1"].split("d")[-1]
                    damage_type = dmg_dict[item["dmgType"]]
            else:
                is_weapon = False
            weapon_properties = []
            if("property" in item.keys()):
                for properties in base["itemProperty"]:
                    if(properties["abbreviation"] == item["property"] or (type(item["property"] == list) and properties["abbreviation"] in item["property"])):
                        if("name" in properties.keys()):
                            weapon_properties.append(properties["name"].casefold().capitalize())
                        else:
                            weapon_properties.append(properties["entries"][0]["name"].casefold().capitalize())
            if("weight" in item.keys()):
                weight = item["weight"]
            else:
                weight = None
            new_item = Item(
                rulesetid = cruleset.id,
                name = item["name"],
                is_magical = is_magical,
                rarity = rarity,
                tier = None,
                attunement = None,
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
        for item in items["item"]:
            is_magical = False
            rarity = tier = None
            attunement = False
            text = ""
            if("rarity" in item.keys()):
                is_magical = True
                rarity = item["rarity"].casefold().capitalize()
            if("tier" in item.keys()):
                is_magical = True
                tier = item["tier"].casefold().capitalize()
            if("reqAttune" in item.keys()):
                attunement = True
                if(item["reqAttune"] != "true" and type(item["reqAttune"]) != bool):
                    text += f"Requires attunement {item['reqAttune']}\n\n" 
            tags = []
            if("type" in item.keys()):
                for types in base["itemType"]:
                    if(types["abbreviation"] == item["type"] or (type(item["type"] == list) and types["abbreviation"] in item["type"])):
                        if("name" in types.keys()):
                            tags.append(types["name"])
                        else:
                            tags.append(types["entries"][0]["name"])
            proficiency = False
            if("value" in item.keys()):
                cost = item["value"]
            else:
                cost = None
            is_armor = False
            armor_class = add_dex = max_dex = None
            is_weapon = False
            die_num = damage_die = damage_type = weapon_properties = None
            if("weight" in item.keys()):
                weight = item["weight"]
            elif("baseItem" in item.keys()):
                for sitem in base["baseitem"]:
                    if(sitem["name"] == item["baseItem"] and "weight" in sitem.keys()):
                        weight = sitem["weight"]
                        if("ac" in sitem.keys()):
                            is_armor = True
                            armor_class = sitem["ac"]
                            if(sitem["type"] == "LA"):
                                add_dex = True
                                max_dex = 0
                            elif(sitem["type"] == "MA"):
                                add_dex = True
                                max_dex = 2
                            else:
                                add_dex = False
                        elif("weapon" in sitem.keys()):
                            is_weapon = True
                            die_num, damage_die = sitem["dmg1"].split("d")
                            weapon_properties = []
                            if("property" in sitem.keys()):
                                for properties in base["itemProperty"]:
                                    if(properties["abbreviation"] == sitem["property"] or (type(sitem["property"] == list) and properties["abbreviation"] in sitem["property"])):
                                        weapon_properties.append(properties["name"].casefold().capitalize())
            else:
                weight = None
            if("entries" in item.keys()):
                for entry in item["entries"]:
                    if(type(entry) == str):
                        if("#itemEntry" in entry):
                            newtext = ""
                            for group in items["itemGroup"]:
                                if(group["name"] == entry.split(" ")[1].split("|")[0]):
                                    for section in group["entries"]:
                                        if(type(section) == str):
                                            newtext += f"{section}\n\n"
                                        elif(type(section) == dict):
                                            if(section["type"] == "table"):
                                                newtext += f"###### {section['caption']}\n\n"
                                                newtext += "| "
                                                for label in section["colLabels"]:
                                                    newtext += f"{label} | "
                                                newtext += "\n| "
                                                for style in section["colStyles"]:
                                                    if("center" or "left" in style):
                                                        newtext += ":"
                                                    for i in range(style.split(" ")[0].split("-")[1]):
                                                        newtext += "-"
                                                    if("center" or "right" in style):
                                                        newtext += ":"
                                                    newtext += " | "
                                                for row in section["rows"]:
                                                    newtext += "\n| "
                                                    for column in row:
                                                        newtext += str(column)
                                                        newtext += " | "
                                                    newtext += "\n"
                            text = f"{newtext}\n\n{text}"
                        else:
                            text += f"{entry}\n\n"
                    elif(type(entry) == dict):
                        if(entry["type"] == "table"):
                            if("caption" in entry.keys()):
                                text += f"###### {entry['caption']}\n\n"
                            text += "| "
                            for label in entry["colLabels"]:
                                text += f"{label} | "
                            text += "\n| "
                            for style in entry["colStyles"]:
                                if("center" or "left" in style):
                                    text += ":"
                                text += "---"
                                if("center" or "right" in style):
                                    text += ":"
                                text += " | "
                            for row in entry["rows"]:
                                text += "\n| "
                                for column in row:
                                    text += str(column)
                                    text += " | "
                        text += "\n"

            new_item = Item(
                rulesetid = cruleset.id,
                name = item["name"],
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
        flash("Items Imported!", "green")
        return(redirect(url_for("eprefs.items")))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importItems")))

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

def languageImporter(languages, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import languages into rulesets that are not your own.", "red")
        return(redirect(url_for('eprefs.languages')))
    try:
        for language in languages["language"]:
            print(language['name'])
            text = ""
            if("type" in language.keys()):
                text += f"***Type.*** {language['type'].casefold().capitalize()}\n\n"
            if("typicalSpeakers" in language.keys()):
                speakers = ""
                for speaker in language['typicalSpeakers']:
                    if(len(speakers) > 0):
                        speakers += ", "
                    speakers += speaker.casefold().capitalize()
                text += f"***Typical Speakers.*** {speakers}\n\n"
            if("script" in language.keys()):
                text += f"***Script.*** {language['script'].casefold().capitalize()}\n\n"
            if("entries" in language.keys()):
                for entry in language["entries"]:
                    if(type(entry) == str):
                        text += f"{entry}\n\n"
                    elif(type(entry) == dict):
                        text += f"### {entry['name']}\n\n"
                        for paragraph in entry["entries"]:
                            text += f"{paragraph}\n\n"
            new_language = Language(
                rulesetid = cruleset.id,
                name = language["name"],
                text = text
            )
            db.session.add(new_language)
        db.session.commit()
        flash("Languages Imported!", "green")
        return(redirect(url_for("eprefs.languages")))
    except:
        flash("Improperly formatted JSON.; unable to import.", "red")
        return(redirect(url_for("eprefs.importLanguages")))

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

def skillImporter(skills, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import skills into rulests that are not your own.", "red")
        return(redirect(url_for("eprefs.skills")))
    asidict = {
        "Acrobatics": "dex",
        "Animal Handling": "wis",
        "Arcana": "int",
        "Athletics": "str",
        "Deception": "cha",
        "History": "int",
        "Insight": "wis",
        "Intimidation": "cha",
        "Investigation": "int",
        "Medicine": "wis",
        "Nature": "int",
        "Perception": "wis",
        "Performance": "cha",
        "Persuasion": "cha",
        "Religion": "int",
        "Sleight of Hand": "dex",
        "Stealth": "dex",
        "Survival": "wis"
    }
    try:
        for skill in skills["skill"]:
            if(skill["name"] in asidict.keys()):
                ability_score = asidict[skill["name"]]
            else:
                ability_score = None
            description = ""
            for entry in skill["entries"]:
                if(type(entry) == str):
                    description += f"{entry}\n\n"
                elif(type(entry) == dict and entry["type"] == "list"):
                    for item in entry["items"]:
                        description += f" - {item}\n"
                else:
                    flash(f"Unrecognized element of {skill['name']}'s description; skipping...", "orange")
            new_skill = Skill(
                rulesetid = cruleset.id,
                name = skill["name"],
                ability_score = ability_score,
                description = description
            )
            db.session.add(new_skill)
        db.session.commit()
        flash("Skills imported!", "green")
        return(redirect(url_for("eprefs.skills")))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("eprefs.importSkills")))