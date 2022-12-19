from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    foreign_ruleset = db.Column(db.String(1023))
    current_ruleset = db.Column(db.Integer)
    rulesets = db.relationship("Ruleset")
    characters = db.relationship("Character")

class Ruleset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_shareable = db.Column(db.Boolean)
    name = db.Column(db.String(127))
    categories = db.relationship("Category")
    languages = db.relationship("Language")
    item_tags = db.relationship("ItemTag")
    item_properties = db.relationship("Property")
    items = db.relationship("Item")
    conditions = db.relationship("Condition")
    skills = db.relationship("Skill")
    actions = db.relationship("Action")
    races = db.relationship("Race")
    feats = db.relationship("Feat")
    spells = db.relationship("Spell")
    backgrounds = db.relationship("Background")
    classes = db.relationship("Playerclass")
    monsters = db.relationship("Monster")
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    pinned = db.Column(db.Boolean)
    rules = db.relationship("Rule")

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_categoryid = db.Column(db.Integer, db.ForeignKey("category.id"))
    pinned = db.Column(db.Boolean)
    name = db.Column(db.String(511))
    text = db.Column(db.String(16383))

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(255))
    speakers = db.Column(db.String(255))
    script = db.Column(db.String(127))

class ItemTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    is_magical = db.Column(db.Boolean)
    rarity = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    attunement = db.Column(db.Boolean)
    tags = db.Column(db.String(127))
    proficiency = db.Column(db.Boolean)
    cost = db.Column(db.String(31))
    weight = db.Column(db.Integer)
    text = db.Column(db.String(16383))
    is_armor = db.Column(db.Boolean)
    armor_class = db.Column(db.Integer)
    add_dex = db.Column(db.Boolean)
    max_dex = db.Column(db.Integer)
    is_weapon = db.Column(db.Boolean)
    die_num = db.Column(db.Integer)
    damage_die = db.Column(db.Integer)
    damage_type = db.Column(db.String(15))
    weapon_properties = db.Column(db.String(255))

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(63))
    ability_score = db.Column(db.String(3))
    description = db.Column(db.String(16383))

class Action(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    time = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Race(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    flavor = db.Column(db.String(16383))
    strasi = db.Column(db.Integer)
    dexasi = db.Column(db.Integer)
    conasi = db.Column(db.Integer)
    intasi = db.Column(db.Integer)
    wisasi = db.Column(db.Integer)
    chaasi = db.Column(db.Integer)
    asi_text = db.Column(db.String(255))
    size = db.Column(db.Integer)
    size_text = db.Column(db.String(255))
    walk = db.Column(db.Integer)
    fly = db.Column(db.Integer)
    swim = db.Column(db.Integer)
    burrow = db.Column(db.Integer)
    base_height = db.Column(db.Integer)
    base_weight = db.Column(db.Integer)
    height_num = db.Column(db.Integer)
    height_die = db.Column(db.Integer)
    weight_num = db.Column(db.Integer)
    weight_die = db.Column(db.Integer)
    subrace_flavor = db.Column(db.String(16383))
    race_features = db.relationship("RaceFeature")
    subraces = db.relationship("Subrace")

class RaceFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("race.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Subrace(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("race.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    subrace_features = db.relationship("SubraceFeature")

class SubraceFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("subrace.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Feat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    type = db.Column(db.String(31))
    name = db.Column(db.String(127))
    prerequisite = db.Column(db.String(255))
    strasi = db.Column(db.Integer)
    dexasi = db.Column(db.Integer)
    conasi = db.Column(db.Integer)
    intasi = db.Column(db.Integer)
    wisasi = db.Column(db.Integer)
    chaasi = db.Column(db.Integer)
    text = db.Column(db.String(16383))

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    school = db.Column(db.String(31))
    level = db.Column(db.Integer)
    casting_time = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    verbal = db.Column(db.Boolean)
    somatic = db.Column(db.Boolean)
    material = db.Column(db.Boolean)
    consumes_material = db.Column(db.Boolean)
    duration = db.Column(db.String)
    text = db.Column(db.String(16383))

class Background(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    skills = db.Column(db.String(255))
    tools = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    equipment = db.Column(db.String(511))
    text = db.Column(db.String(16383))
    background_features = db.relationship("BackgroundFeature")

class BackgroundFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    backgroundid = db.Column(db.Integer, db.ForeignKey("background.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

# not UpperCamelCase because SQLAlchemy gets mad when it is. idk why
class Playerclass(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    caster_type = db.Column(db.Integer)
    multiclass_prereq = db.Column(db.String(127))
    multiclass_skills = db.Column(db.String(255))
    class_features = db.relationship("ClassFeature")
    subclasses = db.relationship("Subclass")

class ClassFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    level_obtained = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Subclass(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    caster_type = db.Column(db.Integer)
    subclass_features = db.relationship("SubclassFeature")

class SubclassFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subclassid = db.Column(db.Integer, db.ForeignKey("subclass.id"))
    level_obtained = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Monster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    size = db.Column(db.Integer)
    type = db.Column(db.String(127))
    alignment = db.Column(db.String(31))
    armor_class = db.Column(db.Integer)
    ac_note = db.Column(db.String(31))
    die_num = db.Column(db.Integer)
    walk_speed = db.Column(db.Integer)
    fly_speed = db.Column(db.Integer)
    swim_speed = db.Column(db.Integer)
    burrow_speed = db.Column(db.Integer)
    strstat = db.Column(db.Integer)
    dexstat = db.Column(db.Integer)
    constat = db.Column(db.Integer)
    intstat = db.Column(db.Integer)
    wisstat = db.Column(db.Integer)
    chastat = db.Column(db.Integer)
    skills = db.Column(db.String(127))
    immunities = db.Column(db.String(255))
    resistances = db.Column(db.String(255))
    condition_immunities = db.Column(db.String(255))
    senses = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    challenge_rating = db.Column(db.Integer)
    abilities = db.relationship("MonsterAbility")

class MonsterAbility(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    monsterid = db.Column(db.Integer, db.ForeignKey("monster.id"))
    # ability,action,bonusaction,reaction,villainaction,legendaryaction,mythicaction,lairaction
    type = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(2047))

class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    is_npc = db.Column(db.Boolean)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    size = db.Column(db.Integer)
    type = db.Column(db.String(127))
    alignment = db.Column(db.String(31))
    armor_class = db.Column(db.Integer)
    ac_note = db.Column(db.String(31))
    die_num = db.Column(db.Integer)
    walks_peed = db.Column(db.Integer)
    fly_speed = db.Column(db.Integer)
    swim_speed = db.Column(db.Integer)
    burrow_speed = db.Column(db.Integer)
    strstat = db.Column(db.Integer)
    dexstat = db.Column(db.Integer)
    constat = db.Column(db.Integer)
    intstat = db.Column(db.Integer)
    wisstat = db.Column(db.Integer)
    chastat = db.Column(db.Integer)
    skills = db.Column(db.String(127))
    senses = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    level = db.Column(db.Integer)
    abilities = db.relationship("CharacterAbility")
    inventory = db.relationship("CharacterItem")
    spells = db.relationship("CharacterSpell")

class CharacterAbility(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    characterid = db.Column(db.Integer, db.ForeignKey("character.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(2047))

class CharacterItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("character.id"))
    is_custom = db.Column(db.Boolean)
    refitemid = db.Column(db.Integer)
    name = db.Column(db.String(127))
    type = db.Column(db.String(127))
    rarity = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    attunement = db.Column(db.Boolean)
    cost = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    text = db.Column(db.String(16383))
    armor_type = db.Column(db.String(7))
    armor_class = db.Column(db.Integer)
    add_dex = db.Column(db.Boolean)
    is_shield = db.Column(db.Boolean)
    min_strength = db.Column(db.Integer)
    stealth_disadvantage = db.Column(db.Boolean)
    die_num = db.Column(db.Integer)
    damage_die = db.Column(db.Integer)
    weapon_properties = db.Column(db.String(255))
    weapon_special = db.Column(db.String(16383))

class CharacterSpell(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("character.id"))
    is_custom = db.Column(db.Boolean)
    refspellid = db.Column(db.Integer)
    name = db.Column(db.String(127))
    school = db.Column(db.String(31))
    level = db.Column(db.Integer)
    casting_time = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    verbal = db.Column(db.Boolean)
    somatic = db.Column(db.Boolean)
    material = db.Column(db.Boolean)
    consumes_material = db.Column(db.Boolean)
    duration = db.Column(db.String)
    text = db.Column(db.String(16383))