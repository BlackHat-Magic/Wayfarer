from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature, Background, BackgroundFeature, Feat, Item, Playerclass, AbilityScore, ClassColumn, SubclassColumn, ClassFeature, Playerclass, Subclass, SubclassFeature

def convertTable(table):
    text = ""
    for label in table["colLabels"]:
        text += f"| {label} "
    text += "|\n"
    for style in table["colStyles"]:
        text += "| "
        if("center" in style.casefold() or "left" in style.casefold()):
            text += ":"
        text += "---"
        if("center" in style.casefold() or "right" in style.casefold()):
            text += ":"
        text += " "
    text += "|\n"
    for row in table["rows"]:
        for datum in row:
            text += f"| {datum}"
        text += "|\n"
    return(text)

def parseEntries(entries, depth, name):
    text = ""
    if(depth > 6):
        depth = 6
    for entry in entries:
        if(type(entry) == str):
            text += f"{entry}\n"
        elif(type(entry) == dict and entry["type"] == "list"):
            for item in entry["items"]:
                if(type(item) == str):
                    text += f" - {item}\n"
                elif("entry" in item.keys()):
                    text += f" - ***{item['name']}.*** {item['entry']}\n"
                else:
                    text += f" - ***{item['name']}.*** {item['entries'][0]}\n"
            text += "\n"
        elif(type(entry) == dict and entry["type"] == "table"):
            if("caption" in entry.keys()):
                text += f"##### {entry['caption']}\n\n"
            text += convertTable(entry)
        elif(type(entry) == dict and entry["type"] == "inset"):
            if("name" in entry.keys()):
                text += f"> ###### {entry['name']}\n\n"
            for paragraph in entry["entries"]:
                if(type(paragraph) == str):
                    text += f"> {paragraph}\n"
                else:
                    text += f"> ***{paragraph['name']}.*** {paragraph['entries'][0]}\n"
                text += "\n"
        elif(type(entry) == dict and entry["type"] == "quote"):
            for paragraph in entry["entries"]:
                text += f"> {paragraph}\n"
            text += "\n"
        elif(type(entry) == dict and entry["type"] == "entries"):
            if("name" in entry.keys()):
                for i in range(depth):
                    text += "#"
                text += f" {entry['name']}\n\n"
            text += parseEntries(entry["entries"], depth + 1, name)
        elif(type(entry) == dict and entry["type"] == "section"):
            if("name" in entry.keys()):
                for i in range(depth):
                    text += "#"
                text += f" {entry['name']}\n\n"
            text += parseEntries(entry["entries"], depth + 1, name)
        else:
            flash(f"Unrecognized entry type in {name}; skipping...", "orange")
        text += "\n"
    return(text)

def abilityScore(request, cruleset, ability_score, instruction):
    name = request.form.get("name")
    abbr = request.form.get("abbr").casefold()
    order = request.form.get("order")
    text = request.form.get("text")
    bad = False
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
        return(redirect(url_for("epchar.stats")))
    if(order):
        try:
            order = int(order)
        except:
            flash("Ability Score Order must be a number.")
            bad = True
    if(len(name) < 1):
        flash("You must specify an Ability Score name.", "red")
        bad = True
    elif(len(name) > 127):
        flash("Ability Score name must be fewer than 128 characters.", "red")
        bad = True
    elif(len(abbr) != 3):
        flash("Ability Score abbreviation must be 3 characters.", "red")
        bad = True
    elif(len(text) > 16383):
        flash("Ability Score description must be fewer than 16384 characters.", "red")
        bad = True
    elif("<" in text):
        flash("Open angle brackets (\"<\") are not allowed.", "red")
        bad = True
    elif("javascript" in text):
        flash("Cross-site scripting attacks are not allowed.", "red")
        bad = True
    if(not bad):
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
        return(redirect(url_for("epchar.stats")))
    elif(instruction=="create"):
        return(redirect(url_for("epchar.createStat")))
    else:
        return(redirect(url_for("epchar.editStat", score=ability_score.name.replace(" ", "-"))))

def makerace(request, cruleset, race, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create a race in a ruleset that is not yours.")
        return(redirect(url_for("epchar.races")))
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
                    return(redirect(url_for("epchar.createRace")))
                elif(len(feature) > 127):
                    flash("Racial feature names must be fewer than 128 characters.", "red")
                    return(redirect(url_for("epchar.createRace")))
            for ftext in feature_text:
                if(len(ftext) > 16383):
                    flash("Racial feature text must be fewer than 16384 characters.", "red")
                    return(redirect(url_for("epchar.createRace")))
                elif("<" in ftext):
                    flash("Open angle brackets (\"<\") are not allowed.", "red")
                    return(redirect(url_for("epchar.createRace")))
                elif("javascript" in ftext):
                    flash("Cross-site scripting attacks are not allowed.", "red")
                    return(redirect(url_for("epchar.createRace")))
            if(has_subraces):
                for subrace in subraces:
                    if(len(subrace["name"]) < 1):
                        flash("You must specify a name for each subrace.", "red")
                        return(redirect(url_for("epchar.createRace")))
                    elif(len(subrace["name"]) > 127):
                        flash("Subrace names must be fewer than 128 characters.", "red")
                        return(redirect(url_for("epchar.createRace")))
                    elif(len(subrace["text"]) > 16383):
                        flash("Subrace descriptions must be fewer than 16384 characters.", "red")
                        return(redirect(url_for("epchar.createRace")))
                    elif("<" in subrace["text"]):
                        flash("Open angle brackets (\"<\") are not allowed.", "red")
                        return(redirect(url_for("epchar.createRace")))
                    elif("javascript" in subrace["text"]):
                        flash("Cross-site scripting attacks are not allowed.", "red")
                        return(redirect(url_for("epchar.createRace")))
                    for feature in subrace["features"]:
                        if(len(feature["name"]) < 1):
                            flash("You must specify a name for each subrace features.", "red")
                            return(redirect(url_for("epchar.createRace")))
                        elif(len(feature["name"]) > 127):
                            flash("Subrace feature names must be fewer than 128 characters.", "red")
                            return(redirect(url_for("epchar.createRace")))
                        elif(len(feature["text"]) > 16383):
                            flash("Subrace feature text must be fewer than 16384 characters.", "red")
                            return(redirect(url_for("epchar.createRace")))
                        elif("<" in feature["text"]):
                            flash("Open angle brackets (\"<\") are not allowed.", "red")
                            return(redirect(url_for("epchar.createRace")))
                        elif("javascript" in feature["text"]):
                            flash("Cross-site scripting attacks are not allowed.", "red")
                            return(redirect(url_for("epchar.createRace")))
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
                return(redirect(url_for("epchar.races")))
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
                            sb.session.delete(subrace)
                        else:
                            subrace.name = subraces[i]["name"]
                            subrace.text = subraces[i]["text"]
                            for j, feature in enumerate(subrace.subrace_features):
                                if(len(subrace["features"]) < j + 1):
                                    db.session.delete(feature)
                                else:
                                    feature.name = feature["name"]
                                    feature.text = feature["text"]
                            for j in range(len(subrace.race_features), len(features)):
                                new_feature = SubraceFeature(
                                    subraceid = subrace.id,
                                    name = subrace["features"][j]["name"],
                                    text = subrace["features"][j]["text"]
                                )
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
                return(redirect(url_for("epchar.races")))
        return(redirect(url_for("epchar.createRace")))

def raceImporter(races, flavor, cruleset):
    if(cruleset.userid != current_user.id):
        flash("You cannot import races into rulesets that are not your own", "red")
        return(redirect(url_for("epchar.importRace")))
    for i, race in enumerate(races["race"]):
        name = f"{race['name']} ({race['source']})"
        if(len(name) > 127):
            flash(f"All race names must be fewer than 128 characters. Offender: {race['name']}", "red")
        
        sizedict = {
            "T": 0,
            "S": 1,
            "M": 2,
            "L": 3,
            "H": 4,
            "G": 5
        }
        if("size" in race.keys()):
            if(race["size"][0] in sizedict.keys()):
                size = sizedict[race["size"][0]]
                size_text = None
            else:
                size = None
                size_text = race["size"][0]
        else:
            size = 2
        
        walk = 30
        fly = swim = burrow = climb = 0

        if("speed" in race.keys()):
            if(type(race["speed"]) == int):
                walk = race["speed"]
            elif(type(race["speed"]) == dict):
                if("walk" in race["speed"].keys()):
                    walk = race["speed"]["walk"]
                if("fly" in race["speed"].keys()):
                    fly = race["speed"]["fly"]
                if("swim" in race["speed"].keys()):
                    swim = race["speed"]["swim"]
                if("burrow" in race["speed"].keys()):
                    burrow = race["speed"]["burrow"]
                if("climb" in race["speed"].keys()):
                    climb = race["speed"]["climb"]

        base_height = height_num = height_die = base_weight = weight_num = weight_die = None
        if("heightAndWeight" in race.keys() and race["heightAndWeight"]):
            if("baseHeight" in race["heightAndWeight"].keys()):
                base_height = race["heightAndWeight"]["baseHeight"]
                height_num = int(race["heightAndWeight"]["heightMod"].split("d")[0])
                height_die = int(race["heightAndWeight"]["heightMod"].split("d")[-1])
            if("baseWeight" in race["heightAndWeight"].keys()):
                base_weight = race["heightAndWeight"]["baseWeight"]
                if("weightMod" in race["heightAndWeight"].keys()):
                    weight_num = int(race["heightAndWeight"]["weightMod"].split("d")[0])
                    weight_die = int(race["heightAndWeight"]["weightMod"].split("d")[-1])
                else:
                    height_num = weight_num = 1

        asis = {}
        asi_text = ""
        if("ability" in race.keys()):
            if("choose" not in race["ability"][0].keys()):
                for score in AbilityScore.query.filter_by(rulesetid = cruleset.id).order_by(AbilityScore.order):
                    asis.update({score.abbr: 0})
                for score in race["ability"][0].keys():
                    asis[score] = race["ability"][0][score]
            else:
                for score in race["ability"][0].keys():
                    if(len(asi_text) > 0):
                        asi_text += ", "
                    if(score != "choose"):
                        asi_text += score.capitalize() + " "
                        if(race["ability"][0][score] > 0):
                            asi_text += "+"
                        asi_text += str(race["ability"][0][score])
                    else:
                        if("count" in race["ability"][0]["choose"].keys()):
                            asi_text += "+1 to any " + str(race["ability"][0]["choose"]["count"]) + " of your choice from:"
                            for thingy in race["ability"][0]["choose"]["from"]:
                                asi_text += f" {thingy},"
                        else:
                            asi_text += f"+{race['ability'][0]['choose']['amount']} to any one ability score of your choice"
        new_asis = []
        for asi in asis.values():
            new_asis.append(asi)
        
        if(asi_text != None and len(asi_text) > 255):
            asi_text = f"{asi_text[:252]}..."
            flash(f"{race['name']} Ability Score Improvement text had to be shortened to fit 256 character limit.", "orange")
        
        if(size_text != None and len(size_text) > 255):
            flash(f"Size text must be fewer than 256 characters. Offender: {race['name']}", "red")
            return(redirect(url_for("epchar.importRace")))

        flavortext = ""

        for flavors in flavor["raceFluff"]:
            if(flavors["name"] == race["name"] and flavors["source"] == race["source"] and "entries" in flavors.keys()):
                flavortext += parseEntries(flavors["entries"], 3, name)

        flavortext += f"## {race['name']} Traits\n\n---"

        new_race = Race(
            rulesetid = cruleset.id,
            name = name,
            flavor = flavortext,
            asis = new_asis,
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
            subrace_flavor = None
        )
        db.session.add(new_race)

        if("speed" in race.keys() and type(race["speed"]) != int and type(race["speed"]) != dict):
            new_race_feature = RaceFeature(
                race = new_race,
                name = "Speed",
                text = str(race["speed"])
            )
            db.session.add(new_race_feature)
        
        featurenames = []

        if("entries" in race.keys()):
            for feature in race["entries"]:
                if(type(feature) == dict and "name" in feature.keys()):
                    text = parseEntries(feature["entries"], 4, f"{name}")
                    if("<" in text):
                        flash(f"Open angle brackets (\"<\") are not allowed. Offender: {race['name']} feature '{feature['name']}'", "red")
                        return(redirect(url_for("epchar.importRace")))
                    elif("javascript" in text):
                        flash(f"Cross-site scripting attacks are not allowed. Offender: {race['name']} feature '{feature['name']}'", "red")
                        return(redirect(url_for("epchar.importRace")))
                    elif(len(feature["name"]) > 127):
                        flash(f"Race feature names must be fewer than 128 characters. Offender: {race['name']} feature '{feature['name']}", "red")
                        return(redirect(url_for("epchar.importRace")))
                    elif(len(text) > 16383):
                        flash(f"Race feature descriptions must be fewer than 16384 characters. Offender: {race['name']} feature '{feature['name']}'", "red")
                        return(redirect(url_for("epchar.importRace")))
                    new_race_feature = RaceFeature(
                        race = new_race,
                        name = feature["name"],
                        text = text
                    )
                    db.session.add(new_race_feature)
                    featurenames.append(feature["name"])
                else:
                    if(len(new_race.flavor) > 0):
                        new_race.flavor += "\n\n"
                    new_race.flavor += str(feature)

        if("languageProficiencies" in race.keys() and "Languages" not in featurenames and "Language" not in featurenames):
            langtext = ""
            for language in race["languageProficiencies"][0].keys():
                if(language != "other" and language != "anyStandard"):
                    if(len(langtext) > 0):
                        langtext += ", "
                    langtext += language.capitalize()
            if("other" in race["languageProficiencies"][0].keys()):
                if(len(langtext) > 0):
                    langtext += f", plus one extra language of your choice"
                else:
                    langtext += "one language of your choice"
            if("anyStandard" in race["languageProficiencies"][0].keys()):
                if(len(langtext) > 0):
                    langtext += f", and {['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][race['languageProficiencies'][0]['anyStandard'] - 1]} of your choice"
            langtext = "You can speak, read, and write " + langtext + "."
            new_race_feature = RaceFeature(
                race = new_race,
                name = "Languages",
                text = langtext
            )
            db.session.add(new_race_feature)
        
        for subrace in races["subrace"]:
            if("name" in subrace.keys() and subrace["raceName"] == race["name"]):
                name = subrace["name"]
                if(len(name) > 127):
                    flash(f"Subrace names must be fewer than 128 characters. Offender: {race['name']} subrace '{subrace['name']}'")
                    return(redirect(url_for("epchar.importRace")))
                new_subrace = Subrace(
                    race = new_race,
                    name = subrace["name"],
                    text = "",
                )
                db.session.add(new_subrace)
                if("entries" in subrace.keys()):
                    for feature in subrace["entries"]:
                        if(type(feature) == dict):
                            text = parseEntries(feature["entries"], 3, feature["name"])
                            if("<" in text):
                                flash(f"Open angle brackets (\"<\") are not allowed. Offender: {race['name']} subrace '{subrace['name']}' feature '{feature['name']}'", "red")
                                return(redirect(url_for("epchar.importRace")))
                            elif("javascript" in text):
                                flash(f"Cross-site scripting attacks are not allowed. Offender: {race['name']} subrace '{subrace['name']}' feature '{feature['name']}'", "red")
                                return(redirect(url_for("epchar.importRace")))
                            elif(len(feature["name"]) > 127):
                                flash(f"Subrace feature names must be fewer than 128 characters. Offender: {race['name']} subrace '{subrace['name']}' feature '{feature['name']}", "red")
                                return(redirect(url_for("epchar.importRace")))
                            elif(len(text) > 16383):
                                flash(f"Subrace feature descriptions must be fewer than 16384 characters. Offender: {race['name']} subrace '{subrace['name']}' feature '{feature['name']}'", "red")
                                return(redirect(url_for("epchar.importRace")))
                            new_subrace_feature = SubraceFeature(
                                subrace = new_subrace,
                                name = feature["name"],
                                text = text
                            )
                            db.session.add(new_subrace_feature)
                        else:
                            if(len(new_subrace.text) > 0):
                                new_subrace.text += "\n\n"
                            new_subrace.text += str(feature)
                for flavors in flavor["raceFluff"]:
                    if(race["name"] in flavors["name"] and subrace["name"] in flavors["name"]):
                        print(f"{race['name']}; {subrace['name']}")
                        if("entries" in flavors.keys()):
                            new_subrace.text += parseEntries(flavors["entries"], 3, flavors["name"])
                        if("_copy" in flavors.keys() and "_mod" in flavors["_copy"].keys()):
                            if(type(flavors["_copy"]["_mod"]["entries"]["items"]) == str):
                                new_subrace.text += flavors["_copy"]["_mod"]["entries"]["items"]
                            else:
                                new_subrace.text += parseEntries(flavors["_copy"]["_mod"]["entries"]["items"]["entries"], 3, subrace["name"])
    db.session.commit()
    flash("Races imported!", "green")
    return(redirect(url_for("epchar.races")))
    # except:
    #     flash("Improperly formatted JSON; could not import.", "red")
    #     return(redirect(url_for("epchar.importRaces")))

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
        languages = request.form.getlist("language")
        items = request.form.getlist("item")
        goldcontainer = request.form.get("goldcontainer")
        startinggold = request.form.get("gold")
        text = request.form.get("text")
        featurenames = request.form.getlist("featurename")
        featuretexts = request.form.getlist("featuretext")
        if(len("name") < 1 or not name):
            flash("You must specify a background name.", "red")
            return(redirect(url_for("epchar.createBackground")))
        elif(len("name") > 127):
            flash("Background name must be fewer than 128 characters.", "red")
            return(redirect(url_for("epchar.createBackground")))
        elif(len("text") > 16383):
            flash("Text must be fewer than 16384 characters.", "red")
            return(redirect(url_for("epchar.createBackground")))
        elif("<" in "text"):
            flash("Open angle brackets(\"<\") are not allowed.", "red")
            return(redirect(url_for("epchar.createBackground")))
        elif("javascript" in "text"):
            flash("Cross-site scripting attacks are not allowed.", "red")
            return(redirect(url_for("epchar.createBackground")))
        elif(len(goldcontainer) > 127):
            flash("Starting gold container name must be fewer than 128 characters.")
            return(redirect(url_for("epchar.createBackground")))
        else:
            for index, feature in enumerate(featurenames):
                if(len(feature) < 1):
                    flash("You must specify a feature name.", "red")
                    return(redirect(url_for("epchar.createBackground")))
                elif(len(feature) > 127):
                    flash("Feature name must be fewer than 128 characters.", "red")
                    return(redirect(url_for("epchar.createBackground")))
                elif(len(featuretexts[index]) > 16383):
                    flash("Text must be fewer than 16383 characters.", "red")
                    return(redirect(url_for("epchar.createBackground")))
                elif("<" in featuretexts[index]):
                    flash("Open angle brackets(\"<\") are not allowed.", "red")
                    return(redirect(url_for("epchar.createBackground")))
                elif("javascript" in featuretexts[index]):
                    flash("Cross-site scripting attacks are not allowed.", "red")
                    return(redirect(url_for("epchar.createBackground")))
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

    return(redirect(url_for("epchar.backgrounds")))

def backgroundImporter(backgrounds, flavor, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import backgrounds into rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.backgrounds")))
    try:
        for background in backgrounds["background"]:
            name = background["name"]
            skills = []
            if("skillProficiencies" in background.keys()):
                for skill in background["skillProficiencies"][0].keys():
                    skills.append(skill.casefold().capitalize())
            tools = []
            # something something tools
            lang_num = 0
            if("languageProficiencies" in background.keys()):
                if("anyStandard" in background["languageProficiencies"][0].keys()):
                    lang_num = background["languageProficiencies"][0]["anyStandard"]
            languages = []
            equipment = []
            gold_container = starting_gold = None
            if("startingEquipment" in background.keys()):
                for i, group in enumerate(background["startingEquipment"]):
                    if("_" in group.keys()):
                        for item in background["startingEquipment"][i]["_"]:
                            if(type(item) == str):
                                equipment.append(item)
                            elif("item" in item.keys()):
                                if("displayName" in item.keys()):
                                    equipment.append(item["displayName"])
                                elif("containsValue" in item.keys()):
                                    gold_container = item['item'].split('|')[0]
                                    starting_gold = item["containsValue"] / 100
                            elif("special" in item.keys()):
                                if("quantity" in item.keys()):
                                    equipment.append(f"{str(item['quantity'])} {item['special']}")
                                else:
                                    equipment.append(item["special"])
                    else:
                        thingy = "("
                        for key in group.keys():
                            if(len(thingy) > 1):
                                thingy += " or "
                            if(type(group[key][0]) == str):
                                thingy += group[key][0]
                            elif("displayName" in group[key][0].keys()):
                                thingy += group[key][0]["displayName"].split("|")[0]
                            elif("special" in group[key][0].keys()):
                                thingy += group[key][0]["special"]
                        thingy += ")"
                        equipment.append(thingy)
            text = ""
            if("hasFluff" in background.keys()):
                for fluff in flavor["backgroundFluff"]:
                    if(fluff["name"] == background["name"] and fluff["source"] == background["source"]):
                        if("_copy" in fluff.keys()):
                            flash("Variant background detected; variants not yet supported. Skipping...", "orange")
                        elif(type(fluff["entries"][0]) == dict):
                            for entry in fluff["entries"][0]["entries"][0]["entries"]:
                                text += f"{entry}\n\n"
                        else:
                            for entry in fluff["entries"]:
                                text += f"{entry}\n\n"
            new_background = Background(
                rulesetid = cruleset.id,
                name = name,
                skills = skills,
                tools = tools,
                lang_num = lang_num,
                languages = languages,
                equipment = equipment,
                text = text,
                gold_container = gold_container,
                starting_gold = starting_gold
            )
            db.session.add(new_background)

            if("entries" in background.keys()):
                for entry in background["entries"]:
                    if(entry["type"] == "entries"):
                        name = entry['name'].casefold().capitalize()
                        text = ""
                        for section in entry["entries"]:
                            if(type(section) == str):
                                text += f"{section}"
                            elif(type(section) == dict and "type" in section.keys() and section["type"] == "table"):
                                text += convertTable(section)
                            text += "\n\n"
                    elif(entry["type"] == "table"):
                        name = entry["caption"]
                        text += converTable(entry)
                    new_background_feature = BackgroundFeature(
                        background=new_background,
                        name = name,
                        text = text
                    )
                    db.session.add(new_background_feature)
        db.session.commit()
        flash("Backgrounds Imported!", "green")
        return(redirect(url_for('epchar.backgrounds')))
    except:
        flash("Improperly formatted JSON; unable to import.", "red")
        return(redirect(url_for("epchar.importBackgrounds")))

def makefeat(request, cruleset, tfeat, instruction):
    if(current_user.id != cruleset.userid):
        flash("You cannot create backgrounds in rulesets that are not your own.", "red")
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
        elif(len(name) > 127):
            flash("Feat name must be fewer than 128 characters.", "red")
        elif(len(prereq) > 255):
            flash("Feat Prerequisite must be fewer than 256 characters.", "red")
        elif(len(text) > 16383):
            flash("Feat description must be fewer than 16384 characters.", "red")
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
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
    return(redirect(url_for("epchar.feats")))

def featImporter(feats, cruleset):
    if(current_user.id != cruleset.userid):
        flash("You cannot import feats into rulesets that are not your own.", "red")
        return(redirect(url_for("epchar.feats")))
    try:
        for feat in feats["feat"]:
            name = feat["name"]
            prerequisites = ""
            if("prerequisite" in feat.keys()):
                for key in feat["prerequisite"][0].keys():
                    if(len(prerequisites) > 0):
                        prerequisites += ", "
                    prerequisites += f"{key.casefold().capitalize()}: {feat['prerequisite'][0][key]}"
            text = ""
            if("ability" in feat.keys()):
                # text += "***Ability Score Improvement.*** "
                for i, key in enumerate(feat["ability"][0].keys()):
                    scorename = AbilityScore.query.filter_by(rulesetid = cruleset.id, abbr = key).first()
                    if(not scorename):
                        scorename = "{Unknown Score}"
                    else:
                        scorename = scorename.name.casefold().capitalize()
                    if(len(text) > 1):
                        if(i == len(feat["ability"][0].keys) - 1):
                            text += f", and your {scorename} increases by {feat['ability'][0][key]}."
                        else:
                            f", and your {scorename} increases by {feat['ability'][0][key]}."
                    else:
                        f"Your {scorename} increases by {feat['ability'][0][key]}."
                text = "***Ability Score Improvement.*** " + text
            if("entries" in feat.keys()):
                for entry in feat["entries"]:
                    if(type(entry) == str):
                        text += f"{entry}\n\n"
                    elif(type(entry) == dict and "type" in entry.keys() and entry["type"] == "list"):
                        for item in entry["items"]:
                            text += f" - {item}\n"
                        text += "\n"
                    elif(type(entry) == dict and "type" in entry.keys() and entry["type"] == "table"):
                        text += convertTable(entry)
                    elif(type(entry) == dict and "type" in entry.keys() and entry["type"] == "section"):
                        for section in entry["entries"][0]["entries"]:
                            text += f"## {section['name']}\n\n---\n\n"
                            for paragraph in section["entries"]:
                                text += f"{paragraph}\n\n"
            new_feat = Feat(
                rulesetid = cruleset.id,
                name = name,
                prerequisite = prerequisites,
                text = text
            )
            db.session.add(new_feat)
        db.session.commit()
        flash("Feats imported!", "green")
        return(redirect(url_for("epchar.feats")))

    except:
        flash("Improperly formatted JSON; unable to import.", "red")
        return(redirect(url_for("epchar.importFeats")))

def makeclass(request, cruleset, tclass, instruction):
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
        bad = False
        name = request.form.get("name")
        text = request.form.get("text")
        hitdie = request.form.get("hitdie")
        proficiencies = request.form.getlist("proficiency")
        skills = request.form.getlist("skill")
        saves = request.form.getlist("save")
        for i in range(len(saves)):
            if(saves[i] == "true"):
                saves[i] = True
            else:
                saves[i] = False
        equipment = request.form.get("equipment")
        gold_nums = request.form.get("gold_nums")
        try:
            gold_nums = int(gold_nums)
        except:
            flash("Number of dice rolled for starting gold must be a number.", "red")
            bad = True
        gold_dice = request.form.get("gold_dice")
        gold_mult = request.form.get("gold_mult")
        try:
            gold_mult = int(gold_mult)
        except:
            flash("Starting gold multiplier must be a number.", "red")
            bad = True
        multiclass_prereq = request.form.get("prereq")
        multiclass_profic = request.form.getlist("multiprofic")
        subclass_name = request.form.get("subclassname")
        subclass_level = int(request.form.get("subclasslevel"))
        levels = request.form.get("levels")
        try:
            levels = int(levels)
        except:
            flash("Max level must be a number.", "red")
            bad = True
        if(len(name) < 1):
            flash("You must specify a class name.", "red")
            bad = True
        elif(len(name) > 127):
            flash("Class name must be fewer than 128 characters.", "red")
            bad = True
        elif(len(text) > 16383):
            flash("Class description must be fewer than 16383 characters.", "red")
            bad = True
        elif("<" in text):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
            bad = True
        elif("javascript" in text):
            flash("Cross-site scripting attacks are not allowed.", "red")
            bad = True
        elif(len(equipment) > 1023):
            flash("Class equipment must be fewer than 1024 characters.", "red")
            bad = True
        elif(len(multiclass_prereq) > 1023):
            flash("Multiclassing prerequisites must be fewer than 1024 characters.", "red")
            bad = True
        elif("<" in multiclass_prereq):
            flash("Open angle brackets (\"<\") are not allowed.", "red")
            bad = True
        elif("javascript" in multiclass_prereq):
            flash("Cross-site scripting attacks are not allowed.", "red")
            bad = True
        elif(len(subclass_name) > 127):
            flash("Subclass title must be fewer than 128 characters.", "red")
            bad = True
        else:
            for i, column in enumerate(request.form.getlist("columnname")):
                if(bad):
                    break
                if(len(column) < 1):
                    bad = True
                    flash("Each custom column must have a name.", "red")
                elif(len(column) > 127):
                    bad = True
                    flash("Custom column names must be fewer than 128 characters.", "red")
                for value in request.form.getlist(f"column{i}value"):
                    if(bad):
                        break
                    elif(len(value) > 127):
                        bad = True
                        flash("Custom column values must be fewer than 128 characters.", "red")
            for i, feature in enumerate(request.form.getlist("class_feature_name")):
                if(bad):
                    break
                try:
                    testint = int(request.form.getlist("level")[i])
                except:
                    bad = True
                    flash("Feature levels must be numbers.", "red")
                if(len(feature) < 1):
                    bad = True
                    flash("You must specify a name for each class feature", "red")
                elif(len(feature) > 127):
                    bad = True
                    flash("Class feature names must be fewer than 128 characters", "red")
                elif(len(request.form.getlist("class_feature_text")[i]) > 16383):
                    bad = True
                    flash("Class feature text must be fewer than 128 characters", "red")
                elif("<" in request.form.getlist("class_feature_text")[i]):
                    bad = True
                    flash("Open angle brackets (\"<\") are not allowed.", "red")
                elif("javascript" in request.form.getlist("class_feature_text")[i]):
                    bad = True
                    flash("Cross-site scripting attacks are not allowed.", "red")
            for i, subclass in enumerate(request.form.getlist("subclass_name")):
                if(bad):
                    break
                if(len(subclass) < 1):
                    bad = True
                    flash("You must specify a name for each subclass.", "red")
                elif(len(subclass) > 127):
                    bad = True
                    flash("Subclass names must be fewer than 128 characters.", "red")
                elif(len(request.form.getlist("subclass_text")[i]) > 16383):
                    bad = True
                    flash("Subclass descriptions must be fewer than 16383 characters.", "red")
                elif("<" in request.form.getlist("subclass_text")[i]):
                    bad = True
                    flash("Open angle brackets (\"<\") are not allowed.", "red")
                elif("javascript" in request.form.getlist("subclass_text")[i]):
                    bad = True
                    flash("Cross-site scripting attacks are not allowed.", "red")
                for j, feature in enumerate(request.form.getlist(f"subclass_{i}_feature_name")):
                    if(bad):
                        break
                    try:
                        testint = int(request.form.getlist(f"subclass_{i}_feature_level")[j])
                    except:
                        bad = True
                        flash("Subclass feature levels must be numbers.", "red")
                    if(len(feature) < 1):
                        bad = True
                        flash("You must specify a name for each subclass feature.", "red")
                    elif(len(feature) > 127):
                        bad = True
                        flash("Subclass feature names must be fewer than 128 characters.", "red")
                    elif(len(request.form.getlist(f"subclass_{i}_feature_text")[j]) > 16383):
                        bad = True
                        flash("Subclass feature descriptions must be fewer than 16383 characters.", "red")
                    elif("<" in request.form.getlist(f"subclass_{i}_feature_text")[j]):
                        bad = True
                        flash("Open angle brackets (\"<\") are not allowed.", "red")
                    elif("javascript" in request.form.getlist(f"subclass_{i}_feature_text")[j]):
                        bad = True
                        flash("Cross-site scripting attacks are not allowed.", "red")
                for j, column in enumerate(request.form.getlist(f"subclass{i}columnname")):
                    if(bad):
                        break
                    if(len(column) < 1):
                        bad = True
                        flash("You must specify a name for each subclass' custom columns.", "red")
                    elif(len(column) > 127):
                        bad = True
                        flash("Each subclass' custom column names must be fewer than 128 characters.", "red")
                    for value in request.form.getlist(f"subclass{i}column{j}value"):
                        if(len(value) > 127):
                            bad = True
                            flash("Each subclass' custom column values must be fewer than 128 characters.", "red")

            if(not bad):
                if(instruction == "create"):
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
                        skills = skills
                    )
                    db.session.add(new_class)
                    db.session.commit()
                    classid = Playerclass.query.filter_by(name=name, text=text, rulesetid=cruleset.id).first().id

                    for i, column in enumerate(request.form.getlist("columnname")):
                        new_column = ClassColumn(
                            classid = classid,
                            name = column,
                            data = request.form.getlist(f"column{i}value")
                        )
                        db.session.add(new_column)

                    for i, feature in enumerate(request.form.getlist("class_feature_name")):
                        new_feature = ClassFeature(
                            classid = classid,
                            level_obtained = request.form.getlist("level")[i],
                            name = feature,
                            text = request.form.getlist("class_feature_text")[i]
                        )
                        db.session.add(new_feature)
                    
                    for i, sublcass in enumerate(request.form.getlist("subclass_name")):
                        new_subclass = Subclass(
                            classid = classid,
                            name = subclass,
                            text = request.form.getlist("subclass_text")[i],
                            caster_type = request.form.getlist("castertype")[i],
                        )
                        db.session.add(new_subclass)
                        db.session.commit()
                        new_subclass = Subclass.query.filter_by(classid = classid, name = subclass).first()

                        for j, feature in enumerate(request.form.getlist(f"subclass_{i}_feature_name")):
                            new_subclass_feature = SubclassFeature(
                                subclassid = new_subclass.id,
                                level_obtained = request.form.getlist(f"subclass_{i}_feature_level")[j],
                                name = feature,
                                text = request.form.getlist(f"subclass_{i}_feature_text")[j]
                            )
                            db.session.add(new_subclass_feature)
                        for j, column in enumerate(request.form.getlist(f"subclass{i}columnname")):
                            new_subclass_column = SubclassColumn(
                                    subclassid = new_subclass.id,
                                    name = column,
                                    data = request.form.getlist(f"subclass{i}column{j}value")
                                )
                            db.session.add(new_subclass_column)
                        db.session.commit()
                    flash("Class Created!", "green")
                else:
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
                    for i, column in enumerate(tclass.columns):
                        if(len(request.form.getlist("columnname")) < i + 1):
                            db.session.delete(column)
                        else:
                            column.name = request.form.getlist("columnname")[i]
                            column.data = request.form.getlist(f"column{i}value")
                    for i in range(len(tclass.columns), len(request.form.getlist("columnname"))):
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

                            for j, column in enumerate(subclass.columns):
                                if(len(request.form.getlist(f"subclass{i}columnname")) < j + 1):
                                    db.session.delete(column)
                                else:
                                    column.name = request.form.getlist(f"subclass{i}columnname")[j]
                                    column.data = request.form.getlist(f"subclass{i}column{j}value")
                            for j in range(len(subclass.columns), len(request.form.getlist(f"subclass{i}columnname"))):
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
            elif(instruction == "edit"):
                return(redirect(url_for("epchar.editClass", tclass=tclass.name.replace(" ", "-"))))
            else:
                return(redirect(url_for("epchar.createClass")))
    return(redirect(url_for("epchar.classes")))
