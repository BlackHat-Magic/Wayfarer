from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import random

def shortid(length):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_"
    return ''.join(random.choice(characters) for _ in range(length))

class User(db.Model, UserMixin):
    id = db.Column(db.String(32), primary_key=True, default=lambda: shortid(8))
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    foreign_ruleset = db.Column(db.String(1023))
    current_ruleset = db.Column(db.Integer)
    rulesets = db.relationship("Ruleset")
    characters = db.relationship("Character")

class Ruleset(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=lambda: shortid(8))
    is_admin = db.Column(db.Boolean)
    userid = db.Column(db.String(36), db.ForeignKey("user.id"))
    is_shareable = db.Column(db.Boolean)
    name = db.Column(db.String(127))
    description = db.Column(db.String(16383))
    categories = db.relationship("Category")
    languages = db.relationship("Language")
    recipes = db.relationship("Recipe")
    item_tags = db.relationship("ItemTag")
    item_properties = db.relationship("Property")
    items = db.relationship("Item")
    conditions = db.relationship("Condition")
    diseases = db.relationship("Disease")
    statuses = db.relationship("Status")
    skills = db.relationship("Skill")
    actions = db.relationship("Action")
    races = db.relationship("Race")
    feats = db.relationship("Feat")
    ability_scores = db.relationship("AbilityScore")
    spells = db.relationship("Spell")
    backgrounds = db.relationship("Background")
    classes = db.relationship("Playerclass")
    monsters = db.relationship("Monster")
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
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
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class ItemTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    is_magical = db.Column(db.Boolean)
    rarity = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    attunement = db.Column(db.Boolean)
    tags = db.Column(db.PickleType)
    proficiency = db.Column(db.Boolean)
    cost = db.Column(db.Integer)
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
    weapon_properties = db.Column(db.PickleType)

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(63))
    ability_score = db.Column(db.String(3))
    description = db.Column(db.String(16383))

class Action(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    time = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Race(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    flavor = db.Column(db.String(16383))
    asis = db.Column(db.PickleType)
    asi_text = db.Column(db.String(255))
    size = db.Column(db.Integer)
    size_text = db.Column(db.String(255))
    walk = db.Column(db.Integer)
    climb = db.Column(db.Integer)
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
    race_features = db.relationship("RaceFeature", backref="race")
    subraces = db.relationship("Subrace", backref="race")

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
    subrace_features = db.relationship("SubraceFeature", backref="subrace")

class SubraceFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("subrace.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Feat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    prerequisite = db.Column(db.String(255))
    text = db.Column(db.String(16383))

class AbilityScore(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    order = db.Column(db.Integer)
    abbr = db.Column(db.String(3))
    text = db.Column(db.String(16383))

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    school = db.Column(db.String(31))
    level = db.Column(db.Integer)
    casting_time = db.Column(db.Integer)
    spell_range = db.Column(db.Integer)
    verbal = db.Column(db.Boolean)
    somatic = db.Column(db.Boolean)
    material = db.Column(db.Boolean)
    material_specific = db.Column(db.String(255))
    consumes_material = db.Column(db.Boolean)
    concentration = db.Column(db.Boolean)
    duration = db.Column(db.String)
    text = db.Column(db.String(16383))

class Background(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    skills = db.Column(db.PickleType)
    tools = db.Column(db.PickleType)
    lang_num = db.Column(db.Integer)
    languages = db.Column(db.PickleType)
    equipment = db.Column(db.PickleType)
    gold_container = db.Column(db.String(127))
    starting_gold = db.Column(db.Integer)
    text = db.Column(db.String(16383))
    background_features = db.relationship("BackgroundFeature", backref="background")

class BackgroundFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    backgroundid = db.Column(db.Integer, db.ForeignKey("background.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

# not UpperCamelCase because SQLAlchemy gets mad when it is. idk why
class Playerclass(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    hitdie = db.Column(db.Integer)
    proficiencies = db.Column(db.PickleType)
    saves = db.Column(db.PickleType)
    skills = db.Column(db.PickleType)
    equipment = db.Column(db.String(1023))
    gold_nums = db.Column(db.Integer)
    gold_dice = db.Column(db.Integer)
    gold_mult = db.Column(db.Integer)
    multiclass_prereq = db.Column(db.String(1023))
    multiclass_profic = db.Column(db.PickleType)
    subclass_name = db.Column(db.String(127))
    subclass_level = db.Column(db.Integer)
    levels = db.Column(db.Integer)
    text = db.Column(db.String(16383))
    class_features = db.relationship("ClassFeature")
    subclasses = db.relationship("Subclass")
    columns = db.relationship("ClassColumn")

class ClassFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    level_obtained = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class ClassColumn(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    name = db.Column(db.String(127))
    data = db.Column(db.PickleType)

class Subclass(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    caster_type = db.Column(db.Integer)
    subclass_features = db.relationship("SubclassFeature")
    columns = db.relationship("SubclassColumn")

class SubclassFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subclassid = db.Column(db.Integer, db.ForeignKey("subclass.id"))
    level_obtained = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class SubclassColumn(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subclassid = db.Column(db.Integer, db.ForeignKey("subclass.id"))
    name = db.Column(db.String(127))
    data = db.Column(db.PickleType)

class Monster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
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
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    is_npc = db.Column(db.Boolean)
    userid = db.Column(db.String(36), db.ForeignKey("user.id"))
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