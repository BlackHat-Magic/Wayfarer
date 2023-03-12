from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
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
    if(ability_score and current_user.id != cruleset.userid):
        flash("You cannot edit Ability Scores for rulesets that are not your own.", "red")
    elif(len(name) < 1):
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

def makerace(request, cruleset, race, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create a race in a ruleset that is not yours.")
    elif(instruction == "duplicate"):
        new_race = Race(
            rulesetid = cruleset.id,
            name = f"{race.name} Duplicate",
            flavor = race.flavor,
            asis = race.asis,
            asi_text = race.asi_text,
            size = race.size,
            size_text = race.size_text,
            walk = race.walk,
            fly = race.fly,
            swim = race.swim,
            burrow = race.burrow,
            base_height = race.base_height,
            base_weight = race.base_weight,
            height_num = race.height_num,
            height_die = race.height_die,
            weight_num = race.weight_num,
            weight_die = race.weight_die,
            subrace_flavor = race.subrace_flavor,
        )
        db.session.add(new_race)
        db.session.commit()
        new_race = Race.query.filter_by(rulesetid=cruleset.id, name=f"{race.name} Duplicate").first()
        for feature in race.race_features:
            new_feature = RaceFeature(
                raceid = new_race.id,
                name = feature.name,
                text = feature.text
            )
            db.session.add(new_feature)
        for subrace in race.subraces:
            new_subrace = Subrace(
                raceid = new_race.id,
                name = subrace.name,
                text = subrace.text
            )
            db.session.add(new_subrace)
            db.session.commit()
            new_subrace = Subrace.query.filter_by(rulesetid=cruleset.id, raceid=new_race.id, name=subrace.name, text=new_subrace.text)
            for feature in subrace.subrace_features:
                new_subrace_feature = SubraceFeature(
                    raceid = new_race.id,
                    name = feature.name,
                    text = feature.text
                )
                db.session.add(new_subrace_feature)
        db.session.commit()
        flash("Race duplicated!", "green")
        return(redirect(url_for("epchar.races")))
    else:
        name = request.form.get("name")
        asis = request.form.getlist("asi")
        asi_override = request.form.get("asi_override")
        if(asi_override):
            asis = None
            asi_text = request.form.get("asi_text")
        else:
            # asis = request.form.getlist("asi")
            asi_text = None
        sizelib = [
            "Tiny", 
            "Small", 
            "Medium", 
            "Large", 
            "Huge", 
            "Gargantuan"
        ]
        size_override = request.form.get("size_override")
        if(size_override):
            size = None
            size_text = request.form.get("size_text")
        else:
            size = int(request.form.get("size"))
            size_text = None
        base_height = request.form.get("base_height")
        height_num = request.form.get("height_num")
        height_die = request.form.get("height_die")
        base_weight = request.form.get("base_weight")
        weight_num = request.form.get("weight_num")
        weight_die = request.form.get("weight_die")
        walk = request.form.get("walk")
        swim = request.form.get("swim")
        climb = request.form.get("climb")
        fly = request.form.get("fly")
        burrow = request.form.get("burrow")
        flavor = request.form.get("text")
        features = request.form.getlist("feature_name")
        feature_text = request.form.getlist("feature_text")
        has_subraces = request.form.get("has_subraces")
        if(has_subraces):
            subraces = []
            subrace_flavor = request.form.get("subrace_flavor")
            print(request.form.getlist("subrace_text"))
            for i, subrace in enumerate(request.form.getlist("subrace_name")):
                subraces.append({
                    "name": subrace,
                    "text": request.form.getlist("subrace_text")[i],
                    "features": []
                })
                for j, feature in enumerate(request.form.getlist(f"{subrace}_feature_name")):
                    subraces[i]["features"].append({
                        "name": feature,
                        "text": request.form.getlist(f"{subrace}_feature_text")[j]
                    })
        else:
            subraces = None
            subrace_flavor = None
        if(len(name) < 1):
            flash("You must specify a race name.", "red")
        elif(len(name) > 127):
            flash("Race name must be fewer than 128 characters.", "red")
        elif(len(flavor) > 16383):
            flash("Race description must be fewer than 16384 characters.", "red")
        elif("<" in flavor):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in flavor):
            flash("Cross-site scripting attacks are not allowed.", "red")
        elif("-" in name):
            flash("Dashes (\"-\") are not allowed in race name.", "red")
        else:
            bad = False
            for feature in features:
                if(bad):
                    break
                elif(len(feature) < 1):
                    bad = True
                    flash("Each racial feature must have a name.", "red")
                elif(len(feature) > 127):
                    bad = True
                    flash("Racial feature names must be fewer than 128 characters.", "red")
            for ftext in feature_text:
                if(bad):
                    break
                elif(len(ftext) > 16383):
                    bad = True
                    flash("Racial feature text must be fewer than 16384 characters.", "red")
                elif("<" in ftext):
                    bad = True
                    flash("Open angle brackets (\"<\") are not allowed.", "red")
                elif("javascript" in ftext):
                    bad = True
                    flash("Cross-site scripting attacks are not allowed.", "red")
            if(has_subraces and not bad):
                for subrace in subraces:
                    if(bad):
                        break
                    elif(len(subrace["name"]) < 1):
                        bad = True
                        flash("You must specify a name for each subrace.", "red")
                    elif(len(subrace["name"]) > 127):
                        bad = True
                        flash("Subrace names must be fewer than 128 characters.", "red")
                    elif(len(subrace["text"]) > 16383):
                        bad = True
                        flash("Subrace descriptions must be fewer than 16384 characters.", "red")
                    elif("<" in subrace["text"]):
                        bad = True
                        flash("Open angle brackets (\"<\") are not allowed.", "red")
                    elif("javascript" in subrace["text"]):
                        bad = True
                        flash("Cross-site scripting attacks are not allowed.", "red")
                    for feature in subrace["features"]:
                        if(bad):
                            break
                        elif(len(feature["name"]) < 1):
                            bad = True
                            flash("You must specify a name for each subrace features.", "red")
                        elif(len(feature["name"]) > 127):
                            bad = True
                            flash("Subrace feature names must be fewer than 128 characters.", "red")
                        elif(len(feature["text"]) > 16383):
                            bad = True
                            flash("Subrace feature text must be fewer than 16384 characters.", "red")
                        elif("<" in feature["text"]):
                            bad = True
                            flash("Open angle brackets (\"<\") are not allowed.", "red")
                        elif("javascript" in feature["text"]):
                            bad = True
                            flash("Cross-site scripting attacks are not allowed.", "red")
            if(not bad):
                if(not race):
                    new_race = Race(
                        rulesetid = cruleset.id,
                        name = name,
                        flavor = flavor,
                        asis = asis,
                        asi_text = asi_text,
                        size = size,
                        size_text = size_text,
                        walk = walk,
                        swim = swim,
                        fly = fly,
                        burrow = burrow,
                        base_height = base_height,
                        height_num = height_num,
                        height_die = height_die,
                        base_weight = base_weight,
                        weight_num = weight_num,
                        weight_die = weight_die,
                        subrace_flavor = subrace_flavor
                    )
                    db.session.add(new_race)
                    db.session.commit()
                    new_race = Race.query.filter_by(
                        name = name, 
                        rulesetid = cruleset.id
                    ).first()
                    for i, feature in enumerate(features):
                        new_feature = RaceFeature(
                            raceid = new_race.id,
                            name = feature,
                            text = feature_text[i]
                        )
                        db.session.add(new_feature)
                    db.session.commit()
                    if(has_subraces):
                        for subrace in subraces:
                            new_subrace = Subrace(
                                raceid = new_race.id,
                                name = subrace["name"],
                                text = subrace["text"]
                            )
                            db.session.add(new_subrace)
                            db.session.commit()
                            new_subrace = Subrace.query.filter_by(
                                raceid = new_race.id,
                                name = subrace["name"],
                                text = subrace["text"]
                            ).first()
                            for feature in subrace["features"]:
                                new_feature = SubraceFeature(
                                    raceid = new_subrace.id,
                                    name = feature["name"],
                                    text = feature["text"]
                                )
                                db.session.add(new_feature)
                            db.session.commit()
                    flash("Race created!", "green")
                return(redirect(url_for("epchar.races")))
    return(False)