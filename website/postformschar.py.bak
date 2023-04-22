from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .models import Ruleset, Race, RaceFeature, Subrace, SubraceFeature, Background, BackgroundFeature, Feat, Item, Playerclass, AbilityScore, ClassColumn, SubclassColumn, ClassFeature, Playerclass, Subclass, SubclassFeature

def abilityScore(request, cruleset, ability_score, instruction):
    name = request.form.get("name")
    abbr = request.form.get("abbr")
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
                else:
                    race.namme = name
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
    return(False)

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
        lang_num = reuqest.form.get("lang_num")
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
        elif("-" in "name"):
            flash("Dashes (\"-\") are not allowed in the background name.", "red")
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
                background.equipment = equipment
                background.text = text
                featurenum = 0
                for index, feature in enumerate(background.features):
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
        print(saves)
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
                    for column in tclass.columns:
                        db.session.delete(column)
                    for i, column in request.form.getlist("columnname"):
                        new_class_column = ClassColumn(
                            classid = tclass.id,
                            name = column,
                            data = request.form.getlist(f"column{i}value")
                        )
                        db.session.add(new_class_column)

                    for feature in tclass.class_features:
                        db.session.delete(feature)
                    for i, feature in request.form.getlist("class_feature_name"):
                        new_class_feature = ClassFeature(
                            classid = tclass.id,
                            name = feature,
                            level_obtained = request.form.getlist("level")[i],
                            text = request.form.getlist("class_feature_text")[i]
                        )
                        db.session.add(new_class_feature)

                    for subclass in tclass.subclasses:
                        for column in subclass.columns:
                            db.session.delete(column)
                        for feature in subclass.subclass_features:
                            db.session.delete(feature)
                    for i, subclass in enumerate(request.form.getlist("subclass_name")):
                        new_subclass = Subclass(
                            classid = tclass.id,
                            name = subclass,
                            text = request.form.getlist("subclass_text")[i],
                            caster_type = request.form.getlist("castertype")[i],
                        )
                        db.session.add(new_subclass)
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
                                level_obtained = request.form.getlist(f"subclass_{i}_feature_level"),
                                text = request.form.getlist(f"subclass_{i}_feature_text")
                            )
                            db.session.add(new_subclass_feature)
                    db.session.commit()
                    flash("Changes saved!")
            elif(instruction == "edit"):
                return(redirect(url_for("epchar.editClass", tclass=tclass.name.replace(" ", "-"))))
            else:
                return(redirect(url_for("epchar.createClass")))
    return(redirect(url_for("epchar.classes")))