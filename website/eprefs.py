from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, jsonify, flash, send_file
from .models import *
from flask_login import login_user, current_user, login_required
from .postformsrefs import *
from .uservalidation import *
from . import db
import json, io

eprefs = Blueprint('eprefs', __name__)

@eprefs.route("/")
def noRulesetRefs():
    return(noRuleset(current_user, "epmain.home"))
@eprefs.route("/", subdomain="<ruleset>")
def refs(ruleset):
    return(redirect(url_for("epmain.home", ruleset=ruleset)))

@eprefs.route("/Actions")
def noRulesetActions():
    return(noRuleset(current_user, "eprefs.actions"))
@eprefs.route("/Actions", subdomain="<ruleset>")
def actions(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "actions.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Actions"
        )
    )

@eprefs.route("/Actions/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createAction(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeAction(request, cruleset, None, "create"))
    return(
        render_template(
            "create-action.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Action"
        )
    )

@eprefs.route("/Actions/Duplicate/<string:action>", subdomain="<ruleset>")
@login_required
def duplicateAction(action, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    action = Action.query.filter_by(rulesetid = cruleset.id, name=action).first_or_404()
    return(makeAction(None, cruleset, action, "duplicate"))

@eprefs.route("/Actions/Edit/<string:action>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editAction(action, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    action = Action.query.filter_by(rulesetid = cruleset.id, name=action).first_or_404()
    if(request.method == "POST"):
        return(makeAction(request, cruleset, action, "edit"))
    return(
        render_template(
            "create-action.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Action",
            action=action
        )
    )

@eprefs.route("/Actions/Delete/<string:action>", subdomain="<ruleset>")
@login_required
def deleteAction(action, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    action = Action.query.filter_by(rulesetid = cruleset.id, name=action).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete actions in rulesets that are not your own.", "red")
    else:
        db.session.delete(action)
        db.session.commit()
        flash("Action deleted", "orange")
    return(redirect(url_for("eprefs.actions", ruleset=ruleset)))

@eprefs.route("/Actions/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importActions(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method=="POST"):
        return(actionImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-action.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Import Actions"
        )
    )

@eprefs.route("/Actions/Export", subdomain="<ruleset>")
def exportActions(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    actions = [action.to_dict() for action in cruleset.actions]
    json_data = json.dumps(actions)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="actions.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Conditions")
def noRulesetConditions():
    return(noRuleset(current_user, "eprefs.conditions"))
@eprefs.route("/Conditions", subdomain="<ruleset>")
def conditions(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "conditions.html", 
            cruleset=cruleset, 
            conditions=cruleset.conditions, 
            adminrulesets=adminrulesets,
            title="Conditions",
            button="Condition",
            importer="eprefs.importConditions",
            exporter="eprefs.exportConditions"
        )
    )

@eprefs.route("/Conditions/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createCondition(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeCondition(request, cruleset, None, "create"))
    return(
        render_template(
            "create-condition.html",
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Condition"
        )
    )

@eprefs.route("/Conditions/Duplicate/<string:condition>", subdomain="<ruleset>")
@login_required
def duplicateCondition(condition, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    return(makeCondition(None, cruleset, condition, "duplicate"))

@eprefs.route("/Conditions/Edit/<string:condition>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editCondition(condition, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    if(request.method == "POST"):
        return(makeCondition(request, cruleset, condition, "edit"))
    return(
        render_template(
            "create-condition.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {condition.name}",
            condition = condition
        )
    )

@eprefs.route("/Conditions/Delete/<string:condition>", subdomain="<ruleset>")
@login_required
def deleteCondition(condition, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    condition = Condition.query.filter_by(rulesetid = cruleset.id, name = condition).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete conditions in rulesets that are not your own", "red")
    else:
        db.session.delete(condition)
        db.session.commit()
    return(redirect(url_for("eprefs.conditions", ruleset=ruleset)))

@eprefs.route("/Conditions/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importConditions(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(conditionImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-condition.html", 
            cruleset=cruleset, 
            conditions=conditions, 
            adminrulesets=adminrulesets,
            title="Import Conditions"
        )
    )

@eprefs.route("/Conditions/Export", subdomain="<ruleset>")
def exportConditions(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    conditions = [condition.to_dict() for condition in cruleset.conditions]
    json_data = json.dumps(conditions)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="conditions.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Diseases")
def noRulesetDiseases():
    return(noRuleset(current_user, "eprefs.diseases"))
@eprefs.route("/Diseases", subdomain="<ruleset>")
def diseases(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "conditions.html", 
            cruleset=cruleset, 
            conditions = cruleset.diseases,
            adminrulesets=adminrulesets,
            title="Diseases",
            button="Disease",
            importer="eprefs.importDiseases",
            exporter="eprefs.exportDiseases"
        )
    )

@eprefs.route("/Diseases/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importDiseases(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(diseaseImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-disease.html", 
            cruleset=cruleset, 
            conditions=conditions, 
            adminrulesets=adminrulesets,
            title="Import Diseases"
        )
    )

@eprefs.route("/Diseases/Export", subdomain="<ruleset>")
def exportDiseases(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    diseases = [disease.to_dict() for disease in cruleset.diseases]
    json_data = json.dumps(diseases)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="diseases.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Diseases/Create", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def createDisease(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeDisease(request, cruleset, None, "create"))
    return(
        render_template(
            "create-condition.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Disease"
        )
    )

@eprefs.route("/Diseases/Duplicate/<string:disease>", subdomain="<ruleset>")
@login_required
def duplicateDisease(disease, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    disease = Disease.query.filter_by(rulesetid = cruleset.id, name = disease).first_or_404()
    return(makeDisease(None, cruleset, disease, "duplicate"))

@eprefs.route("/Diseases/Edit/<string:disease>", subdomain="<ruleset>")
@login_required
def editDisease(disease, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    disease = Disease.query.filter_by(rulesetid = cruleset.id, name = disease).first_or_404()
    if(request.method == "POST"):
        return(makeDisease(request, cruleset, disease, "edit"))
    return(
        render_template(
            "create-condition.html", 
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
    return(redirect(url_for("eprefs.diseases", ruleset=ruleset)))

@eprefs.route("/Statuses")
def noRulesetStatuses():
    return(noRuleset(current_user, "eprefs.statuses"))
@eprefs.route("/Statuses", subdomain="<ruleset>")
def statuses(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "conditions.html", 
            cruleset=cruleset, 
            conditions=cruleset.statuses, 
            adminrulesets=adminrulesets,
            title="Statuses",
            button="Status",
            importer="eprefs.importStatuses",
            exporter="eprefs.exportStatuses"
        )
    )

@eprefs.route("/Statuses/Create", subdomain="<ruleset>")
@login_required
def createStatus(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeStatus(request, cruleset, None, "create"))
    return(
        render_template(
            "create-condition.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Status"
        )
    )

@eprefs.route("/Statuses/Duplicate/<string:status>", subdomain="<ruleset>")
@login_required
def duplicateStatus(status, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    status = Status.query.filter_by(rulesetid = cruleset.id, name = status).first_or_404()
    return(makeStatus(None, cruleset, status, "duplicate"))

@eprefs.route("/Statuses/Edit/<string:status>", subdomain="<ruleset>")
@login_required
def editStatus(status, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    status = Status.query.filter_by(rulesetid = cruleset.id, name = status).first_or_404()
    if(request.method == "POST"):
        return(makeStatus(request, cruleset, status, "edit"))
    return(
        render_template(
            "create-condition.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {status.name}",
            condition = status
        )
    )

@eprefs.route("/Statuses/Delete/<string:status>", subdomain="<ruleset>")
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
    return(redirect(url_for("eprefs.statuses", ruleset=ruleset)))

@eprefs.route("/Statuses/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importStatuses(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(statusImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-status.html", 
            cruleset=cruleset, 
            conditions=conditions, 
            adminrulesets=adminrulesets,
            title="Import Status"
        )
    )

@eprefs.route("/Statuses/Export", subdomain="<ruleset>")
def exportStatuses(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    statuses = [status.to_dict() for status in cruleset.statuses]
    json_data = json.dumps(statuses)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="statuses.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Items")
def noRulesetItems():
    return(noRuleset(current_user, "eprefs.items"))
@eprefs.route("/Items", subdomain="<ruleset>")
def items(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    items = Item.query.filter_by(rulesetid = cruleset.id).order_by(Item.name)
    return(
        render_template(
            "items.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Items",
            items = items
        )
    )

@eprefs.route("/Items/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createItem(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeItem(request, cruleset, None, "create"))
    return(
        render_template(
            "create-item.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            tags = ItemTag.query.filter_by(rulesetid=cruleset.id).order_by(ItemTag.name),
            properties = Property.query.filter_by(rulesetid=cruleset.id).order_by(Property.name)
        )
    )

@eprefs.route("/Items/Duplicate/<string:item>", subdomain="<ruleset>")
@login_required
def duplicateItem(item, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    item = Item.query.filter_by(rulesetid = cruleset.id, name = item.replace('-', ' ')).first_or_404()
    return(makeItem(None, cruleset, item, "duplicate"))

@eprefs.route("/Items/Edit/<string:item>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editItem(item, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    item = Item.query.filter_by(rulesetid = cruleset.id, name = item).first_or_404()
    if(request.method == "POST"):
        return(makeItem(request, cruleset, item, "edit"))
    return(
        render_template(
            "create-item.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create an Item",
            item=item,
        )
    )

@eprefs.route("/Items/Delete/<string:item>", subdomain="<ruleset>")
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
    return(redirect(url_for("eprefs.items", ruleset=ruleset)))

@eprefs.route("/Items/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importItems(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method=="POST"):
        items = json.loads(request.form.get("parsed"))
        return(itemImporter(items, cruleset))
    return(
        render_template(
            "import-item.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Items"
        )
    )

@eprefs.route("/Items/Export", subdomain="<ruleset>")
def exportItems(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    items = [item.to_dict() for item in cruleset.items]
    json_data = json.dumps(items)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="items.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Item/<string:item>")
def noRulesetItem(item):
    return(noRuleset(current_user, "eprefs.item", item=item))
@eprefs.route("/Item/<string:item>", subdomain="<ruleset>")
def item(item, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    item = Item.query.filter_by(rulesetid = cruleset.id, name=item).first_or_404()
    return(
        render_template(
            "item.html", 
            cruleset=cruleset, 
            item=item, 
            adminrulesets=adminrulesets,
            title=item.name
        )
    )

@eprefs.route("/Items/Tags")
def noRulesetItemTags():
    return(noRuleset(current_user, "eprefs.tags"))
@eprefs.route("/Items/Tags", subdomain="<ruleset>")
def tags(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "tags.html", 
            cruleset=cruleset, 
            tags=ItemTag.query.filter_by(rulesetid=cruleset.id).order_by(ItemTag.name), 
            adminrulesets=adminrulesets,
            title="Item Types"
        )
    )

@eprefs.route("/Items/Tags/Create", methods=["GET", "POST"], subdomain="<ruleset>") 
@login_required
def createTag(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(itemTag(request, cruleset, None, "create"))
    return(
        render_template(
            "create-tag.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create Item Type"
        )
    )

@eprefs.route("/Items/Tags/Duplicate/<string:item>", subdomain="<ruleset>")
@login_required
def duplicateTag(item, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    return(itemTag(None, cruleset, tag, "duplicate"))

@eprefs.route("/Items/Tags/Edit/<string:item>", methods=["GET", "POST"], subdomain="<ruleset>") 
@login_required
def editTag(item, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(request.method == "POST"):
        return(itemTag(request, cruleset, tag, "edit"))
    return(
        render_template(
            "create-tag.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {tag.name}",
            tag=tag
        )
    )

@eprefs.route("/Items/Tags/Delete/<string:item>", subdomain="<ruleset>")
@login_required
def deleteTag(ruleset, item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tag = ItemTag.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete item tags in rulesets that are not your own.", "red")
    else:
        db.session.delete(tag)
        db.session.commit()
        flash("Item tag deleted.", "orange")
    return(redirect(url_for("eprefs.tags", ruleset=ruleset)))

@eprefs.route("/Items/Tags/Import", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def importTags(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method=="POST"):
        tags = json.loads(request.form.get("parsed"))
        return(tagImporter(tags, cruleset))
    return(
        render_template(
            "import-tag.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Item Tags"
        )
    )

@eprefs.route("/Items/Tags/Export", subdomain="<ruleset>")
def exportTags(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tags = [tag.to_dict() for tag in cruleset.item_tags]
    json_data = json.dumps(tags)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="item-tags.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Items/Properties")
def noRulesetWeaponProperties():
    return(noRuleset(current_user, "eprefs.properties"))
@eprefs.route("/Items/Properties", subdomain="<ruleset>")
def properties(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "properties.html", 
            cruleset=cruleset, 
            properties=Property.query.filter_by(rulesetid=cruleset.id).order_by(Property.name), 
            adminrulesets=adminrulesets,
            title="Weapon Properties"
        )
    )

@eprefs.route("/Items/Properties/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createProperty(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(itemProperty(request, cruleset, None, "create"))
    return(
        render_template(
            "create-property.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create Weapon Property"
        )
    )

@eprefs.route("/Items/Properties/Duplicate/<string:item>", subdomain="<ruleset>")
@login_required
def duplicateProperty(item, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    return(itemProperty(None, cruleset, tproperty, "duplicate"))

@eprefs.route("/Items/Properties/Edit/<string:item>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editProperty(item, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(request.method == "POST"):
        return(itemProperty(request, cruleset, tproperty, "edit"))
    return(
        render_template(
            "create-property.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {tproperty.name}",
            tproperty=tproperty
        )
    )

@eprefs.route("/Items/Properties/Delete/<string:item>", subdomain="<ruleset>")
@login_required
def deleteProperty(ruleset, item):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    tproperty = Property.query.filter_by(rulesetid=cruleset.id, name=item).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete item properties in rulesets that are not your own.", "red")
    else:
        db.session.delete(tproperty)
        db.session.commit()
        flash("Item property deleted.", "orange")
    return(redirect(url_for("eprefs.properties", ruleset=ruleset)))

@eprefs.route("/Items/Properties/Import", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def importProperties(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method=="POST"):
        properties = json.loads(request.form.get("parsed"))
        return(propertyImporter(properties, cruleset))
    return(
        render_template(
            "import-property.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Weapon Properties"
        )
    )

@eprefs.route("/Items/Properties/Export", subdomain="<ruleset>")
def exportProperties(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    items = [item.to_dict() for item in cruleset.item_properties]
    json_data = json.dumps(items)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="properties.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

# @eprefs.route("Items/Bulk-Tools", subdomain="<ruleset>", methods=["GET", "POST"])
# @login_required
# def bulkItems(ruleset):
#     adminrulesets, cruleset = validateRuleset(current_user, ruleset)
#     if(request.method == "POST"):
#         if(request.form.get("action") == "delete"):
#             for i, item in enumerate(cruleset.items):
#                 if(request.form.get(f"{item.name}-select")):
#                     db.session.delete(item)
#             flash("Items deleted.", "orange")
#         elif(request.form.get("action") == "addtag"):
#             for i, item in enumerate(cruleset.items):
#                 if(request.form.get(f"{item.name}-select")):
#                     # idk why, but SQLAlchemy refuses to acknowledge the commit # unless I convert it to a set first (a tuple would probably # also work but I didn't test it). I've tried refreshing
#                     # making it transient and readding it, deleting and
#                     # reinitializing, expiring the session; only this works
#                     tags = set(item.tags)
#                     for tag in request.form.getlist("addremtag"):
#                         tags.add(tag)
#                     item.tags = list(tags)
#             flash("Tags added.", "green")
#         elif(request.form.get("action") == "remtag"):
#             for i, item in enumerate(cruleset.items):
#                 if(request.form.get(f"{item.name}-select")):
#                     for tag in request.form.getlist("addremtag"):
#                         if(tag in item.tags):
#                             item.tags.remove(tag)
#             flash("Tags removed.", "green")
#         db.session.commit()
#         return(redirect(url_for("eprefs.items", ruleset=cruleset.identifier)))
#     return(
#         render_template(
#             "items-bulk.html", 
#             cruleset=cruleset,
#             adminrulesets=adminrulesets,
#             title="Bulk Item Tools"
#         )
#     )

@eprefs.route("/Languages")
def noRulesetLanguages():
    return(noRuleset(current_user, "eprefs.languages"))
@eprefs.route("/Languages", subdomain="<ruleset>")
def languages(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "languages.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Languages"
        )
    )

@eprefs.route("/Languages/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createLanguage(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeLanguage(request, cruleset, None, "create"))
    return(
        render_template(
            "create-language.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Language"
        )
    )

@eprefs.route("/Languages/Duplicate/<string:language>", subdomain="<ruleset>")
@login_required
def duplicateLanguage(language, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    language = Language.query.filter_by(rulesetid=cruleset.id, name=language).first_or_404()
    return(makeLanguage(None, cruleset, language, "duplicate"))

@eprefs.route("/Languages/Edit/<string:language>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editLanguage(language, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    language = Language.query.filter_by(rulesetid=cruleset.id, name=language).first_or_404()
    if(request.method == "POST"):
        return(makeLanguage(request, cruleset, language, "edit"))
    return(
        render_template(
            "create-language.html",
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {language.name}",
            language=language
        )
    )

@eprefs.route("/Languages/Delete/<string:language>", subdomain="<ruleset>")
@login_required
def deleteLanguage(language):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    language = Language.query.filter_by(rulesetid=cruleset.id, name=language).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete languages in rulesets that are not your own.", "red")
    else:
        db.session.delete(language)
        db.session.commit()
        flash("Language deleted.", "orange")
    return(redirect(url_for("eprefs.languages", ruleset=ruleset)))

@eprefs.route("/Languages/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importLanguages(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(languageImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-language.html",
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Import Languages",
        )
    )

@eprefs.route("/Languages/Export", subdomain="<ruleset>")
def exportLanguages(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    languages = [language.to_dict() for language in cruleset.languages]
    json_data = json.dumps(languages)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="languages.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Spells")
def noRulesetSpells():
    return(noRuleset(current_user, "eprefs.spells"))
@eprefs.route("/Spells", subdomain="<ruleset>")
def spells(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "spells.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Spells"
        )
    )

@eprefs.route("/Spells/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createSpell(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeSpell(request, cruleset, None, "create"))
    return(
        render_template(
            "create-spell.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Spell"
        )
    )

@eprefs.route("/Spells/Duplicate/<string:spell>", subdomain="<ruleset>")
@login_required
def duplicateSpell(spell, ruleset):
    cruleset = getCurrentRuleset(current_user)
    spell = cruleset.spells.filter_by(name = spell).first_or_404()
    return(makeSpell(None, cruleset, spell, "duplicate"))

@eprefs.route("/Spells/Edit/<string:spell>", subdomain="<ruleset>")
@login_required
def editSpell(spell, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    spell = cruleset.spells.filter_by(name = spell).first_or_404()
    if(request.method == "POST"):
        return(makeSpell(request, cruleset, spell, "edit"))
    return(
        render_template(
            "create-spell.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {spell.name}",
            spell = spell
        )
    )

@eprefs.route("/Spells/Delete/<string:spell>", subdomain="<ruleset>")
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
    return(redirect(url_for("eprefs.spells", ruleset=ruleset)))

@eprefs.route("/Spells/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importSpells(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(spellImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-spell.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Import Spells"
        )
    )

@eprefs.route("/Spells/Export", subdomain="<ruleset>")
def exportSpells(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    spells = [spell.to_dict() for spell in cruleset.spells]
    json_data = json.dumps(spells)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="spells.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Spell/<string:spell>")
def noRulesetSpell(spell):
    return(noRuleset(current_user, "eprefs.spell"))
@eprefs.route("/Spell/<string:spell>", subdomain="<ruleset>")
def spell(spell, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    spell = Spell.query.filter_by(rulesetid = cruleset.id, name = spell).first()
    return(
        render_template(
            "spell.html", 
            cruleset=cruleset, 
            spell=spell, 
            adminrulesets=adminrulesets,
            title=spell.name
        )
    )

@eprefs.route("/Recipes")
def noRulesetRecipes():
    return(noRuleset(current_user, "eprefs.recipes"))
@eprefs.route("/Recipes", subdomain="<ruleset>")
def recipes(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "recipes.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Recipes"
        )
    )

@eprefs.route("/Recipes/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createRecipe(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeRecipe(request, cruleset, None, "create"))
    return(
        render_template(
            "create-recipe.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Recipe"
        )
    )

@eprefs.route("/Recipes/Duplicate/<string:recipe>", subdomain="<ruleset>")
@login_required
def duplicateRecipe(recipe, ruleset):
    cruleset = getCurrentRuleset(current_user)
    recipe = Recipe.query.filter_by(rulesetid=cruleset.id, name=recipe).first_or_404()
    return(makeRecipe(request, cruleset, recipe, "duplicate"))

@eprefs.route("/Recipes/Edit/<string:recipe>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editRecipe(recipe, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    recipe = Recipe.query.filter_by(rulesetid=cruleset.id, name=recipe).first_or_404()
    if(request.method == "POST"):
        return(makeRecipe(request, cruleset, recipe, "edit"))
    return(
        render_template(
            "create-recipe.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title=f"Edit {recipe.name}",
            recipe = recipe
        )
    )

@eprefs.route("/Recipes/Delete/<string:recipe>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def deleteRecipe(recipe, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    recipe = Recipe.query.filter_by(rulesetid=cruleset.id, name=recipe).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete recipes in rulesets that are not your own.", "red")
    else:
        db.session.delete(recipe)
        db.session.commit()
        flash("Recipe deleted.", "orange")
    return(redirect(url_for("eprefs.recipes", ruleset=ruleset)))

@eprefs.route("/Recipes/Import", subdomain="<ruleset>", methods=["GET", "POST"])
@login_required
def importRecipes(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        recipes = json.loads(request.form.get('parsed'))
        return(recipeImporter(cruleset, recipes))
    return(
        render_template(
            "import-recipe.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Import Recipes",
        )
    )

@eprefs.route("/Recipes/Export", subdomain="<ruleset>")
def exportRecipes(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    recipes = [recipe.to_dict() for recipe in cruleset.recipes]
    json_data = json.dumps(recipes)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="recipes.json",
            mimetype="application/json",
            as_attachment=True
        )
    )

@eprefs.route("/Skills")
def noRulesetSkills():
    return(noRuleset(current_user, "eprefs.skills"))
@eprefs.route("/Skills", subdomain="<ruleset>")
def skills(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    skills = Skill.query.filter_by(rulesetid = cruleset.id).order_by(Skill.name)
    return(
        render_template(
            "skills.html", 
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Skills",
            skills = skills
        )
    )

@eprefs.route("/Skills/Create", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def createSkill(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(makeSkill(request, cruleset, None, "create"))
    return(
        render_template(
            "create-skill.html",
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Skill"
        )
    )

@eprefs.route("/Skills/Duplicate/<string:skill>", subdomain="<ruleset>")
@login_required
def duplicateSkill(skill, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    skill = Skill.query.filter_by(rulesetid=cruleset.id, name=skill).first_or_404()
    return(makeSkill(request, cruleset, tskill, "duplicate"))

@eprefs.route("/Skills/Edit/<string:skill>", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def editSkill(skill, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    skill = Skill.query.filter_by(rulesetid=cruleset.id, name=skill).first_or_404()
    if(request.method == "POST"):
        return(makeSkill(request, cruleset, skill, "edit"))
    return(
        render_template(
            "create-skill.html",
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Create a Skill",
            skill=skill
        )
    )


@eprefs.route("/Skills/Delete/<string:skill>", subdomain="<ruleset>")
@login_required
def deleteSkill(skill, ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    skill = Skill.query.filter_by(rulesetid=cruleset.id, name=skill).first_or_404()
    if(current_user.id != cruleset.userid):
        flash("You cannot delete skills in rulesets that are not your own.", "red")
        return(redirect(url_for("eprefs.skills", ruleset=ruleset)))
    if(request.method == "POST"):
        db.session.delete(tskill)
        db.session.commit()
        flash("Skill deleted.", "orange")
    return(
        render_template(
            "delete-skill.html",
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title=f"Delete {tskill}?"
        )
    )

@eprefs.route("/Skills/Import", methods=["GET", "POST"], subdomain="<ruleset>")
@login_required
def importSkills(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    if(request.method == "POST"):
        return(skillImporter(json.loads(request.form.get("parsed")), cruleset))
    return(
        render_template(
            "import-one.html",
            cruleset=cruleset, 
            adminrulesets=adminrulesets,
            title="Import Skills",
        )
    )

@eprefs.route("/Skills/Export", subdomain="<ruleset>")
def exportSkills(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    skills = [skill.to_dict() for skill in cruleset.skills]
    json_data = json.dumps(skills)

    mem = io.BytesIO()
    mem.write(json_data.encode('utf-8'))
    mem.seek(0)

    return(
        send_file(
            mem, 
            download_name="skills.json",
            mimetype="application/json",
            as_attachment=True
        )
    )