from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .models import *
import pickle, sys

def abilityScore(request, cruleset, ability_score, instruction):
    name = request.form.get("name")
    abbr = request.form.get("abbr").casefold()
    order = request.form.get("order")
    text = request.form.get("text")
    invalid = False
    if(ability_score and current_user.id != cruleset.userid):
        flash("You cannot edit Ability Scores for rulesets that are not your own.", "red")
    elif(instruction == "duplicate"):
        new_ability_score = AbilityScore(
            rulesetid=cruleset.id,
            name=ability_score.name,
            abbr=ability_score.abbr,
            order=ability_score.order,
            text=ability_score.text
        )
        db.session.add(new_ability_score)
        db.session.commit()
        flash("Ability Score Duplicated!")
        return(f"<button x-init=\"window.location.href='{url_for('epchar.stats', ruleset=cruleset.identifier)}'\">Duplicate {stat.name}</button>")
    if(order):
        try:
            order = int(order)
        except:
            flash("Ability Score Order must be a number.")
            invalid = True
    if(len(name) < 1):
        flash("You must specify an Ability Score name.", "red")
        invalid = True
    elif(len(name) > 127):
        flash("Ability Score name must be fewer than 128 characters.", "red")
        invalid = True
    elif(len(abbr) != 3):
        flash("Ability Score abbreviation must be 3 characters.", "red")
        invalid = True
    elif(len(text) > 16383):
        flash("Ability Score description must be fewer than 16384 characters.", "red")
        invalid = True
    elif("<" in text):
        flash("Open angle brackets (\"<\") are not allowed.", "red")
        invalid = True
    elif("javascript" in text):
        flash("Cross-site scripting attacks are not allowed.", "red")
        invalid = True
    if(not invalid):
        if(instruction == "create"):
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
        return(f"<button x-init=\"window.location.href='{url_for('epchar.stats', ruleset=cruleset.identifier)}'\">{'Submit Changes' if stat else 'Create Ability Score!'}</button>")
    elif(instruction=="create"):
        return(f"<button x-init=\"window.location.href='{url_for('epchar.createStat', ruleset=cruleset.identifier)}'\">Create Ability Score!</button>")
    return(f"<button x-init=\"window.location.href='{url_for('epchar.stats', ruleset=cruleset.identifier)}'\">Submit Changes</button>")

def abilityScoreImporter(scores, cruleset):
    if(cruleset.userid != current_user.id):
        flash("You cannot import races into rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.importRace", ruleset=cruleset.identifier)))
    try:
        for i, score in enumerate(scores):
            name = score["name"]
            order = score["order"]
            abbr = score["abbr"]
            text = score["text"]
            if(len(name) < 1):
                flash(f"Each ability score must have a name; skipping index {i}...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"Ability score {name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(abbr) != 3):
                flash(f"Ability score abbreviations must be three characters; skipping {name}...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_ability_score = AbilityScore(
                ruleset = cruleset,
                name = name,
                order = order,
                abbr = abbr,
                text = text
            )
            db.session.add(new_ability_score)
        db.session.commit()
        flash("Ability scores imported!", "green")
        return(redirect(url_for("epchar.stats", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("epchar.importStats", ruleset=cruleset.identifier)))

def makeRace(request, cruleset, race, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create a race in a ruleset that is not yours.")
        return(f"<button x-init=\"window.location.href='{url_for('epchar.races', ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
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
        return(f"<button x-init=\"window.location.href='{url_for('epchar.races', ruleset=cruleset.identifier)}'\">Duplicate {race.name}</button>")
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
        else:
            for feature in features:
                if(len(feature) < 1):
                    flash("Each racial feature must have a name.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                elif(len(feature) > 127):
                    flash("Racial feature names must be fewer than 128 characters.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
            for ftext in feature_text:
                if(len(ftext) > 16383):
                    flash("Racial feature text must be fewer than 16384 characters.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                elif("<" in ftext):
                    flash("Open angle brackets (\"<\") are not allowed.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                elif("javascript" in ftext):
                    flash("Cross-site scripting attacks are not allowed.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
            if(has_subraces):
                for subrace in subraces:
                    if(len(subrace["name"]) < 1):
                        flash("You must specify a name for each subrace.", "red")
                        return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                    elif(len(subrace["name"]) > 127):
                        flash("Subrace names must be fewer than 128 characters.", "red")
                        return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                    elif(len(subrace["text"]) > 16383):
                        flash("Subrace descriptions must be fewer than 16384 characters.", "red")
                        return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                    elif("<" in subrace["text"]):
                        flash("Open angle brackets (\"<\") are not allowed.", "red")
                        return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                    elif("javascript" in subrace["text"]):
                        flash("Cross-site scripting attacks are not allowed.", "red")
                        return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                    for feature in subrace["features"]:
                        if(len(feature["name"]) < 1):
                            flash("You must specify a name for each subrace features.", "red")
                            return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                        elif(len(feature["name"]) > 127):
                            flash("Subrace feature names must be fewer than 128 characters.", "red")
                            return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                        elif(len(feature["text"]) > 16383):
                            flash("Subrace feature text must be fewer than 16384 characters.", "red")
                            return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                        elif("<" in feature["text"]):
                            flash("Open angle brackets (\"<\") are not allowed.", "red")
                            return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
                        elif("javascript" in feature["text"]):
                            flash("Cross-site scripting attacks are not allowed.", "red")
                            return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
            if(instruction == "create"):
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
                return(f"<button x-init=\"window.location.href='{url_for('epchar.races', ruleset=cruleset.identifier)}'; localStorage.removeItem('cached_race')\">{'Submit Changes' if race else 'Create Race!'}</button>")
            else:
                race.name = name
                race.flavor = flavor
                race.asis = asis
                race.asi_text = asi_text
                race.size = size
                race.size_text = size_text
                race.walk = walk
                race.swim = swim
                race.fly = fly
                race.burrow = burrow
                race.base_height = base_height
                race.height_num = height_num
                race.height_die = height_die
                race.base_weight = base_weight
                race.weight_num = weight_num
                race.weight_die = weight_die
                race.subrace_flavor = subrace_flavor
                for i, feature in enumerate(race.race_features):
                    if(len(features) < i + 1):
                        db.session.delete(feature)
                    else:
                        feature.name = features[i]
                        feature.text = feature_text[i]
                for i in range(len(race.race_features), len(features)):
                    new_feature = RaceFeature(
                        raceid = race.id,
                        name = features[i],
                        text = feature_text[i]
                    )
                    db.session.add(new_feature)
                if(has_subraces):
                    for i, subrace in enumerate(race.subraces):
                        if(len(subraces) < i + 1):
                            db.session.delete(subrace)
                        else:
                            subrace.name = subraces[i]["name"]
                            subrace.text = subraces[i]["text"]
                            for j, feature in enumerate(subrace.subrace_features):
                                if(len(subraces[i]["features"]) < j + 1):
                                    print("deleting")
                                    db.session.delete(feature)
                                else:
                                    feature.name = subraces[i]["features"][j]["name"]
                                    feature.text = subraces[i]["features"][j]["text"]
                            for j in range(len(subrace.subrace_features), len(subraces[i]["features"])):
                                new_feature = SubraceFeature(
                                    subrace = subrace,
                                    name = subraces[i]["features"][j]["name"],
                                    text = subraces[i]["features"][j]["text"]
                                )
                                db.session.add(new_feature)
                    for i in range(len(race.subraces), len(subraces)):
                        new_subrace = Subrace(
                            raceid = race.id,
                            name = subraces[i]["name"],
                            text = subraces[i]["text"]
                        )
                        db.session.add(new_subrace)
                        for feature in subraces[i]["features"]:
                            new_feature = SubraceFeature(
                                subraceid = new_subrace.id,
                                name = feature["name"],
                                text = feature["text"]
                            )
                            db.session.add(new_feature)
                else:
                    for subrace in race.subraces:
                        for feature in subrace.subrace_features:
                            db.session.delete(feature)
                        db.session.delete(subrace)
                db.session.commit()
                flash("Changes saved!", "green")
                return(f"<button x-init=\"window.location.href='{url_for('epchar.races', ruleset=cruleset.identifier)}'; localStorage.removeItem('cached_race')\">{'Submit Changes' if race else 'Create Race!'}</button>")
        return(f"<button x-init=\"window.location.href='{url_for('epchar.createRace', ruleset=cruleset.identifier) if not race else url_for('epchar.editRace', race=race.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")

def raceImporter(races, cruleset):
    if(cruleset.userid != current_user.id):
        flash("You cannot import races into rulesets that are not your own", "red")
        return(redirect(url_for("epchar.importRace", ruleset=cruleset.identifier)))
    try:
        for i, race in enumerate(races):
            name = race["name"]
            flavor = race["flavor"]
            images = race["images"]
            asis = race["asis"]
            asi_text = race["asi_text"]
            size = race["size"]
            size_text = race["size_text"]
            walk = race["walk"]
            climb = race["climb"]
            fly = race["fly"]
            swim = race["swim"]
            burrow = race["burrow"]
            base_height = race["base_height"]
            base_weight = race["base_weight"]
            height_num = race["height_num"]
            height_die = race["height_die"]
            weight_num = race["weight_num"]
            weight_die = race["weight_die"]
            subrace_flavor = race["subrace_flavor"]

            if(len(name) < 1):
                flash(f"Each race must have a name; skipping index {i}...", "orange")
                continue
            if(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(flavor and len(flavor) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(images)) > 16384):
                flash(f"{name} has too many images (maximum raw data size of links 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(asis)) > 16384):
                flash(f"{name} has too many ability score improvements (maximum raw data size of list 16KiB); skipping...", "orange")
                continue
            elif(asi_text and len(asi_text) > 255):
                flash(f"{name} ability score improvement text too long (maximum 255 characters); skipping...", "orange")
                continue
            elif(size_text and len(size_text) > 255):
                flash(f"{name} size text too long (maximum 255 characters); skipping...", "orange")
                continue
            elif(subrace_flavor and len(subrace_flavor) > 16383):
                flash(f"{name} subrace flavor text too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_race = Race(
                ruleset = cruleset,
                name = name,
                flavor = flavor,
                images = images,
                asis = asis,
                asi_text = asi_text,
                size = size,
                size_text = size_text,
                walk = walk,
                climb = climb,
                fly = fly,
                swim = swim,
                burrow = burrow,
                base_height = base_height,
                base_weight = base_weight,
                height_num = height_num,
                height_die = height_die,
                weight_num = weight_num,
                weight_die = weight_die,
                subrace_flavor = subrace_flavor
            )
            db.session.add(new_race)
            for j, feature in enumerate(race["race_features"]):
                name = feature["name"]
                text = feature["text"]

                if(len(name) < 1):
                    flash(f"{new_race.name} feature at index {j} is missing a name; skipping...", "orange")
                    continue
                elif(len(name) > 127):
                    flash(f"{new_race.name} feature {name} name too long (maximum 127 characters); skipping...", "orange")
                    continue
                elif(text and len(text) > 16383):
                    flash(f"{new_race.name} feature {name} description too long (maximum 16383 characters); skipping...", "orange")
                    continue
                new_race_feature = RaceFeature(
                    race = new_race,
                    name = name,
                    text = text
                )
                db.session.add(new_race_feature)
            for j, subrace in enumerate(race["subraces"]):
                name = subrace["name"]
                text = subrace["text"]
                images = subrace["images"]

                if(len(name) < 1):
                    flash(f"{new_race.name} feature at index {j} is missing a name; skipping...", "orange")
                    continue
                elif(len(name) > 127):
                    flash(f"{new_race.name} subrace {name} name too long (maximum 127 characters); skipping...", "orange")
                    continue
                elif(text and len(text) > 16383):
                    flash(f"{new_race.name} subrace {name} description too long (maximum 16383 characters); skipping...", "orange")
                    continue
                elif(sys.getsizeof(pickle.dumps(images)) > 16384):
                    flash(f"{new_race.name} subrace {name} has too many images (maximum raw data size of links 16KiB); skipping...", "orange")
                    continue
                new_subrace = Subrace(
                    race = new_race,
                    name = name,
                    text = text,
                    images = images
                )
                db.session.add(new_subrace)
                for k, feature in enumerate(subrace["subrace_features"]):
                    name = feature["name"]
                    text = feature["text"]

                    if(len(name) < 1):
                        flash(f"{new_race.name} subrace {new_subrace.name} feature at index {k} is missing a name; skipping...", "orange")
                        continue
                    elif(len(name) > 127):
                        flash(f"{new_race.name} subrace {new_subrace.name} feature {name} name too long (maximum 127 characters); skipping...", "orange")
                        continue
                    elif(text and len(text) > 16383):
                        flash(f"{new_race.name} subrace {new_subrace.name} feature {name} description too long (maximum 16383 characters); skipping...", "orange")
                        continue
                    new_subrace_feature = SubraceFeature(
                        subrace = new_subrace,
                        name = name,
                        text = text
                    )
                    db.session.add(new_subrace)
        db.session.commit()
        flash("Races imported!", "green")
        return(f"<button x-init=\"window.location.href='{url_for('epchar.races', ruleset=cruleset.identifier)}'\">{'Submit Changes' if race else 'Create Race!'}</button>")
    except:
        flash("Improperly formatted JSON; could not import.", "red")
        return(redirect(url_for("epchar.importRaces", ruleset=cruleset.identifier)))

def makebackground(request, cruleset, background, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create backgrounds in rulesets that are not your own.", "red")
    elif(instruction == "duplicate"):
        new_background = Background(
            rulesetid = background.rulesetid,
            name = f"{background.name} Duplicate",
            skills = background.skills,
            tools = background.tools,
            lang_num = background.lang_num,
            languages = background.languages,
            equipment = background.equipment,
            text = background.text
        )
        db.session.add(new_background)
        db.session.commit()
        new_background = Background.query.filter_by(rulesetid = cruleset.id, name=new_background.name).first()
        for feature in background.background_features:
            new_background_feature = BackgroundFeature(
                backgroundid = new_background.id,
                name = feature.name,
                text = feature.text
            )
            db.session.add(new_background_feature)
            db.session.commit()
        flash("Background Duplicated!", "green")
    else:
        name = request.form.get("name")
        skills = request.form.getlist("skill")
        tools = request.form.getlist("tool")
        lang_num = request.form.get("lang_num")
        if(not lang_num):
            lang_num = 0
        languages = request.form.getlist("language")
        items = request.form.getlist("item")
        goldcontainer = request.form.get("goldcontainer")
        startinggold = request.form.get("gold")
        text = request.form.get("text")
        featurenames = request.form.getlist("featurename")
        featuretexts = request.form.getlist("featuretext")
        if(len("name") < 1 or not name):
            flash("You must specify a background name.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
        elif(len("name") > 127):
            flash("Background name must be fewer than 128 characters.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
        elif(len("text") > 16383):
            flash("Text must be fewer than 16384 characters.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
        elif("<" in "text"):
            flash("Open angle brackets(\"<\") are not allowed.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
        elif("javascript" in "text"):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
        elif(len(goldcontainer) > 127):
            flash("Starting gold container name must be fewer than 128 characters.")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
        else:
            for index, feature in enumerate(featurenames):
                if(len(feature) < 1):
                    flash("You must specify a feature name.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
                elif(len(feature) > 127):
                    flash("Feature name must be fewer than 128 characters.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
                elif(len(featuretexts[index]) > 16383):
                    flash("Text must be fewer than 16383 characters.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
                elif("<" in featuretexts[index]):
                    flash("Open angle brackets(\"<\") are not allowed.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
                elif("javascript" in featuretexts[index]):
                    flash("Cross-site scripting attacks are not allowed.", "red")
                    return(f"<button x-init=\"window.location.href='{url_for('epchar.createBackground', ruleset=cruleset.identifier) if not background else url_for('epchar.editBackground', background=background.name, ruleset=cruleset.name)}'\">Create Background!</button>")
            if(instruction == "create"):
                new_background = Background(
                    rulesetid = cruleset.id,
                    name = name,
                    skills = skills,
                    tools = tools,
                    lang_num = lang_num,
                    languages = languages,
                    equipment = items,
                    gold_container = goldcontainer,
                    starting_gold = startinggold,
                    text = text
                )
                db.session.add(new_background)
                db.session.commit()

                new_background = Background.query.filter_by(
                    name = name,
                    rulesetid = cruleset.id
                ).first()
                for index, feature in enumerate(featurenames):
                    new_feature = BackgroundFeature(
                        backgroundid = new_background.id,
                        name = feature,
                        text = featuretexts[index]
                    )
                    db.session.add(new_feature)
                db.session.commit()
                flash("Background created!", "green")
            else:
                background.name = name
                background.skills = skills
                background.tools = tools
                background.lang_num = lang_num
                background.languages = languages
                background.equipment = items
                background.text = text
                featurenum = 0
                for index, feature in enumerate(background.background_features):
                    feature.name = featurenames[index]
                    feature.text = featuretexts[index]
                    featurenum += 1
                db.session.commit()
                if(len(featurenames) > featurenum):
                    for index, feature in enumerate(featurenames):
                        if(index + 1 > featurenum):
                            new_background_feature = BackgroundFeature(
                                backgroundid = background.id,
                                name = feature,
                                text = featuretexts[index]
                            )
                            db.session.add(new_background_feature)
                    db.session.commit()
                flash("Changes saved!", "green")

    return(f"<button x-init=\"window.location.href='{url_for('epchar.backgrounds', ruleset=cruleset.identifier)}'; localStorage.removeItem('cached_background')\">{'Submit Changes' if background else 'Create Background!'}</button>")
    return(redirect(url_for("epchar.backgrounds", ruleset=cruleset.identifier)))

def backgroundImporter(backgrounds, flavor, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import backgrounds into rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.backgrounds", ruleset=cruleset.identifier)))
    try:
        for i, background in enumerate(backgrounds):
            name = background["name"]
            skills = background["skills"]
            tools = background["tools"]
            lang_num = background["lang_num"]
            languages = background["languages"]
            equipment = background["equipment"]
            gold_container = background["gold_container"]
            starting_gold = background["starting_gold"]
            text = background["text"]
            images = background["images"]

            if(len(name) < 1):
                flash(f"Background at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(skills)) > 16384):
                flash(f"{name} has too many skills (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(tools)) > 16384):
                flash(f"{name} has too many tool proficiencies (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(languages)) > 16384):
                flash(f"{name} has too many language proficiencies (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(equipment)) > 16384):
                flash(f"{name} has too much starting equipment (Maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(len(gold_container) > 127):
                flash(f"{name} gold container name ({gold_container}) too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(images)) > 16384):
                flash(f"{name} has too many images (maximum raw size of list of links 16 KiB); skipping...", "orange")
                continue
            new_background = Background(
                ruleset = cruleset,
                name = name,
                skills = skills,
                tools = tools,
                lang_num = lang_num,
                languages = languages,
                equipment = equipment,
                gold_container = gold_container,
                starting_gold = starting_gold,
                text = text,
                images = images
            )
            db.session.add(new_background)
            for j, feature in enumerate(background["background_features"]):
                name = feature["name"]
                text = feature["text"]
                if(len(name) < 1):
                    flash(f"{new_background.name} feature at index {j} has no name; skipping...", "orange")
                    continue
                elif(len(name) > 127):
                    flash(f"{new_background.name} feature {name} name too long (maximum 127 characters); skipping...", "orange")
                    continue
                elif(len(text) > 16383):
                    flash(f"{new_background.name} feature {name} description too long (maximum 16383 characters); skipping...", "orange")
                    continue
                new_background_feature = BackgroundFeature(
                    background = new_background,
                    name = name,
                    text = text
                )
                db.session.add(new_background_feature)
        db.session.commit()
        flash("Backgrounds Imported!", "green")
        return(redirect(url_for('epchar.backgrounds', ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; unable to import.", "red")
        return(redirect(url_for("epchar.importBackgrounds", ruleset=cruleset.identifier)))

def makefeat(request, cruleset, tfeat, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create feats in rulesets that are not your own.", "red")
    elif(instruction == "duplicate"):
        new_feat = Feat(
            rulesetid = cruleset.id,
            name = f"{tfeat.name} Duplicate",
            prerequisite = tfeat.prerequisite,
            text = tfeat.text
        )
        db.session.add(new_feat)
        db.session.commit()
        flash("Feat duplicated!", "green")
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        prereq = request.form.get("prereq")
        if(len(name) < 1):
            flash("You must specify a feat name.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createFeat', ruleset=cruleset.identifier) if not tfeat else url_for('epchar.editFeat', feat=tfeat.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if tfeat else 'Create Feat!'}</button>")
        elif(len(name) > 127):
            flash("Feat name must be fewer than 128 characters.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createFeat', ruleset=cruleset.identifier) if not tfeat else url_for('epchar.editFeat', feat=tfeat.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if tfeat else 'Create Feat!'}</button>")
        elif(len(prereq) > 255):
            flash("Feat Prerequisite must be fewer than 256 characters.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createFeat', ruleset=cruleset.identifier) if not tfeat else url_for('epchar.editFeat', feat=tfeat.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if tfeat else 'Create Feat!'}</button>")
        elif(len(text) > 16383):
            flash("Feat description must be fewer than 16384 characters.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createFeat', ruleset=cruleset.identifier) if not tfeat else url_for('epchar.editFeat', feat=tfeat.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if tfeat else 'Create Feat!'}</button>")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createFeat', ruleset=cruleset.identifier) if not tfeat else url_for('epchar.editFeat', feat=tfeat.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if tfeat else 'Create Feat!'}</button>")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(f"<button x-init=\"window.location.href='{url_for('epchar.createFeat', ruleset=cruleset.identifier) if not tfeat else url_for('epchar.editFeat', feat=tfeat.name, ruleset=cruleset.identifier)}'\">{'Submit Changes' if tfeat else 'Create Feat!'}</button>")
        else:
            if(instruction == "create"):
                new_feat = Feat(
                    rulesetid = cruleset.id,
                    name = name,
                    prerequisite = prereq,
                    text = text
                )
                db.session.add(new_feat)
                db.session.commit()
                flash("Feat created!", "green")
            else:
                tfeat.name = name
                tfeat.prerequisite = prereq
                tfeat.text = text
                db.session.commit()
                flash("Changes saved!", "green")
    return(f"<button x-init=\"window.location.href='{url_for('epchar.feats', ruleset=cruleset.identifier)}'; localStorage.removeItem('cached_feat')\">{'Submit Changes' if tfeat else 'Create Feat!'}</button>")

def featImporter(feats, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import feats into rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.feats", ruleset=cruleset.identifier)))
    try:
        for i, feat in enumerate(feats):
            name = feat["name"]
            prerequisite = feat["prerequisite"]
            text = feat["text"]
            
            if(len(name) < 1):
                flash(f"Feat at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(prerequisite) > 255):
                flash(f"{name} prerequisite too long (maximum 255 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            new_feat = Feat(
                ruleset = cruleset,
                name = name,
                prerequisite = prerequisite,
                text = text
            )
            db.session.add(new_feat)
        db.session.commit()
        flash("Feats imported!", "green")
        return(redirect(url_for("epchar.feats", ruleset=cruleset.identifier)))

    except:
        flash("Improperly formatted JSON; unable to import.", "red")
        return(redirect(url_for("epchar.importFeats", ruleset=cruleset.identifier)))

def makeclass(request, cruleset, tclass, instruction, adminrulesets):
    if(current_user.id != cruleset.userid):
        flash("You cannot create classes in rulesets that are not your own.", "red")
    elif(instruction == "duplicate"):
        new_class = Playerclass(
            name = f"{tclass.name} Duplicate",
            text = tclass.text,
            hitdie = tclass.hitdie,
            proficiencies = tclass.proficiencies,
            saves = tclass.saves,
            equipment = tclass.equipment,
            gold_nums = tclass.gold_nums,
            gold_dice = tclass.gold_dice,
            gold_mult = tclass.gold_mult,
            multiclass_prereq = tclass.multiclass_prereq,
            multiclass_profic = tclass.multiclass_profic,
            subclass_name = tclass.subclass_name,
            subclass_level = tclass.subclass_level,
            levels = tclass.levels,
            skill_num = tclass.skill_num,
            skills = tclass.skills
        )
        db.session.add(new_class)
        db.session.commit()
        new_class=Playerclass.query.filter_by(name=new_class.name, rulesetid=cruleset.id).first()
        for column in tclass.columns:
            new_column = ClassColumn(
                classid=new_class.id,
                name=column.name,
                data=column.data
            )
            db.session.add(new_column)
        for feature in tclass.features:
            new_feature = ClassFeature(
                classid=new_class.id,
                level_obtained=feature.level_obtained,
                name=feature.name,
                text=feature.text
            )
            db.session.add(new_feature)
        for subclass in tclass.subclasses:
            new_subclass = Subclass(
                classid=new_class.id,
                name=subclass.name,
                text=subclass.text,
                caster_type=subclass.caster_type
            )
            db.session.add(new_class)
            db.session.commit()
            new_subclass=Subclass.query.filter_by(classid=new_class.id, name=subclass.name).first()
            for column in subclass.columns:
                new_subclass_column = SubclassColumn(
                    subclassid=new_subclass.id,
                    name=column.name,
                    data=column.data
                )
                db.session.add(new_subclass_column)
            for feature in subclass.features:
                new_subclass_feature = SubclassFeature(
                    subclassid=new_subclass.id,
                    name=feature.name,
                    text=feature.text,
                    level_obtained=feature.level_obtained
                )
                db.session.add(new_subclass_feature)
        db.session.commit()
        flash("Class duplicated!", "green")
    else:
        invalid = False
        name = request.form.get("name")
        text = request.form.get("text")
        hitdie = request.form.get("hitdie")
        proficiencies = request.form.getlist("proficiency")
        try:
            skill_num = int(request.form.get("skill_num"))
        except:
            flash("Number of skills must be a number", "red")
            skill_num = 0
            invalid = True
        if(not skill_num):
            skill_num = 0
        skills = request.form.getlist("skill")
        saves = []
        for i in range(AbilityScore.query.filter_by(rulesetid=cruleset.id).count()):
            if(request.form.get(f"save-{i}") == "true"):
                saves.append(True)
            else:
                saves.append(False)
        equipment = request.form.get("equipment")
        gold_nums = request.form.get("gold_nums")
        try:
            gold_nums = int(gold_nums)
        except:
            flash("Number of dice rolled for starting gold must be a number.", "red")
            gold_nums = 0
            invalid = True
        gold_dice = request.form.get("gold_dice")
        gold_mult = request.form.get("gold_mult")
        try:
            gold_mult = int(gold_mult)
        except:
            flash("Starting gold multiplier must be a number.", "red")
            gold_mult = 0
            invalid = True
        multiclass_prereq = request.form.get("prereq")
        multiclass_profic = request.form.getlist("multiprofic")
        subclass_name = request.form.get("subclassname")
        subclass_level = int(request.form.get("subclasslevel"))
        levels = request.form.get("levels")
        try:
            levels = int(levels)
        except:
            flash("Max level must be a number.", "red")
            levels = 0
            invalid = True
        if(len(name) < 1):
            flash("You must specify a class name.", "red")
            invalid = True
        elif(len(name) > 127):
            flash("Class name must be fewer than 128 characters.", "red")
            invalid = True
        elif(len(text) > 16383):
            flash("Class description must be fewer than 16383 characters.", "red")
            invalid = True
        elif(len(equipment) > 1023):
            flash("Class equipment must be fewer than 1024 characters.", "red")
            invalid = True
        elif(len(multiclass_prereq) > 1023):
            flash("Multiclassing prerequisites must be fewer than 1024 characters.", "red")
            invalid = True
        elif(len(subclass_name) > 127):
            flash("Subclass title must be fewer than 128 characters.", "red")
            invalid = True
        for i, column in enumerate(request.form.getlist("columnname")):
            if(len(column) < 1):
                invalid = True
                flash("Each custom column must have a name.", "red")
            elif(len(column) > 127):
                invalid = True
                flash("Custom column names must be fewer than 128 characters.", "red")
            for value in request.form.getlist(f"column{i}value"):
                if(len(value) > 127):
                    invalid = True
                    flash("Custom column values must be fewer than 128 characters.", "red")
        for i, feature in enumerate(request.form.getlist("class_feature_name")):
            try:
                testint = int(request.form.getlist("level")[i])
            except:
                invalid = True
                flash("Feature levels must be numbers.", "red")
            if(len(feature) < 1):
                invalid = True
                flash("You must specify a name for each class feature", "red")
            elif(len(feature) > 127):
                invalid = True
                flash("Class feature names must be fewer than 128 characters", "red")
            elif(len(request.form.getlist("class_feature_text")[i]) > 16383):
                invalid = True
                flash("Class feature text must be fewer than 128 characters", "red")
        for i, subclass in enumerate(request.form.getlist("subclass_name")):
            if(len(subclass) < 1):
                invalid = True
                flash("You must specify a name for each subclass.", "red")
            elif(len(subclass) > 127):
                invalid = True
                flash("Subclass names must be fewer than 128 characters.", "red")
            elif(len(request.form.getlist("subclass_text")[i]) > 16383):
                invalid = True
                flash("Subclass descriptions must be fewer than 16383 characters.", "red")
            elif("<" in request.form.getlist("subclass_text")[i]):
                invalid = True
                flash("Open angle brackets (\"<\") are not allowed.", "red")
            elif("javascript" in request.form.getlist("subclass_text")[i]):
                invalid = True
                flash("Cross-site scripting attacks are not allowed.", "red")
            for j, feature in enumerate(request.form.getlist(f"subclass_{i}_feature_name")):
                try:
                    testint = int(request.form.getlist(f"subclass_{i}_feature_level")[j])
                except:
                    invalid = True
                    flash("Subclass feature levels must be numbers.", "red")
                if(len(feature) < 1):
                    invalid = True
                    flash("You must specify a name for each subclass feature.", "red")
                elif(len(feature) > 127):
                    invalid = True
                    flash("Subclass feature names must be fewer than 128 characters.", "red")
                elif(len(request.form.getlist(f"subclass_{i}_feature_text")[j]) > 16383):
                    invalid = True
                    flash("Subclass feature descriptions must be fewer than 16383 characters.", "red")
                elif("<" in request.form.getlist(f"subclass_{i}_feature_text")[j]):
                    invalid = True
                    flash("Open angle brackets (\"<\") are not allowed.", "red")
                elif("javascript" in request.form.getlist(f"subclass_{i}_feature_text")[j]):
                    invalid = True
                    flash("Cross-site scripting attacks are not allowed.", "red")
            for j, column in enumerate(request.form.getlist(f"subclass{i}columnname")):
                if(len(column) < 1):
                    invalid = True
                    flash("You must specify a name for each subclass' custom columns.", "red")
                elif(len(column) > 127):
                    invalid = True
                    flash("Each subclass' custom column names must be fewer than 128 characters.", "red")
                for value in request.form.getlist(f"subclass{i}column{j}value"):
                    if(len(value) > 127):
                        invalid = True
                        flash("Each subclass' custom column values must be fewer than 128 characters.", "red")
        if(instruction == "create"):
            if(invalid):
                return(f"<button x-init=\"window.location.href='{url_for('epchar.createClass', ruleset=cruleset.identifier)}'\">Create Class!</button>")
            new_class = Playerclass(
                rulesetid = cruleset.id,
                name = name,
                hitdie = hitdie,
                proficiencies = proficiencies,
                saves = saves,
                equipment = equipment,
                gold_nums = gold_nums,
                gold_dice = gold_dice,
                gold_mult = gold_mult,
                multiclass_prereq = multiclass_prereq,
                multiclass_profic = multiclass_profic,
                subclass_name = subclass_name,
                subclass_level = subclass_level,
                levels = levels,
                text = text,
                skill_num = skill_num,
                skills = skills
            )
            for i, column in enumerate(request.form.getlist("columnname")):
                new_class.class_columns.append(ClassColumn(
                    name = column,
                    data = request.form.getlist(f"column{i}value")
                ))
            for i, feature in enumerate(request.form.getlist("class_feature_name")):
                new_class.class_features.append(ClassFeature(
                    level_obtained = request.form.getlist("level")[i],
                    name = feature,
                    text = request.form.getlist("class_feature_text")[i]
                ))
            for i, sublcass in enumerate(request.form.getlist("subclass_name")):
                new_class.subclasses.append(Subclass(
                    name = subclass,
                    text = request.form.getlist("subclass_text")[i],
                    caster_type = request.form.getlist("castertype")[i],
                ))
                for j, feature in enumerate(request.form.getlist(f"subclass_{i}_feature_name")):
                    new_class.subclasses[i].subclass_features.append(SubclassFeature(
                        level_obtained = request.form.getlist(f"subclass_{i}_feature_level")[j],
                        name = feature,
                        text = request.form.getlist(f"subclass_{i}_feature_text")[j]
                    ))
                for j, column in enumerate(request.form.getlist(f"subclass{i}columnname")):
                    new_class.subclasses[i].subclass_columns.append(SubclassColumn(
                        name = column,
                        data = request.form.getlist(f"subclass{i}column{j}value")
                    ))
            db.session.add(new_class)
            db.session.commit()
            flash("Class Created!", "green")
        else:
            if(invalid):
                return(f"<button x-init=\"window.location.href='{url_for('epchar.editClass', tclass=tclass, ruleset=cruleset.identifier)}'\">Submit Changes</button>")
            tclass.name = name
            tclass.hitdie = hitdie
            tclass.proficiencies = proficiencies
            tclass.saves = saves
            tclass.equipment = equipment
            tclass.gold_nums = gold_nums
            tclass.gold_dice = gold_dice
            tclass.gold_mult = gold_mult
            tclass.multiclass_prereq = multiclass_prereq
            tclass.multiclass_profic = multiclass_profic
            tclass.subclass_name = subclass_name
            tclass.subclass_level = subclass_level
            tclass.levels = levels
            tclass.text = text
            tclass.skills = skills
            for i, column in enumerate(tclass.class_columns):
                if(len(request.form.getlist("columnname")) < i + 1):
                    db.session.delete(column)
                else:
                    column.name = request.form.getlist("columnname")[i]
                    column.data = request.form.getlist(f"column{i}value")
            for i in range(len(tclass.class_columns), len(request.form.getlist("columnname"))):
                new_class_column = ClassColumn(
                    classid = tclass.id,
                    name = request.form.getlist("columnname")[i],
                    data = request.form.getlist(f"column{i}value")
                )
                db.session.add(new_class_column)

            for i, feature in enumerate(tclass.class_features):
                if(len(request.form.getlist("class_feature_name")) < i + 1):
                    db.session.delete(feature)
                else:
                    feature.name = request.form.getlist("class_feature_name")[i]     
                    feature.level_obtained = request.form.getlist("level")[i]
                    feature.text = request.form.getlist("class_feature_text")[i]
            for i in range(len(tclass.class_features), len(request.form.getlist("class_feature_name"))):
                new_class_feature = ClassFeature(
                    classid = tclass.id,
                    name = request.form.getlist("class_feature_name")[i],
                    level_obtained = request.form.getlist("level")[i],
                    text = request.form.getlist("class_feature_text")[i]
                )
                db.session.add(new_class_feature)
            
            for i, subclass in enumerate(tclass.subclasses):
                if(len(request.form.getlist("subclass_name")) < i + 1):
                    for column in subclass.columns:
                        db.session.delete(column)
                    for feature in subclass.subclass_features:
                        db.session.delete(feature)
                    db.session.delete(subclass)
                else:
                    subclass.name = request.form.getlist("subclass_name")[i]
                    subclass.text = request.form.getlist("subclass_text")[i]
                    subclass.caster_type = request.form.getlist("castertype")[i]\

                    for j, column in enumerate(subclass.subclass_columns):
                        if(len(request.form.getlist(f"subclass{i}columnname")) < j + 1):
                            db.session.delete(column)
                        else:
                            column.name = request.form.getlist(f"subclass{i}columnname")[j]
                            column.data = request.form.getlist(f"subclass{i}column{j}value")
                    for j in range(len(subclass.subclass_columns), len(request.form.getlist(f"subclass{i}columnname"))):
                        new_subclass_column = SubclassColumn(
                            subclassid = subclass.id,
                            name = request.form.getlist(f"subclass{i}columnname")[j],
                            data = request.form.getlist(f"subclass{i}column{j}name")
                        )
                        db.session.add(new_subclass_column)
                    
                    for j, feature in enumerate(subclass.subclass_features):
                        if(len(request.form.getlist(f"subclass_{i}_feature_name")) < j + 1):
                            db.session.delete(feature)
                        else:
                            feature.name = request.form.getlist(f"subclass_{i}_feature_name")[j]
                            feature.level_obtained = request.form.getlist(f"subclass_{i}_feature_level")[j]
                            feature.text = request.form.getlist(f"subclass_{i}_feature_text")[j]
                    for j in range(len(subclass.subclass_features), len(request.form.getlist(f"subclass_{i}_feeature_name"))):
                        new_subclass_feature = SubclassFeature(
                            subclassid = subclass.id,
                            name = request.form.getlist(f"subclass_{i}_feature_name")[j],
                            text = request.form.getlist(f"subclass_{i}_feature_text")[j]
                        )
                        db.session.add(new_subclass_feature)
            for i in range(len(tclass.subclasses), len(request.form.getlist("subclass_name"))):
                new_subclass = Subclass(
                    classid = tclass.id,
                    name = request.form.getlist("subclass_name")[i],
                    text = request.form.getlist("subclass_text")[i],
                    caster_type = request.form.getlist("castertype")[i]
                )
                for j, column in enumerate(request.form.getlist(f"subclass{i}columnname")):
                    new_subclass_column = SubclassColumn(
                        subclassid = new_subclass.id,
                        name = column,
                        data = request.form.getlist(f"subclass{i}column{j}value")
                    )
                    db.session.add(new_subclass_column)
                for j, feature in enumerate(request.form.getlist(f"subclass_{i}_feature_name")):
                    new_subclass_feature = SubclassFeature(
                        subclassid = new_subclass.id,
                        name = feature,
                        level_obtained = request.form.getlist(f"subclass_{i}_feature_level")[j],
                        text = request.form.getlist(f"subclass_{i}_feature_text")[j]
                    )
                    db.session.add(new_subclass_feature)
                db.session.add(new_subclass)
            db.session.commit() 
            flash("Changes saved!", "green")
        return(f"<button x-init=\"window.location.href='{url_for('epchar.classes', ruleset=cruleset.identifier)}'\">{'Submit Changes' if tclass else 'Create Class'}</button>")

def classImporter(classes, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import classes into rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.classes", ruleset=cruleset.identifier)))
    try:
        for i, playerclass in classes:
            name = playerclass["name"]
            hitdie = playerclass["hitdie"]
            proficiencies = playerclass["proficiencies"]
            saves = playerclass["saves"]
            skill_num = playerclass["skill_num"]
            skills = playerclass["skills"]
            equipment = playerclass["equipment"]
            gold_nums = playerclass["gold_nums"]
            gold_dice = playerclass["gold_dice"]
            gold_mult = playerclass["gold_mult"]
            multiclass_prereq = playerclass["multiclass_prereq"]
            multiclass_profic = playerclass["multiclass_profic"]
            subclass_name = playerclass["subclass_name"]
            subclass_level = playerclass["subclass_level"]
            levels = playerclass["levels"]
            text = playerclass["text"]
            images = playerclass["images"]

            if(len(name) < 1):
                flash(f"Class at index {i} has no name; skipping...", "orange")
                continue
            elif(len(name) > 127):
                flash(f"{name} name too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(proficiencies)) > 16384):
                flash(f"{name} has too many proficiencies (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(saves)) > 16384):
                flash(f"{name} has too many saving throw proficiencies (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(skills)) > 16384):
                flash(f"{name} has too many skill proficiency choices (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(len(equipment) > 1023):
                flash(f"{name} starting equipment too long (maximum 1023 characters); skipping...", "orange")
                continue
            elif(len(multiclass_prereq) > 1023):
                flash(f"{name} multiclass prerequisites too long (maximum 1023 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(multiclass_profic)) > 16384):
                flash(f"{name} has too many proficiencies granted on multiclass (maximum raw data size 16KiB); skipping...", "orange")
                continue
            elif(len(subclass_name) > 127):
                flash(f"{name} subclass title ({subclass_name}) too long (maximum 127 characters); skipping...", "orange")
                continue
            elif(len(text) > 16383):
                flash(f"{name} description too long (maximum 16383 characters); skipping...", "orange")
                continue
            elif(sys.getsizeof(pickle.dumps(images))):
                flash(f"{name} has too many images (maximum raw data size of list of links 16KiB); skipping...")
                continue
            new_class = Playerclass(
                ruleset = cruleset,
                name = name,
                hitdie = hitdie,
                proficiencies = proficiencies,
                saves = saves,
                skill_num = skill_num,
                skills = skills,
                equipment = equipment,
                gold_nums = gold_nums,
                gold_dice = gold_dice,
                gold_mult = gold_mult,
                multiclass_prereq = multiclass_prereq,
                multiclass_profic = multiclass_profic,
                subclass_name = subclass_name,
                subclass_level = subclass_level,
                levels = levels,
                text = text,
                images = images
            )
            db.session.add(new_class)
            for j, column in playerclass["class_columns"]:
                name = column["name"]
                data = column["data"]
                if(len(name) < 1):
                    flash(f"{new_class.name} column at index {j} has no name; skipping...", "orange")
                    continue
                elif(len(name) > 127):
                    flash(f"{new_class.name} column {name} name too long (maximum 127 characters); skipping...", "orange")
                    continue
                elif(sys.getsizeof(pickle.dumps(data))):
                    flash(f"{new_class} column {name} has too much data (maximum 16KiB); skipping...", "orange")
                    continue
                new_class_column = classColumn(
                    playerclass = new_class,
                    name = name,
                    data = data
                )
                db.session.add(new_column)
            for j, feature in playerclass["class_features"]:
                level_obtained = feature["level_obtained"]
                name = feature["name"]
                text = feature["text"]

                if(len(name) < 1):
                    flash(f"{new_class.name} feature at index {j} has no name; skipping...", "orange")
                    continue
                elif(len(name) > 127):
                    flash(f"{new_class.name} feature {name} name too long (maximum 127 characters); skipping...", "orange")
                    continue
                elif(len(text) > 16383):
                    flash(f"{new_class.name} feature {name} description too long (maximum 16383 characters); skipping...", "orange")
                    continue
                new_class_feature = ClassFeature(
                    playerclass = new_class,
                    level_obtained = level_obtained,
                    name = name,
                    text = text
                )
                db.session.add(new_class_feature)
            for j, subclass in playerclss["subclasses"]:
                name = subclass["name"]
                text = subclass["text"]
                images = subclass["images"]
                caster_type = subclass["caster_type"]

                if(len(name) < 1):
                    flash(f"{new_class.name} subclass at index {j} has no name; skipping...", "orange")
                    continue
                elif(len(name) > 127):
                    flash(f"{new_class.name} subclass {name} name too long (maximum 127 characters); skipping...", "orange")
                    continue
                elif(len(text) > 16383):
                    flash(f"{new_class.name} subclass {name} description too long (maximum 16383 characters); skipping...", "orange")
                    continue
                elif(sys.getsizeof(pickle.dumps(images)) > 16384):
                    flash(f"{new_class.name} subclass {name} has too many images (maximum raw data size of list of links 16KiB); skipping...", "orange")
                    continue
                new_subclass = Subclass(
                    playerclass = new_class,
                    name = name,
                    text = text,
                    images = images,
                    caster_type = caster_type
                )
                db.session.add(new_subclass)
                for k, column in subclass["subclass_columns"]:
                    name = column["name"]
                    data = column["data"]

                    if(len(name) < 1):
                        flash(f"{new_class.name} subclass {new_subclass.name} column at index {k} has no name; skipping...", "orange")
                        continue
                    elif(len(name) > 127):
                        flash(f"{new_class.name} subclass {new_subclass.name} column {name} name too long (maximum 127 characters); skipping...", "orange")
                        continue
                    elif(sys.getsizeof(pickle.dumps(data)) > 16384):
                        flash(f"{new_class.name} subclass {new_subclass.name} column {name} has too much data (maximum 16KiB); skipping...", "orange")
                        continue
                    new_subclass_column = SubclassColumn(
                        subclass = new_subclass,
                        name = name,
                        data = data
                    )
                    db.session.add(new_subclass)
                for k, feature in subclass["subclass_features"]:
                    level_obtained = feature["level_obtained"]
                    name = feature["name"]
                    text = feature["text"]

                    if(len(name) < 1):
                        flash(f"{new_class.name} subclass {new_subclass.name} feature at index {k} has no name; skipping...", "orange")
                        continue
                    if(len(name) > 127):
                        flash(f"{new_class.name} subclass {new_subclass.name} feature {name} name too long (maximum 127 characters); skipping...", "orange")
                        continue
                    if(len(text) > 16383):
                        flash(f"{new_class.name} subclass {new_subclass.name} feature {name} description too long (maximum 16383 characters); skipping...", "orange")
                        continue
                    new_subclass_feature = SubclassFeature(
                        subclass = new_subclass,
                        level_obtained = level_obtained,
                        name = name,
                        text = text
                    )
                    db.session.add(new_subclass)
        db.session.commit()
        flash("Classes imported!", "green")
        return(redirect(url_for("epchar.classes", ruleset=cruleset.identifier)))
    except:
        flash("Improperly formatted JSON; unable to import.", "red")
        return(redirect(url_for("epchar.importClass", ruleset=cruleset.identifier)))