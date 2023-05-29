from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import random

def shortid(length):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_"
    return ''.join(random.choice(characters) for _ in range(length))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.String(32), primary_key=True, default=lambda: shortid(8))
    is_admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    characters = db.relationship("Character", backref="user")
    rulesets = db.relationship("Ruleset", backref="user")
    foreign_ruleset = db.Column(db.PickleType, default=[])
    current_ruleset = db.Column(db.String(32))

class Ruleset(db.Model):
    __tablename__ = "ruleset"
    id = db.Column(db.String(32), primary_key=True, default=lambda: shortid(8))
    identifier = db.Column(db.String(31), unique=True)
    is_admin = db.Column(db.Boolean)
    userid = db.Column(db.String(36), db.ForeignKey("user.id"))
    viewers = db.Column(db.PickleType)
    editors = db.Column(db.PickleType)
    visibility = db.Column(db.Integer)
    name = db.Column(db.String(127))
    description = db.Column(db.String(16383))
    categories = db.relationship("Category", backref="ruleset")
    languages = db.relationship("Language", backref="ruleset")
    recipes = db.relationship("Recipe", backref="ruleset")
    item_tags = db.relationship("ItemTag", backref="ruleset")
    item_properties = db.relationship("Property", backref="ruleset")
    items = db.relationship("Item", backref="ruleset")
    conditions = db.relationship("Condition", backref="ruleset")
    diseases = db.relationship("Disease", backref="ruleset")
    statuses = db.relationship("Status", backref="ruleset")
    skills = db.relationship("Skill", backref="ruleset")
    actions = db.relationship("Action", backref="ruleset")
    races = db.relationship("Race", backref="ruleset")
    feats = db.relationship("Feat", backref="ruleset")
    ability_scores = db.relationship("AbilityScore", backref="ruleset")
    spells = db.relationship("Spell", backref="ruleset")
    backgrounds = db.relationship("Background", backref="ruleset")
    classes = db.relationship("Playerclass", backref="ruleset")
    currencies = db.relationship("Currency", backref="ruleset")
    characters = db.relationship("Character", backref="ruleset")
    monster = db.relationship("Monster", backref="ruleset")
    monster_type = db.relationship("MonsterType", backref="ruleset")
    damage_type = db.relationship("DamageType", backref="ruleset")
    
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    pinned = db.Column(db.Boolean)
    rules = db.relationship("Rule", backref="category")

class Rule(db.Model):
    __tablename__ = "rule"
    id = db.Column(db.Integer, primary_key=True)
    rule_categoryid = db.Column(db.Integer, db.ForeignKey("category.id"))
    pinned = db.Column(db.Boolean)
    name = db.Column(db.String(511))
    text = db.Column(db.String(16383))

class Language(db.Model):
    __tablename__ = "language"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    images = db.Column(db.PickleType)

class ItemTag(db.Model):
    __tablename__ = "itemtag"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Property(db.Model):
    __tablename__ = "property"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Item(db.Model):
    __tablename__ = "item"
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
    images = db.Column(db.PickleType)
    is_armor = db.Column(db.Boolean)
    stealth = db.Column(db.Boolean)
    strength = db.Column(db.Integer)
    armor_class = db.Column(db.Integer)
    add_dex = db.Column(db.Boolean)
    max_dex = db.Column(db.Integer)
    is_weapon = db.Column(db.Boolean)
    die_num = db.Column(db.Integer)
    damage_die = db.Column(db.Integer)
    damage_type = db.Column(db.String(15))
    weapon_properties = db.Column(db.PickleType)

class Condition(db.Model):
    __tablename__ = "condition"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Disease(db.Model):
    __tablename__ = "disease"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Skill(db.Model):
    __tablename__ = "skill"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(63))
    ability_score = db.Column(db.String(3))
    description = db.Column(db.String(16383))

class Action(db.Model):
    __tablename__ = "action"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    time = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Race(db.Model):
    __tablename__ = "race"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    flavor = db.Column(db.String(16383))
    images = db.Column(db.PickleType)
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
    __tablename__ = "racefeature"
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("race.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Subrace(db.Model):
    __tablename__ = "subrace"
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("race.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    images = db.Column(db.PickleType)
    subrace_features = db.relationship("SubraceFeature", backref="subrace")

class SubraceFeature(db.Model):
    __tablename__ = "subracefeature"
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("subrace.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Feat(db.Model):
    __tablename__ = "feat"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    prerequisite = db.Column(db.String(255))
    text = db.Column(db.String(16383))

class AbilityScore(db.Model):
    __tablename__ = "abilityscore"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.String(36), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    order = db.Column(db.Integer)
    abbr = db.Column(db.String(3))
    text = db.Column(db.String(16383))

class Spell(db.Model):
    __tablename__ = "spell"
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
    __tablename__ = "background"
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
    images = db.Column(db.PickleType)
    background_features = db.relationship("BackgroundFeature", backref="background")

class BackgroundFeature(db.Model):
    __tablename__ = "backgroundfeature"
    id = db.Column(db.Integer, primary_key = True)
    backgroundid = db.Column(db.Integer, db.ForeignKey("background.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

# not UpperCamelCase because SQLAlchemy gets mad when it is. idk why
class Playerclass(db.Model):
    __tablename__ = "playerclass"
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
    images = db.Column(db.PickleType)
    class_features = db.relationship("ClassFeature", backref = "playerclass")
    subclasses = db.relationship("Subclass", backref = "playerclass")
    columns = db.relationship("ClassColumn", backref = "playerclass")

class ClassFeature(db.Model):
    __tablename__ = "classfeature"
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    level_obtained = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class ClassColumn(db.Model):
    __tablename__ = "classcolumn"
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    name = db.Column(db.String(127))
    data = db.Column(db.PickleType)

class Subclass(db.Model):
    __tablename__ = "subclass"
    id = db.Column(db.Integer, primary_key = True)
    classid = db.Column(db.Integer, db.ForeignKey("playerclass.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    images = db.Column(db.PickleType)
    caster_type = db.Column(db.Integer)
    subclass_features = db.relationship("SubclassFeature", backref="subclass")
    columns = db.relationship("SubclassColumn", backref="subclass")

class SubclassFeature(db.Model):
    __tablename__ = "subclassfeature"
    id = db.Column(db.Integer, primary_key = True)
    subclassid = db.Column(db.Integer, db.ForeignKey("subclass.id"))
    level_obtained = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class SubclassColumn(db.Model):
    __tablename__ = "subclasscolumn"
    id = db.Column(db.Integer, primary_key = True)
    subclassid = db.Column(db.Integer, db.ForeignKey("subclass.id"))
    name = db.Column(db.String(127))
    data = db.Column(db.PickleType)

class Currency(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    value = db.Column(db.Integer)
    text = db.Column(db.String(16383))

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    is_npc = db.Column(db.Boolean)
    userid = db.Column(db.String(32), db.ForeignKey("user.id"))
    rulesetid = db.Column(db.String(32), db.ForeignKey("ruleset.id"))
    race = db.Column(db.String(127))
    walk = db.Column(db.Integer)
    climb = db.Column(db.Integer)
    fly = db.Column(db.Integer)
    hover = db.Column(db.Boolean)
    swim = db.Column(db.Integer)
    burrow = db.Column(db.Integer)
    alignment = db.Column(db.String)
    experience = db.Column(db.Integer)
    background = db.Column(db.String(127))
    personality = db.Column(db.String(16383))
    ideals = db.Column(db.String(16383))
    bonds = db.Column(db.String(16383))
    flaws = db.Column(db.String(16383))
    backstory = db.Column(db.String(16383))
    notes = db.Column(db.String(16383))
    images = db.Column(db.PickleType)
    classes = db.Column(db.PickleType)
    level = db.Column(db.Integer)
    proficiency_bonus = db.Column(db.Integer)
    saves = db.Column(db.PickleType) # index of ability in CHARACTER (not database ID)
    skills = db.Column(db.PickleType)
    proficiencies = db.Column(db.PickleType)
    armor_class = db.Column(db.Integer)
    initiative = db.Column(db.Integer) # stored as bonus
    current_hp = db.Column(db.Integer)
    max_hp = db.Column(db.Integer)
    temp_hp = db.Column(db.Integer)
    current_hit_dice = db.Column(db.Integer)
    max_hit_dice = db.Column(db.Integer)
    death_saves = db.Column(db.PickleType)
    currency = db.Column(db.PickleType)
    features = db.relationship("CharacterFeature", backref="character")
    attacks = db.relationship("CharacterAttack", backref="character")
    items = db.relationship("CharacterItem", backref="character")
    spells = db.Column(db.PickleType)# name
    spellcasting_ability = db.Column(db.Integer) # index of ability score in CHARACTEr (not database ID)
    spell_attack_misc_bonus = db.Column(db.Integer)
    spell_savedc_misc_bonus = db.Column(db.Integer)

class CharacterFeature(db.Model):
    __tablename__ = "characterfeature"
    id = db.Column(db.Integer, primary_key=True)
    characterid = db.Column(db.Integer, db.ForeignKey("character.id"))
    comes_from = db.Column(db.String(127)) # race? class? background? etc; name
    reference = db.Column(db.Integer) # name
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class CharacterAttack(db.Model):
    __tablename__ = "characterattack"
    id = db.Column(db.Integer, primary_key=True)
    characterid = db.Column(db.Integer, db.ForeignKey("character.id"))
    name = db.Column(db.String(127))
    ability_score = db.Column(db.Integer) # index of ability in CHARACTER (not database ID)
    misc_bonus = db.Column(db.Integer)
    proficient = db.Column(db.Boolean)
    attack_range = db.Column(db.Integer)
    damage_nums = db.Column(db.Integer)
    damage_dice = db.Column(db.Integer)
    crit_nums = db.Column(db.Integer)
    crit_die = db.Column(db.Integer)
    add_ability = db.Column(db.Boolean)
    damage_type = db.Column(db.String(127))
    note = db.Column(db.String(16383))

class CharacterItem(db.Model):
    __tablename__ = "characteritem"
    id = db.Column(db.Integer, primary_key=True)
    characterid = db.Column(db.Integer, db.ForeignKey("character.id"))
    reference = db.Column(db.Integer) # reference item name
    quantity = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Monster(db.Model):
    __tablename__ = "monster"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(32), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    shortened_name = db.Column(db.String(127))
    shortened_plural = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    images = db.Column(db.PickleType)
    size = db.Column(db.Integer)
    size_text = db.Column(db.String(127))
    monster_type = db.Column(db.Integer) # MonsterType name
    monster_subtype = db.Column(db.Integer) # MonsterSubtype name
    type_text = db.Column(db.String(127))
    alignment = db.Column(db.String(127))
    armor_item = db.Column(db.Integer) # Item name
    base_ac = db.Column(db.Integer)
    custom_armor = db.Column(db.String(127))
    has_shield = db.Column(db.Boolean)
    die_num = db.Column(db.Integer)
    hit_die = db.Column(db.Integer)
    avg_hp = db.Column(db.Integer)
    walk = db.Column(db.Integer)
    climb = db.Column(db.Integer)
    fly = db.Column(db.Integer)
    hover = db.Column(db.Boolean)
    swim = db.Column(db.Integer)
    burrow = db.Column(db.Integer)
    ability_scores = db.Column(db.PickleType)
    saves = db.Column(db.PickleType)  # index of ability in CHARACTER (not database ID)
    versatile = db.Column(db.PickleType) # name
    skills = db.Column(db.PickleType) # name
    expertise = db.Column(db.PickleType) # name
    damage_immunities = db.Column(db.PickleType) # Type ID
    damage_resistances = db.Column(db.PickleType) # ^
    damage_vulnerabilities = db.Column(db.PickleType) # ^
    condition_immunities = db.Column(db.PickleType) # Condition ID
    senses = db.Column(db.PickleType) # Sense ID
    languages = db.Column(db.PickleType) # Language ID
    challenge_rating = db.Column(db.Float)
    features = db.relationship("MonsterFeature", backref="monster")
    is_legendary = db.Column(db.Boolean)
    is_mythic = db.Column(db.Boolean)
    is_villain = db.Column(db.Boolean)
    has_lair = db.Column(db.Boolean)
    actions = db.relationship("MonsterAction", backref="monster")
    reactions_text = db.Column(db.String(16383))
    bonus_actions_text = db.Column(db.String(16383))
    actions_text = db.Column(db.String(16383))
    legendary_actions_text = db.Column(db.String(16383))
    mythic_actions_text = db.Column(db.String(16383))
    villain_actions_text = db.Column(db.String(16383))
    lair_actions_text = db.Column(db.String(16383))
    custom_actions_text = db.Column(db.PickleType)

class MonsterType(db.Model):
    __tablename__ = "monstertype"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(32), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383)) # might stay unused
    subtypes = db.relationship("MonsterSubtype", backref="monstertype")

class MonsterSubtype(db.Model):
    __tablename__ = "monstersubtype"
    id = db.Column(db.Integer, primary_key=True)
    typeid = db.Column(db.Integer, db.ForeignKey("monstertype.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383)) # might stay unused

class DamageType(db.Model):
    __tablename__ = "damagetype"
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.String(32), db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383)) # might stay unused

class MonsterFeature(db.Model):
    __tablenae__ = "monsterfeature"
    id = db.Column(db.Integer, primary_key=True)
    monsterid = db.Column(db.Integer, db.ForeignKey("monster.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class MonsterAction(db.Model):
    __tablename__ = "monsteraction"
    id = db.Column(db.Integer, primary_key=True)
    monsterid = db.Column(db.Integer, db.ForeignKey("monster.id"))
    action_type = db.Column(db.String(31)) # reaction, bonus, action, legendary action, mythic action, lair action, villain action; string to allow custom
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))