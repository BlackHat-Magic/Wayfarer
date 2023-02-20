from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, jsonify, flash
from .models import Ruleset, Skill, Action, Condition, Item, ItemTag, Property, Language, Recipe, Spell
from flask_login import login_user, current_user, login_required
from .check_ruleset import *
from . import db
import json

eprefs = Blueprint('eprefs', __name__)

## QUICK REFERENCE
@eprefs.route("/")
def refs():
    return(redirect(url_for("epmain.home")))

@eprefs.route("/Actions")
def actions():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "actions.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            actions=actions, 
            adminrulesets=adminrulesets,
            title="Actions"
        )
    )

@eprefs.route("/Actions/Create", methods=["GET", "POST"])
@login_required
def createAction():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create actions for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            time = request.form.get("time")
            if(len(name) < 1):
                flash("You must specify an action name.")
            elif(len(name) > 127):
                flash("Action name must be fewer than 128 characters.")
            elif(len(time) > 127):
                flash("Action time must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Action text must be fewer than 16383 characters")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_action = Action(
                    rulesetid = cruleset.id,
                    name = name,
                    time = time,
                    text = text
                )
                db.session.add(new_action)
                db.session.commit()
                flash("Action created!")
                return(redirect(url_for("eprefs.actions")))
    return(
        render_template(
            "create-action.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Action"
        )
    )

@eprefs.route("/Conditions")
def conditions():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    conditions = []
    for condition in Condition.query.filter_by(rulesetid = cruleset.id):
        conditions.append(condition)
    return(
        render_template(
            "conditions.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            conditions=conditions, 
            adminrulesets=adminrulesets,
            title="Conditions"
        )
    )

@eprefs.route("/Conditions/Create", methods=["GET", "POST"])
@login_required
def createCondition():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create conditions for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            if(len(name) < 1):
                flash("You must specify an action name.")
            elif(len(name) > 127):
                flash("Action name must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Action text must be fewer than 16383 characters")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_action = Condition(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_action)
                db.session.commit()
                flash("Condition created!")
                return(redirect(url_for("eprefs.conditions")))
    return(
        render_template(
            "create-condition.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Condition"
        )
    )

@eprefs.route("/Items")
def items():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "items.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Items"
        )
    )

@eprefs.route("/Items/Create", methods=["GET", "POST"])
@login_required
def createItem():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create items for rulesets that are not yours.")
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
            is_armor = request.form.get("isarmorr")
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
                flash("You must specify an item name.")
            elif(len(name) > 127):
                flash("Item name must be fewer than 128 characters.")
            elif(len(cost) > 31):
                flash("Item cost must be fewer than 32 characters.")
            elif(len(tags) > 127):
                flash("Too many item tags specified (sorry).")
            elif(len(text) > 16383):
                flash("Item text must be fewer than 16384 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            elif(len(weapon_properties) > 255):
                flash("Weapon Properties must be fewer than 256 characters.")
            else:
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
                flash("Item created.")
                return(redirect(url_for("eprefs.items")))
    return(
        render_template(
            "create-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item"
        )
    )

@eprefs.route("/Item/<string:item>")
def item(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    item = Item.query.filter_by(rulesetid = cruleset.id, name=item.replace("-", " ")).first()
    return(
        render_template(
            "item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            item=item, 
            adminrulesets=adminrulesets,
            title=item.name
        )
    )

@eprefs.route("/Item/<string:item>/Delete")
@login_required
def deleteItem(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(current_user.id != cruleset.userid):
        flash("You cannot delete items from rulesets that are not yours.")
    else:
        db.session.delete(Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first())
        db.session.commit()
        flash("Item deleted.")
    return(redirect(url_for("eprefs.items")))

@eprefs.route("/Items/Tags")
def tags():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tags = ItemTag.query.filter_by(rulesetid=cruleset.id).order_by(ItemTag.name)
    return(
        render_template(
            "tags.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            tags=tags, 
            adminrulesets=adminrulesets,
            title="Item Types"
        )
    )

@eprefs.route("/Items/Tags/Create", methods=["GET", "POST"]) 
@login_required
def createTag():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create item tags for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            if(len(name) < 1):
                flash("You must specify a tag name.")
            elif(len(name) > 127):
                flash("Tag name must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Tag description must be fewer than 16384 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_tag = ItemTag(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_tag)
                db.session.commit()
                flash("Item tag created!")
                return(redirect(url_for("eprefs.tags")))
    return(
        render_template(
            "create-tag.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create Item Type"
        )
    )

@eprefs.route("/Items/Properties")
def properties():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    properties = Property.query.filter_by(rulesetid = cruleset.id).order_by(Property.name)
    return(
        render_template(
            "properties.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            properties=properties, 
            adminrulesets=adminrulesets,
            title="Weapon Properties"
        )
    )

@eprefs.route("/Items/Properties/Create", methods=["GET", "POST"])
def createProperty():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create weapon properties for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            if(len(name) < 1):
                flash("You must specify a property name.")
            elif(len(name) > 127):
                flash("Property name must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Property description must be fewer than 16384 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_tag = Property(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_tag)
                db.session.commit()
                flash("Weapon property created!")
                return(redirect(url_for("eprefs.properties")))
    return(
        render_template(
            "create-property.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create Weapon Properties"
        )
    )

@eprefs.route("/Languages")
def refsLang():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "languages.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Languages"
        )
    )

@eprefs.route("/Languages/Create", methods=["GET", "POST"])
@login_required
def createLanguage():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create languages for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            if(len(name) < 1):
                flash("You must specify a language name.")
            elif(len(name) > 127):
                flash("Language name must be fewer than 128 characters.")
            elif(len(text) > 16383):
                flash("Language description must be fewer than 16384 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_language = Language(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_language)
                db.session.commit()
                flash("Language created!")
                return(redirect(url_for("eprefs.refsLang")))
    return(
        render_template(
            "create-language.html", 
            user=current_user, 
            cruleset=cruleset, 
            frulesets=frulesets, 
            adminrulesets=adminrulesets,
            title="Create a Language"
        )
    )

@eprefs.route("/Spells")
def spells():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "spells.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Spells"
        )
    )

@eprefs.route("/Spells/Create", methods=["GET", "POST"])
@login_required
def createSpell():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create spells for rulesets that are not yours.")
        else:
            rulesetid = cruleset.id
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
                verbal = False
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
                flash("Spell name must be fewer than 127 characters.")
            elif(len(name) < 1):
                flash("You must specify a spell name.")
            elif(len(text) > 16383):
                flash("Spell description must be fewer than 16383 characters.")
            elif(material):
                if(len(material_specific) > 255):
                    flash("Spell material components must be fewer than 256 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_spell = Spell(
                    rulesetid = rulesetid,
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
                flash("Spell created.")
                return(redirect(url_for("eprefs.spells")))
    return(
        render_template(
            "create-spell.html", 
            user=current_user, 
            cruleset=cruleset, 
            frulesets=frulesets, 
            adminrulesets=adminrulesets,
            title="Create a Spell"
        )
    )

@eprefs.route("/Spell/<string:spell>")
def spell(spell):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    spell = Spell.query.filter_by(rulesetid = cruleset.id, name = spell.replace("-", " ")).first()
    return(
        render_template(
            "spell.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            spell=spell, 
            adminrulesets=adminrulesets,
            title=spell.name
        )
    )


@eprefs.route("/Recipes")
def recipes():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "recipes.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Recipes"
        )
    )

@eprefs.route("/Recipes/Create", methods=["GET", "POST"])
@login_required
def createRecipe():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create recipes for rulesets that are not yours.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            if(len(name) < 1):
                flash("You must specify a recipe name.")
            elif(len(name) > 127):
                flash("Recipe name must be fewer than 127 characters.")
            elif(len(text) > 16383):
                flash("Recipe text must be fewer than 16384 characters.")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            else:
                new_recipe = Recipe(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_recipe)
                db.session.commit()
                flash("Recipe created!")
                return(redirect(url_for("eprefs.recipes")))
    return(
        render_template(
            "create-recipe.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Recipe"
        )
    )

@eprefs.route("/Skills")
def skills():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "skills.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Skills"
        )
    )

@eprefs.route("/Skills/Create", methods=["GET", "POST"])
@login_required
def createSkill():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot create a skill for a ruleset that is not your own.")
        else:
            name = request.form.get("name")
            text = request.form.get("text")
            ability = request.form.get("ability")
            if(ability == ""):
                ability = "STR"
            if(len(name) < 1):
                flash("You must specify a skill name.")
            elif(len(name) > 63):
                flash("Skill name must be fewer than 64 characters.")
            elif(len(text) > 16383):
                flash("Skill description must be fewer than 16384 characters.")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.")
            elif("<" in text):
                flash("Open angle brackets(\"<\") are not allowed.")
            else:
                new_skill = Skill(
                    rulesetid = cruleset.id,
                    name = name,
                    ability_score = ability,
                    description = text
                )
                db.session.add(new_skill)
                db.session.commit()
                flash("Skill created!")
                return(redirect(url_for("eprefs.skills")))
    return(
        render_template(
            "create-skill.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Skill"
        )
    )

@eprefs.route("/Skills/Delete/<int:rid>")
@login_required
def deleteSkill(rid):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(current_user.id != cruleset.userid):
        flash("You cannod delete skills from rulesets that are not your own.")
        return(redirect(url_for("eprefs.skills")))
    else:
        skill = Skill.query.filter_by(id=rid, rulesetid = cruleset.id).first()
        db.session.delete(skill)
        db.session.commit()
        flash("Skill deleted.")
        return(redirect(url_for("eprefs.skills")))
