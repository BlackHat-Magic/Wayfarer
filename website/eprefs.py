from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, jsonify, flash
from .models import Ruleset, Skill, Action, Condition, Item, ItemTag, Property, Language, Recipe, Spell
from flask_login import login_user, current_user, login_required
from .postformsrefs import *
from .uservalidation import *
from . import db
import json

eprefs = Blueprint('eprefs', __name__)

@eprefs.route("/")
def refs():
    return(redirect(url_for("epmain.home")))

@eprefs.route("/Actions")
def actions():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeAction(request, cruleset, None, "create"))
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

@eprefs.route("/Actions/Duplicate/<string:action>")
@login_required
def duplicateAction(action):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    action = Action.query.filter_by(rulesetid = cruleset.id, name=action).first_or_404()
    return(makeAction(None, cruleset, action, "duplicate"))

@eprefs.route("/Actions/Edit/<string:action>", methods=["GET", "POST"])
@login_required
def editAction(action):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    action = Action.query.filter_by(rulesetid = cruleset.id, name=action).first_or_404()
    if(request.method == "POST"):
        return(makeAction(request, cruleset, action, "edit"))
    return(
        render_template(
            "create-action.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Action",
            action=action
        )
    )

@eprefs.route("/Actions/Delete/<string:action>")
@login_required
def deleteAction(action):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    action = Action.query.filter_by(rulesetid = cruleset.id, name=action).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete actions in rulesets that are not your own.", "red")
    else:
        db.session.delete(action)
        db.session.commit()
        flash("Action deleted", "orange")
    return(redirect(url_for("eprefs.actions")))

@eprefs.route("/Actions/Import", methods=["GET", "POST"])
@login_required
def importActions():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method=="POST"):
        return(actionImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-action.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Import Actions"
        )
    )

@eprefs.route("/Conditions")
def conditions():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "conditions.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            conditions=cruleset.conditions, 
            adminrulesets=adminrulesets,
            title="Conditions",
            button="Condition"
        )
    )

@eprefs.route("/Conditions/Create", methods=["GET", "POST"])
@login_required
def createCondition():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeCondition(request, cruleset, None, "create"))
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

@eprefs.route("/Conditions/Duplicate/<string:condition>")
@login_required
def duplicateCondition(condition):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    return(makeCondition(None, cruleset, condition, "duplicate"))

@eprefs.route("/Conditions/Edit/<string:condition>", methods=["GET", "POST"])
@login_required
def editCondition(condition):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    if(request.method == "POST"):
        return(makeCondition(request, cruleset, condition, "edit"))
    return(
        render_template(
            "create-condition.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {condition.name}",
            condition = condition
        )
    )
    
@eprefs.route("/Conditions/Delete/<string:condition>")
@login_required
def deleteCondition(condition):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete conditions in rulesets that are not your own", "red")
    else:
        db.session.delete(condition)
        db.session.commit()
    return(redirect(url_for("eprefs.conditions")))

@eprefs.route("/Conditions/Import", methods=["GET", "POST"])
@login_required
def importConditions():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(conditionImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-condition.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            conditions=conditions, 
            adminrulesets=adminrulesets,
            title="Import Conditions, Diseases, and Statuses"
        )
    )

@eprefs.route("/Diseases")
def diseases():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "conditions.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            conditions = cruleset.diseases,
            adminrulesets=adminrulesets,
            title="Diseases",
            button="Disease"
        )
    )

@eprefs.route("/Diseases/Create")
@login_required
def createDisease():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeDisease(request, cruleset, None, "create"))
    return(
        render_template(
            "create-condition.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Disease"
        )
    )

@eprefs.route("/Diseases/Duplicate/<string:disease>")
@login_required
def duplicateDisease(disease):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    disease = Disease.query.filter_by(rulesetid = cruleset.id, name = disease).first_or_404()
    return(makeDisease(None, cruleset, disease, "duplicate"))

@eprefs.route("/Diseases/Edit/<string:disease>")
@login_required
def editDisease(disease):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    disease = Disease.query.filter_by(rulesetid = cruleset.id, name = disease).first_or_404()
    if(request.method == "POST"):
        return(makeDisease(request, cruleset, disease, "edit"))
    return(
        render_template(
            "create-condition.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {disease.name}",
            condition = disease
        )
    )

@eprefs.route("/Diseases/Delete/<string:disease>")
@login_required
def deleteDisease(disease):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    disease = Disease.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete diseases in rulesets that are not your own.", "red")
    else:
        db.session.delete(disease)
        db.session.commit()
        flash("Disease deleted.", "orange")
    return(redirect(url_for("eprefs.diseases")))

@eprefs.route("/Statuses")
def statuses():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "conditions.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            conditions=cruleset.statuses, 
            adminrulesets=adminrulesets,
            title="Statuses",
            button="Status"
        )
    )

@eprefs.route("/Statuses/Create")
@login_required
def createStatus():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeStatus(request, cruleset, None, "create"))
    return(
        render_template(
            "create-condition.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Status"
        )
    )

@eprefs.route("/Statuses/Duplicate/<string:status>")
@login_required
def duplicateStatus(status):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    status = Status.query.filter_by(rulesetid = cruleset.id, name = status).first_or_404()
    return(makeStatus(None, cruleset, status, "duplicate"))

@eprefs.route("/Statuses/Edit/<string:status>")
@login_required
def editStatus(status):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    status = Status.query.filter_by(rulesetid = cruleset.id, name = status).first_or_404()
    if(request.method == "POST"):
        return(makeStatus(request, cruleset, status, "edit"))
    return(
        render_template(
            "create-condition.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {status.name}",
            condition = status
        )
    )

@eprefs.route("/Statuses/Delete/<string:status>")
@login_required
def deleteStatus(status):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    status = Status.query.filter_by(rulesetid = cruleset.id, name = status).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete statuses in rulesets that are not your own.", "red")
    else:
        db.session.delete(status)
        db.session.commit()
        flash("Status deleted.", "orange")
    return(redirect(url_for("eprefs.statuses")))

@eprefs.route("/Items")
def items():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeItem(request, cruleset, None, "create"))
    return(
        render_template(
            "create-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            tags = ItemTag.query.filter_by(rulesetid=cruleset.id).order_by(ItemTag.name),
            properties = Property.query.filter_by(rulesetid=cruleset.id).order_by(Property.name)
        )
    )

@eprefs.route("/Items/Duplicate/<string:item>")
@login_required
def duplicateItem(item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    item = Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first_or_404()
    return(makeItem(None, cruleset, item, "duplicate"))

@eprefs.route("/Items/Edit/<string:item>", methods=["GET", "POST"])
@login_required
def editItem(item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    item = Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first_or_404()
    if(request.method == "POST"):
        makeItem(request, cruleset, item, "edit")
    return(
        render_template(
            "create-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            item=cruleset.item_tags.order_by(ItemTag.name),
            tags = cruleset.item_properties.order_by(Property.name),
            properties = properties
        )
    )

@eprefs.route("/Items/Delete/<string:item>")
@login_required
def deleteItem(item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    item = Item.query.filter_by(rulesetid = cruleset.id, name=item).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete items from rulesets that are not yours.", "red")
    else:
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted.", "orange")
    return(redirect(url_for("eprefs.items")))

@eprefs.route("/Items/Import", methods=["GET", "POST"])
@login_required
def importItems():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method=="POST"):
        items = json.loads(request.form.get("feature_file"))
        base = json.loads(request.form.get("flavor_file"))
        return(itemImporter(items, base, cruleset))
    return(
        render_template(
            "import-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Items"
        )
    )

@eprefs.route("/Item/<string:item>")
def item(item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    item = Item.query.filter_by(rulesetid = cruleset.id, name=item).first_or_404()
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "tags.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            tags=ItemTag.query.filter_by(rulesetid=cruleset.id).order_by(ItemTag.name), 
            adminrulesets=adminrulesets,
            title="Item Types"
        )
    )

@eprefs.route("/Items/Tags/Create", methods=["GET", "POST"]) 
@login_required
def createTag():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    return(itemTag(None, cruleset, tag, "duplicate"))

@eprefs.route("/Items/Tags/Edit/<string:item>", methods=["GET", "POST"]) 
@login_required
def editTag(item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(request.method == "POST"):
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete item tags in rulesets that are not your own.", "red")
    else:
        db.session.delete(tag)
        db.session.commit()
        flash("Item tag deleted.", "orange")
    return(redirect(url_for("eprefs.tags")))

@eprefs.route("/Items/Properties")
def properties():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "properties.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            properties=Property.query.filter_by(rulesetid=cruleset.id).order_by(Property.name), 
            adminrulesets=adminrulesets,
            title="Weapon Properties"
        )
    )

@eprefs.route("/Items/Properties/Create", methods=["GET", "POST"])
@login_required
def createProperty():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    return(itemProperty(None, cruleset, tproperty, "duplicate"))

@eprefs.route("/Items/Properties/Edit/<string:item>", methods=["GET", "POST"])
@login_required
def editProperty(item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(request.method == "POST"):
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete item properties in rulesets that are not your own.", "red")
    else:
        db.session.delete(tproperty)
        db.session.commit()
        flash("Item property deleted.", "orange")
    return(redirect(url_for("eprefs.properties")))

@eprefs.route("/Languages")
def languages():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tlanguage = Language.query.filter_by(rulesetid=cruleset.id, name=tlanguage).first_or_404()
    return(makeLanguage(None, cruleset, tlanguage, "duplicate"))

@eprefs.route("/Languages/Edit/<string:tlanguage>", methods=["GET", "POST"])
@login_required
def editLanguage(tlanguage):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tlanguage = Language.query.filter_by(rulesetid=cruleset.id, name=tlanguage).first_or_404()
    if(request.method == "POST"):
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tlanguage = Language.query.filter_by(rulesetid=cruleset.id, name=tlanguage).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete languages in rulesets that are not your own.", "red")
    else:
        db.session.delete(tlanguage)
        db.session.commit()
        flash("Language deleted.", "orange")
    return(redirect(url_for("eprefs.languages")))

@eprefs.route("/Languages/Import", methods=["GET", "POST"])
@login_required
def importLanguages():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(languageImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-language.html",
            user=current_user, 
            cruleset=cruleset, 
            frulesets=frulesets, 
            adminrulesets=adminrulesets,
            title="Import Languages",
        )
    )

@eprefs.route("/Spells")
def spells():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeSpell(request, cruleset, None, "create"))
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

@eprefs.route("/Spells/Duplicte/<string:spell>")
@login_required
def duplicateSpell(spell):
    cruleset = getCurrentRuleset(current_user)
    spell = cruleset.spells.filter_by(name = spell).first_or_404()
    return(makeSpell(None, cruleset, spell, "duplicate"))

@eprefs.route("/Spells/Edit/<string:spell>")
@login_required
def editSpell(spell):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    spell = cruleset.spells.filter_by(name = spell).first_or_404()
    if(request.method == "POST"):
        return(makeSpell(request, cruleset, spell, "edit"))
    return(
        render_template(
            "create-spell.html", 
            user=current_user, 
            cruleset=cruleset, 
            frulesets=frulesets, 
            adminrulesets=adminrulesets,
            title=f"Edit {spell.name}",
            spell = spell
        )
    )

@eprefs.route("/Spells/Delete/<string:spell>")
@login_required
def deleteSpell(spell):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    spell = cruleset.spells.filter_by(name = spell).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete spells in rulesets that are not your own.", "red")
    else:
        db.session.delete(spell)
        db.session.commit()
        flash("Spell deleted.", "orange")
    return(redirect(url_for("eprefs.spells")))

@eprefs.route("/Spells/Import", methods=["GET", "POST"])
@login_required
def importSpells():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(spellImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-spell.html", 
            user=current_user, 
            cruleset=cruleset, 
            frulesets=frulesets, 
            adminrulesets=adminrulesets,
            title="Import Spells"
        )
    )

@eprefs.route("/Spell/<string:spell>")
def spell(spell):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeRecipe(request, cruleset, None, "create"))
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

@eprefs.route("/Recipes/Duplicate/<string:recipe>")
@login_required
def duplicateRecipe(recipe):
    cruleset = getCurrentRuleset(current_user)
    recipe = cruleset.recipes.filter_by(name = recipe).first_or_404()
    return(makeRecipe(request, cruleset, recipe, "duplicate"))

@eprefs.route("/Recipes/Edit/<string:recipe>", methods=["GET", "POST"])
@login_required
def editRecipe(recipe):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    recipe = cruleset.recipes.filter_by(name = recipe).first_or_404()
    if(request.method == "POST"):
        return(makeRecipe(request, cruleset, recipe, "edit"))
    return(
        render_template(
            "create-recipe.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {recipe.name}",
            recipe = recipe
        )
    )

@eprefs.route("/Skills")
def skills():
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tskill = Skill.query.filter_by(rulesetid=cruleset.id, name=tskill.replace('-', ' ')).first()
    if(not tskill):
        flash("Skill does not exist.", "red")
        return(redirect(url_for("eprefs.skills")))
    return(skill(request, cruleset, tskill, "duplicate"))

@eprefs.route("/Skills/Edit/<string:tskill>", methods=["GET", "POST"])
@login_required
def editSkill(tskill):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
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
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(skillImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-one.html",
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Import Skills",
        )
    )
