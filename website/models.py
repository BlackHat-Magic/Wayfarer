from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    rulesets = db.relationship("Ruleset")

class Ruleset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    rules = db.relationship("HouseRule")
    languages = db.relationship("Language")
    items = db.relationship("Item")
    conditions = db.relationship("Condition")
    skills = db.relationship("Skill")
    actions = db.relationship("Action")
    races = db.relationship("Race")
    feats = db.relationship("Feat")
    backgrounds = db.relationship("Background")
    classes = db.relationship("Playerclass")
    multiclassspelltable = db.relationship("MulticlassSpellTable")
    leveltable = db.relationship("LevelTable")
    monsters = db.relationship("Monster")
    

class HouseRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(511))
    text = db.Column(db.String(16383))

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(255))
    speakers = db.Column(db.String(255))
    script = db.Column(db.String(127))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    type = db.Column(db.String(127))
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

class MagicItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
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

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    ability_score = db.Column(db.String(3))

class Action(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Race(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    strasi = db.Column(db.Integer)
    dexasi = db.Column(db.Integer)
    conasi = db.Column(db.Integer)
    intasi = db.Column(db.Integer)
    wisasi = db.Column(db.Integer)
    chaasi = db.Column(db.Integer)
    asioverride = db.Column(db.String(255))
    size = db.Column(db.Integer)
    sizeoverride = db.Column(db.String(255))
    walkspeed = db.Column(db.Integer)
    flyspeed = db.Column(db.Integer)
    swimspeed = db.Column(db.Integer)
    burrowspeed = db.Column(db.Integer)
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
    subrace_featires = db.relationship("SubraceFeature")

class SubraceFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    raceid = db.Column(db.Integer, db.ForeignKey("subrace.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

class Feat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    prerequisite = db.Column(db.String(255))
    strasi = db.Column(db.Integer)
    dexasi = db.Column(db.Integer)
    conasi = db.Column(db.Integer)
    intasi = db.Column(db.Integer)
    wisasi = db.Column(db.Integer)
    chaasi = db.Column(db.Integer)
    text = db.Column(db.String(16383))

class Background(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    skills = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    equipment = db.Column(db.String(511))
    text = db.Column(db.String(16383))
    background_features = db.relationship("BackgroundFeature")

class BackgroundFeature(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    backgroundid = db.Column(db.Integer, db.ForeignKey("background.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))

# classes are called professions in the code because SQLAlchemy gets mad whenever I name it "playerclass" or any variant of such and I can't for the life of me figure out why.
class Playerclass(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    name = db.Column(db.String(127))
    text = db.Column(db.String(16383))
    caster_type = db.Column(db.Integer)
    multiclassprereq = db.Column(db.String(127))
    multiclassskills = db.Column(db.String(255))
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

class MulticlassSpellTable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
    text = db.Column(db.String(16383))

class LevelTable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rulesetid = db.Column(db.Integer, db.ForeignKey("ruleset.id"))
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
    walkspeed = db.Column(db.Integer)
    flyspeed = db.Column(db.Integer)
    swimspeed = db.Column(db.Integer)
    burrowspeed = db.Column(db.Integer)
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
    # ability, action, bonusaction, reaction, villainaction, legendaryaction, mythicaction, lairaction
    type = db.Column(db.Integer)
    name = db.Column(db.String(127))
    text = db.Column(db.String(2047))
