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
    cruleset = getCurrentRuleset(current_user)
    action = Action.query.filter_by(rulesetid = cruleset.id, name=action).first_or_404()
    return(makeAction(None, cruleset, action, "duplicate"))

@eprefs.route("/Actions/Edit/<string:action>", methods=["GET", "POST"])
@login_required
def editAction(action):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method=="POST"):
        return(actionImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-one.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Import Actions"
        )
    )

@eprefs.route("/Conditions")
def conditions():
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    return(makeCondition(None, cruleset, condition, "duplicate"))

@eprefs.route("/Conditions/Edit/<string:condition>", methods=["GET", "POST"])
@login_required
def editCondition(condition):
    cruleset = getCurrentRuleset(current_user)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        return(conditionImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-one.html", 
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
    disease = Disease.query.filter_by(rulesetid = cruleset.id, name = disease).first_or_404()
    return(makeDisease(None, cruleset, disease, "duplicate"))

@eprefs.route("/Diseases/Edit/<string:disease>")
@login_required
def editDisease(disease):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
    status = Status.query.filter_by(rulesetid = cruleset.id, name = status).first_or_404()
    return(makeStatus(None, cruleset, status, "duplicate"))

@eprefs.route("/Statuses/Edit/<string:status>")
@login_required
def editStatus(status):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
        return(makeItem(request, cruleset, None, "create"))
    return(
        render_template(
            "create-item.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            tags = ruleset.item_tags.order_by(Tag.name),
            properties = ruleset.item_properties.order_by(Property.name)
        )
    )

@eprefs.route("/Items/Duplicate/<string:item>")
@login_required
def duplicateItem(item):
    cruleset = getCurrentRuleset(current_user)
    item = Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first_or_404()
    return(makeItem(None, cruleset, item, "duplicate"))

@eprefs.route("/Items/Edit/<string:item>", methods=["GET", "POST"])
@login_required
def editItem(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "tags.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            tags=cruleset.item_tags.order_by(ItemTag.name), 
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
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    return(itemTag(None, cruleset, tag, "duplicate"))

@eprefs.route("/Items/Tags/Edit/<string:item>", methods=["GET", "POST"]) 
@login_required
def editTag(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    return(
        render_template(
            "properties.html", 
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            properties=cruleset.item_properties.order_by(Property.name), 
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
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    return(itemProperty(None, cruleset, tproperty, "duplicate"))

@eprefs.route("/Items/Properties/Edit/<string:item>", methods=["GET", "POST"])
@login_required
def editProperty(item):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
    tlanguage = Language.query.filter_by(rulesetid=cruleset.id, name=tlanguage).first_or_404()
    return(makeLanguage(None, cruleset, tlanguage, "duplicate"))

@eprefs.route("/Languages/Edit/<string:tlanguage>", methods=["GET", "POST"])
@login_required
def editLanguage(tlanguage):
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
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
    cruleset = getCurrentRuleset(current_user)
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
    cruleset = getCurrentRuleset(current_user)
    frulesets = getForeignRulesets(current_user)
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    if(request.method == "POST"):
        return(languageImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-one.html",
            user=current_user, 
            cruleset=cruleset, 
            frulesets=frulesets, 
            adminrulesets=adminrulesets,
            title="Import Languages",
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
            "import-one.html",
            user=current_user, 
            frulesets=frulesets, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Import Skills",
        )
    )
