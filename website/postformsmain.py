from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user
from . import db
from .jsonparsers import *
from .models import *

def makeRuleset(request, ruleset, instruction):
    if(instruction == "duplicate"):
        if(current_user.id != ruleset.userid and ruleset.visibility < 1 and not user in ruleset.editors and not user in ruleset.viewers):
            flash("You must have permission to view a ruleset to duplicate it.", "red")
        elif(request.form.get("same_viewers")):
            viewers = ruleset.viewers
        else:
            viewers = []
        if(request.form.get("same_editors")):
            editors = ruleset.editors
        else:
            editors = []
        visibility = int(request.form.get("visiblity"))
        if(len(request.form.get("name")) < 1):
            flash("You must specify a ruleset name", "red")
        elif(len(request.form.get("name")) > 127):
            flash("Ruleset name must be fewer than 128 characters.", "red")
        elif(visibility > 0 and len(request.form.get(identifier)) < 1):
            flash("Non-private rulesets must have an identifier.", "red")
        elif(not identifier.isalnum()):
            flash("Only alphanumeric characters (a-z, A-Z, 0-9) are allowed in ruleset identifiers.", "red")
        elif(len(request.form.get("identifier")) > 32):
            flash("Ruleset identifier must be fewer than 32 characters.", "red")
        elif(len(request.form.get("text")) > 16383):
            flash("Ruleset description must be fewer than 16383 characters.", "red")
        else:
            new_ruleset = Ruleset(
                identifier = f"{ruleset.identifier}-dupe",
                is_admin = current_user.is_admin,
                userid = current_user.id,
                viewers = viewers,
                editors = editors,
                visibility = visibility,
                name = request.form.get("name"),
                description = request.form.get("text")
            )
            db.session.add(new_ruleset)
            for category in ruleset.categories:
                new_category = Category(
                    ruleset = new_ruleset,
                    name = category.name,
                    pinned = category.pinned,
                )
                db.session.add(new_category)
                for rule in category.rules:
                    new_rule = Rule(
                        category = new_category,
                        pinned = rule.pinned,
                        name = rule.name,
                        text = rule.text
                    )
                    db.session.add(new_rule)
            for language in ruleset.languages:
                new_language = Language(
                    ruleset = new_ruleset,
                    name = language.name,
                    text = language.text
                )
                db.session.dadd(new_language)
            for recipe in ruleset.recipes:
                new_recipe = Recipe(
                    ruleset = new_ruleset,
                    name = recipe.name,
                    text = ruleset.text,
                    images = ruleset.images
                )
                db.session.add(new_recipe)
            for tag in ruleset.item_tags:
                new_tag = ItemTag(
                    ruleset = new_ruleset,
                    name = tag.name,
                    text = tag.text
                )
                db.session.add(new_tag)
            for item_property in ruleset.item_properties:
                new_property = Property(
                    ruleset = new_ruleset,
                    name = item_property.name,
                    text = item_property.text
                )
                db.session.add(new_property)
            for item in ruleset.items:
                new_item = Item(
                    ruleset = new_ruleset,
                    name = item.name,
                    is_magical = item.is_magical,
                    rarity = item.rarity,
                    tier = item.tier,
                    attunement = item.attunement,
                    tags = item.tags,
                    proficiency = item.proficiency,
                    cost = item.cost,
                    weight = item.weight,
                    text = item.text,
                    images = item.images,
                    is_armor = item.is_armor,
                    stealth = item.stealth,
                    strength = item.strength,
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
            for condition in ruleset.conditions:
                new_condition = Condition(
                    ruleset = new_ruleset,
                    name = condition.name,
                    text = condition.text
                )
                db.session.add(new_condition)
            for disease in ruleset.diseases:
                new_disease = Disease(
                    ruleset = new_ruleset,
                    name = disease.name,
                    text = disease.text
                )
                db.session.add(new_disease)
            for status in ruleset.statuses:
                new_status = Status(
                    ruleset = new_ruleset,
                    name = status.name,
                    text = status.name
                )
                db.session.add(new_status)
            for action in ruleset.actions:
                new_action = Action(
                    ruleset = new_ruleset,
                    name = action.name,
                    time = action.time,
                    text = action.text
                )
                db.session.add(new_action)
            for race in ruleset.races:
                new_race = Race(
                    ruleset = new_ruleset,
                    name = race.name,
                    text = race.text,
                    flavor = race.flavor,
                    images = race.images,
                    asis = race.asis,
                    asi_text = race.asi_text,
                    size = race.size,
                    size_text = race.size_text,
                    walk = race.walk,
                    climb = race.climb,
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
                for feature in race.race_features:
                    new_race_feature = RaceFeature(
                        race = new_race,
                        name = feature.name,
                        text = feature.text
                    )
                    db.session.add(new_race_feature)
                for subrace in race.subraces:
                    new_subrace = Subrace(
                        race = new_race,
                        name = subrace.name,
                        text = subrace.text,
                        images = subrace.images
                    )
                    db.session.add(new_subrace)
                    for feature in subrace.subrace_features:
                        new_subrace_feature = SubraceFeature(
                            subrace=new_subrace,
                            name = subrace.name,
                            text = subrace.text
                        )
                        db.session.add(new_subrace_feature)
            for feat in ruleset.feats:
                new_feat = Feat(
                    ruleset = new_ruleset,
                    name = feat.name,
                    prerequisite = feat.prerequisite,
                    text = feat.text
                )
                db.session.add(new_feat)
            for score in ruleset.ability_scores:
                new_ability_score = AbilityScore(
                    ruleset = new_ruleset,
                    name = score.name,
                    order = score.order,
                    abbr = score.abbr,
                    text = score.text
                )
                db.session.add(new_ability_score)
            for spell in ruleset.spells:
                new_spell = Spell(
                    ruleset = new_ruleset,
                    name = spell.name,
                    school = spell.school,
                    level = spell.level,
                    casting_time = spell.casting_time,
                    spell_range = spell.spell_range,
                    verbal = spell.verbal,
                    somatic = spell.somatic,
                    material = spell.material,
                    material_specific = spell.material_specific,
                    consumes_material = spell.consumes_material,
                    concentration = spell.concentration,
                    duration = spell.duration,
                    text = spell.text
                )
                db.session.add(new_spell)
            for background in ruleset.backgrounds:
                new_background = Background(
                    ruleset = new_ruleset,
                    name = background.name,
                    skills = background.skills,
                    tools = background.tools,
                    lang_num = background.lang_num,
                    languages = background.languages,
                    equipment = background.equipment,
                    gold_container = background.gold_container,
                    starting_gold = starting_gold,
                    text = background.text,
                    images = background.images,
                )
                db.session.add(new_background)
                for feature in background.background_features:
                    new_background_feature = BackgroundFeature(
                        background = new_background,
                        name = feature.name,
                        text = feature.text
                    )
                    db.session.add(new_background_feature)
            for player_class in ruleset.classes:
                new_class = Playerclass(
                    ruleset = new_ruleset,
                    name = player_class.name,
                    hitdie = player_class.hitdie,
                    proficiencies = player_class.proficiencies,
                    saves = player_class.proficiencies,
                    skills = player_class.skills,
                    equipment = player_class.equipment,
                    gold_nums = player_class.gold_nums,
                    gold_dice = player_class.gold_dice,
                    gold_mult = player_class.gold_mult,
                    multiclass_prereq = player_class.multiclass_prereq,
                    multiclass_profic = player_class.multiclass_profic,
                    subclass_name = player_class.subclass_name,
                    subclass_level = player_class.subclass_level,
                    levels = player_class.levels,
                    text = player_class.text,
                    images = player_class.images,
                )
                db.session.add(new_class)
                for feature in player_class.class_features:
                    new_class_feature = ClassFeature(
                        playerclass = new_class,
                        level_obtained = feature.level_obtained,
                        name = feature.name,
                        text = feature.text
                    )
                    db.session.add(new_class_feature)
                for subclass in player_class.subclasses:
                    new_subclass = Subclass(
                        playerclass = new_class,
                        name = subclass.name,
                        text = subclass.text,
                        images = subclass.images,
                        caster_type = subclass.caster_type,
                    )
                    db.session.add(new_subclass)
                    for feature in subclass.subclass_features:
                        new_subclass_feature = SubclassFeature(
                            subclass = new_subclass,
                            name = feature.name,
                            level_obtained = feature.level_obtained,
                            text = feature.text
                        )
                        db.session.add(new_subclass_feature)
                    for column in subclass.subclass_columns:
                        new_subclass_column = SubclassColumn(
                            subclass = new_subclass,
                            name = column.name,
                            data = column.data
                        )
                        db.session.add(new_subclass_column)
                for column in player_class.columns:
                    new_class_column = ClassColumn(
                        playerclass = new_class,
                        name = column.name,
                        data = column.data
                    )
                    db.session.add(new_class_column)
            for currency in ruleset.currencies:
                new_currency = Currency(
                    ruleset = new_ruleset,
                    name = currency.name,
                    value = currency.value,
                    text = currency.text
                )
            for character in ruleset.characters:
                new_character = Character(
                    ruleset = new_ruleset,
                    is_npc = character.is_npc,
                    userid = current_user.id,
                    rulesetid = new_ruleset.id,
                    race = character.race,
                    walk = character.walk,
                    climb = character.climb,
                    fly = character.fly,
                    hover = character.hover,
                    swim = character.swim,
                    burrow = character.burrow,
                    alignment = character.alignment,
                    experience = character.experience,
                    background = character.background,
                    personality = character.personality,
                    ideals = character.ideals,
                    bonds = character.bonds,
                    flaws = character.flaws,
                    backstory = character.backstory,
                    notes = character.notes,
                    images = character.images,
                    classes = character.classes,
                    level = character.level,
                    proficiency_bonus = character.proficiency_bonus,
                    saves = character.saves,
                    skills = character.skills,
                    proficiencies = character.proficiencies,
                    armor_class = character.armor_class,
                    initiative = character.initiative,
                    current_hp = character.current_hp,
                    max_hp = character.max_hp,
                    temp_hp = character.temp_hp,
                    current_hit_dice = character.current_hit_dice,
                    max_hit_dice = character.max_hit_dice,
                    death_saves = character.death_saves,
                    currency = character.currency,
                )
                db.session.add(new_character)
                for feature in character.features:
                    new_character_feature = CharacterFeature(
                        character = new_character,
                        comes_from = feature.comes_from,
                        reference = feature.reference,
                        name = feature.name,
                        text = feature.text
                    )
                    db.session.add(new_character_feature)
                for attack in character.attacks:
                    new_character_attack = CharacterAttack(
                        character = new_character,
                        name = attack.name,
                        ability_score = attack.ability_score,
                        misc_bonus = attack.misc_bonus,
                        proficient = attack.proficient,
                        attack_range = attack.attack_range,
                        damage_nums = attack.damage_nums,
                        damage_dice = attack.damage_dice,
                        crit_nums = attack.crit_nums,
                        crit_dice = attack.crit_dice,
                        add_ability = attack.add_ability,
                        damage_type = attack.damage_type,
                        note = attack.note
                    )
                    db.session.add(new_character_attack)
                for item in character.items:
                    new_character_tem = CharacterItem(
                        character = new_character,
                        reference = item.reference,
                        quantity = item.quantity,
                        name = item.name,
                        text = item.text
                    )
                    db.session.add(new_character_item)
            for monster in ruleset.monsters:
                new_monster = Monster(
                    ruleset = new_ruleset,
                    name = monster.name,
                    shorened_name = monster.shortened_name,
                    shortened_plural = monster.shortened_plural,
                    info = monster.text,
                    images = monster.images,
                    size = monster.size,
                    size_text = monster.size_text,
                    monster_type = monster.monster_type,
                    monster_subtype = monster.monster_subtype,
                    type_text = monster.type_text,
                    alignment = monster.alignment,
                    armor_tem = monster.armor_item,
                    base_ac = monster.base_ac,
                    custom_armor = monster.custom_armor,
                    has_shield = monster.has_shield,
                    die_num = monster.die_num,
                    hit_die = monster.hit_die,
                    avg_hp = monster.avg_hp,
                    walk = monster.walk,
                    climb = monster.climb,
                    fly = monster.fly,
                    hover = monster.hover,
                    swim = monster.swim,
                    burrow = monster.burrow,
                    ability_scores = monster.ability_scores,
                    saves = monster.saves,
                    versatile = monster.versatile,
                    skills = monster.skills,
                    expertise = monster.experties,
                    damage_immunities = monster.damage_immunities,
                    damage_resistances = monster.damage_resistances,
                    damage_vulnerabilities = monster.damage_vulnerabilities,
                    condition_immunities = monster.condition_immunities,
                    senses = monster.senses,
                    languages = monster.languages,
                    challenge_rating = monster.challenge_rating,
                    is_legendary = monster.is_legendary,
                    is_mythic = monster.is_mythic,
                    is_villain = monster.is_villain,
                    has_lair = monster.has_lair,
                    reactions_text = monster.reactions_text,
                    bonus_actions_text = monster.bonus_actions_text,
                    actions_text = monster.actions_text,
                    legendary_actions_text = monster.legendary_actions_text,
                    mythic_actions_text = monster.mythic_actions_text,
                    villain_actions_text = monster.villain_actions_text,
                    lair_actions_text = monster.lair_actions_text,
                    custom_actions_text = monster.custom_actions_text
                )
                db.session.add(new_monster)
                for feature in monster.features:
                    new_feature = MonsterFeature(
                        monster = new_monster,
                        name = feature.name,
                        text = feature.text
                    )
                    db.session.add(new_feature)
                for action in monster.actions:
                    new_action = MonsterAction(
                        monster = new_monster,
                        action_type = action.action_type,
                        name = action.name,
                        text = action.text
                    )
                    db.session.add(new_action)
            for monster_type in ruleset.monster_types:
                new_monster_type = MonsterType(
                    ruleset = new_ruleset,
                    name = monster_type.name,
                    text = monster_type.text,
                )
                db.session.add(new_monster_type)
                for subtype in monster_type:
                    new_subtype = MonsterSubtype(
                        monstertype = new_monster_type,
                        name = subtype.name,
                        text = subtype.text
                    )
                    db.session.add(new_subtype)
            for damage_type in ruleset.damage_types:
                new_damage_type = DamageType(
                    ruleset = new_ruleset,
                    name = damage_type.name,
                    text = damage_type.text
                )
                db.session.add(new_damage_type)
            db.session.commit()
            flash("Ruleset created!", "green")
            return(redirect(url_for("epmain.home", ruleset=new_ruleset.identifier)))
        return(redirect(url_for("epmain.createRuleset", ruleset=ruleset.identifier)))
    else:
        name = request.form.get("name")
        text = request.form.get("text")
        identifier = request.form.get("identifier")
        viewers = request.form.getlist("viewer")
        editors = request.form.getlist("editor")
        visibility = int(request.form.get("visibility"))
        if(len(name) < 1):
            flash("You must specify a ruleset name.", "red")
        elif(len(name) > 127):
            flash("Ruleset name must be fewer than 128 characters.", "red")
        elif(visibility > 0 and len(identifier) < 1):
            flash("Non-private rulesets must have identifiers.", "red")
        elif(not identifier.isalnum()):
            flash("Only alphanumeric characters (a-z, A-Z, 0-9) are allowed in ruleset identifiers.", "red")
        elif(len(identifier) > 32):
            flash("Ruleset identifiers must be fewer than 32 characters", "red")
        elif(len(text) > 16383):
            flash("Ruleset description must be fewer than 16383 characters.", "red")
        elif(instruction == "create"):
            new_ruleset = Ruleset(
                identifier = identifier,
                is_admin = current_user.is_admin,
                userid = current_user.id,
                viewers = viewers,
                editors = editors,
                visibility = visibility,
                name = name,
                description = text
            )
            db.session.add(new_ruleset)
            db.session.commit()
            flash("Ruleset created!", "green")
            return(redirect(url_for("epmain.home", ruleset=new_ruleset.identifier)))
        else:
            if(current_user.id != ruleset.userid and not user in ruleset.editors):
                flash("You do not have permission to edit this ruleset.", "red")
            ruleset.identifier = identifier
            ruleset.viewers = viewers
            ruleset.editors = editors
            ruleset.visibility = visibility
            ruleset.name = name
            ruleset.description = text
            db.session.commit()
            flash("Changes saved!", "green")
            return(redirect(url_for("epmain.home", ruleset=ruleset.identifier)))
    return(redirect(url_for("epmain.home", ruleset=Ruleset.query.filter_by(id=current_user.current_ruleset).first().identifier)))   