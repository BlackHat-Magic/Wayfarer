from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, jsonify, flash
from .models import Ruleset, Skill, Action, Condition, Item, ItemTag, Property, Language, Recipe, Spell
from flask_login import login_user, current_user, login_required
from .check_ruleset import *
from .postformsrefs import *
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
            else:
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
                flash("You must specify an action name.", "red")
            elif(len(name) > 127):
                flash("Action name must be fewer than 128 characters.", "red")
            elif(len(text) > 16383):
                flash("Action text must be fewer than 16383 characters", "red")
            elif("<" in text):
                flash("Open angle brackets (\"<\") are not allowed.", "red")
            elif("javascript" in text):
                flash("Cross-site scripting attacks are not allowed.", "red")
            else:
                new_action = Condition(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_action)
                db.session.commit()
                flash("Condition created!", "green")
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
    items = Item.query.filter_by(rulesetid = cruleset.id).order_by(Item.name)
    return(
        render_template(
            "items.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Items",
            items = items
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
            flash("You cannot create items for rulesets that are not yours.", "red")
        else:
            result = makeItem(request, cruleset, None, "create")
            if(result):
                return(result)
    tags = ItemTag.query.filter_by(rulesetid = cruleset.id).order_by(ItemTag.name)
    properties = Property.query.filter_by(rulesetid = cruleset.id).order_by(Property.name)
    return(
        render_template(
            "create-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            tags = tags,
            properties = properties
        )
    )

@eprefs.route("/Items/Duplicate/<string:item>")
@login_required
def duplicateItem(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    item = Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first()
    if(current_user.id != cruleset.userid):
        flash("You cannot duplicate items in rulesets that are not yours.", "red")
    else:
        result = makeItem(request, cruleset, item, "duplicate")
        if(result):
            return(result)
    return(
        render_template(
            "create-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            item=item
        )
    )

@eprefs.route("/Items/Edit/<string:item>", methods=["GET", "POST"])
@login_required
def editItem(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    item = Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first()
    if(request.method == "POST"):
        if(current_user.id != cruleset.userid):
            flash("You cannot edit items in rulesets that are not yours.", "red")
        else:
            result = makeItem(request, cruleset, item, "edit")
            if(result):
                return(result)
    tags = ItemTag.query.filter_by(rulesetid = cruleset.id).order_by(ItemTag.name)
    properties = Property.query.filter_by(rulesetid = cruleset.id).order_by(Property.name)
    return(
        render_template(
            "create-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            item=item,
            tags = tags,
            properties = properties
        )
    )

@eprefs.route("/Items/Delete/<string:item>")
@login_required
def deleteItem(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(current_user.id != cruleset.userid):
        flash("You cannot delete items from rulesets that are not yours.", "red")
    else:
        db.session.delete(Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first())
        db.session.commit()
        flash("Item deleted.", "orange")
    return(redirect(url_for("eprefs.items")))

@eprefs.route("/Items/Import", methods=["GET", "POST"])
@login_required
def importItems():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method=="POST"):
        # try:
        items = json.loads(request.form.get("parsed_item"))
        base = json.loads(request.form.get("parsed_base"))
        return(itemImporter(items, base, cruleset))
        # except:
        #     flash("Both JSON files are required", "red")
    return(
        render_template(
            "import-items.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Items"
        )
    )

@eprefs.route("/Item/<string:item>")
def item(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    item = Item.query.filter_by(rulesetid = cruleset.id, name=item).first()
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
        return(itemTag(request, cruleset, None, "create"))
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

@eprefs.route("/Items/Tags/Duplicate/<string:item>")
@login_required
def duplicateTag(item):
    cruleset = getCurrentRuleset(current_user)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first()
    if(not tag):
        flash("Tag does not exist", "red")
    return(itemTag(None, cruleset, tag, "duplicate"))

@eprefs.route("/Items/Tags/Edit/<string:item>", methods=["GET", "POST"]) 
@login_required
def editTag(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first()
    if(not tag):
        flash("Tag does not exist", "red")
        return(redirect(url_for("eprefs.tags")))
    elif(request.method == "POST"):
        return(itemTag(request, cruleset, tag, "edit"))
    return(
        render_template(
            "create-tag.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {tag.name}",
            tag=tag
        )
    )

@eprefs.route("/Items/Tags/Delete/<string:item>")
@login_required
def deleteTag(item):
    cruleset = getCurrentRuleset(current_user)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete item tags in rulesets that are not your own.", "red")
    elif(not tag):
        flash("Item tag does not exist", "red")
    else:
        db.session.delete(tag)
        db.session.commit()
        flash("Item deleted.", "orange")
    return(redirect(url_for("eprefs.tags")))

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
@login_required
def createProperty():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        return(itemProperty(request, cruleset, None, "create"))
    return(
        render_template(
            "create-property.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create Weapon Property"
        )
    )

@eprefs.route("/Items/Properties/Duplicate/<string:item>")
@login_required
def duplicateProperty(item):
    cruleset = getCurrentRuleset(current_user)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first()
    if(not tproperty):
        flash("Item property does not exist", "red")
        return(redirect(url_for("eprefs.properties")))
    return(itemProperty(None, cruleset, tproperty, "duplicate"))

@eprefs.route("/Items/Properties/Edit/<string:item>", methods=["GET", "POST"])
@login_required
def editProperty(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first()
    if(not tproperty):
        flash("Item property does not exist", "red")
        return(redirect(url_for("eprefs.refslang")))
    elif(request.method == "POST"):
        return(itemProperty(request, cruleset, None, "create"))
    return(
        render_template(
            "create-property.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {tproperty.name}",
            tproperty=tproperty
        )
    )

@eprefs.route("/Items/Properties/Delete/<string:item>")
@login_required
def deleteProperty(item):
    cruleset = getCurrentRuleset(current_user)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first()
    if(not tproperty):
        flash("Item property does not exist.", "red")
    elif(current_user.id != cruleset.userid):
        flash("You cannot delete item properties in rulesets that are not your own.")
    else:
        db.session.delete(tproperty)
        db.session.commit()
        flash("Item property deleted.", "orange")
    return(redirect(url_for("eprefs.properties")))

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
        return(makeLanguage(request, cruleset, None, "create"))
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

@eprefs.route("/Languages/Duplicate/<string:tlanguage>")
@login_required
def duplicateLanguage(tlanguage):
    cruleset = getCurrentRuleset(current_user)
    tlanguage = Language.query.filter_by(rulesetid=cruleset.id, name=tlanguage).first()
    if(cruleset.userid != current_user.id):
        flash("You cannot create languages for rulesets that are not your own.", "red")
    elif(not tlanguage):
        flash("Language does not exist.")
    else:
        return(makeLanguage(None, cruleset, tlanguage, "duplicate"))
    return(redirect(url_for("eprefs.refsLang")))

@eprefs.route("/Languages/Edit/<string:tlanguage>", methods=["GET", "POST"])
@login_required
def editLanguage(tlanguage):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tlanguage = Language.query.filter_by(rulesetid=cruleset.id, name=tlanguage).first()
    if(not tlanguage):
        flash("Language does not exist.", "red")
        return(redirect(url_for("eprefs.refsLang")))
    elif(request.method == "POST"):
        return(makeLanguage(request, cruleset, tlanguage, "edit"))
    return(
        render_template(
            "create-language.html",
            user=current_user, 
            cruleset=cruleset, 
            frulesets=frulesets, 
            adminrulesets=adminrulesets,
            title=f"Edit {tlanguage.name}",
            tlanguage=tlanguage
        )
    )

@eprefs.route("/Languages/Delete/<string:tlanguage>")
@login_required
def deleteLanguage(tlanguage):
    cruleset = getCurrentRuleset(current_user)
    tlanguage = Language.query.filter_by(rulesetid=cruleset.id, name=tlanguage).first()
    if(not language):
        flash("Language does not exist.", "red")
    elif(current_user.id != cruleset.userid):
        flash("You cannot delete languages in rulesets that are not your own.", "red")
    else:
        db.session.delete(tlanguage)
        db.session.commit()
        flash("Language deleted.", "orange")
    return(redirect(url_for("eprefs.refsLang")))
    

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
            flash("You cannot create spells for rulesets that are not yours.", "red")
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
                flash("Spell created.", "green")
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
    spell = Spell.query.filter_by(rulesetid = cruleset.id, name = spell).first()
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
            flash("You cannot create recipes for rulesets that are not yours.", "red")
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
            else:
                new_recipe = Recipe(
                    rulesetid = cruleset.id,
                    name = name,
                    text = text
                )
                db.session.add(new_recipe)
                db.session.commit()
                flash("Recipe created!", "green")
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
    skills = Skill.query.filter_by(rulesetid = cruleset.id).order_by(Skill.name)
    return(
        render_template(
            "skills.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Skills",
            skills = skills
        )
    )

@eprefs.route("/Skills/Create", methods=["GET", "POST"])
@login_required
def createSkill():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        return(skill(request, cruleset, None, "create"))
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

@eprefs.route("/Skills/Duplicate/<string:tskill>")
@login_required
def duplicateSkill(tskill):
    cruleset = getCurrentRuleset(current_user)
    tskill = Skill.query.filter_by(rulesetid=cruleset.id, name=tskill.replace('-', ' ')).first()
    if(not tskill):
        flash("Skill does not exist.", "red")
        return(redirect(url_for("eprefs.skills")))
    return(skill(request, cruleset, tskill, "duplicate"))

@eprefs.route("/Skills/Edit/<string:tskill>", methods=["GET", "POST"])
@login_required
def editSkill(tskill):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    tskill = Skill.query.filter_by(rulesetid=cruleset.id, name=tskill.replace('-', ' ')).first()
    if(not tskill):
        flash("Skill does not exist.", "red")
        return(redirect(url_for("eprefs.skills")))
    elif(request.method == "POST"):
        return(skill(request, cruleset, tskill, "edit"))
    return(
        render_template(
            "create-skill.html",
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Skill",
            skill=tskill
        )
    )


@eprefs.route("/Skills/Delete/<string:tskill>")
@login_required
def deleteSkill(tskill):
    cruleset = getCurrentRuleset(current_user)
    tskill = Skill.query.filter_by(rulesetid=cruleset.id, name=tskill.replace('-', ' ')).first()
    if(not tskill):
        flash("Skill does not exist.", "red")
    else:
        db.session.delete(tskill)
        db.session.commit()
        flash("Skill deleted.", "orange")
    return(redirect(url_for("eprefs.skills")))

@eprefs.route("/Skills/Import", methods=["GET", "POST"])
@login_required
def importSkills():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        return(skillImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-generic.html",
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Import Skills",
        )
    )
