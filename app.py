from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = open("session.key")
#db = SQLAlchemy(app)


## RULES
@app.route("/")
def home():
    return(render_template("index.html"))

@app.route("/Rules")
def rules():
    return(render_template("rules.html"))

@app.route("/Rules/House-Rules")
def houseRules():
    return(render_template("house-rules.html"))

@app.route("/Rules/Higher-Levels")
def higherLevels():
    return(render_template("higher-levels.html"))

@app.route("/Rules/Languages")
def languages():
    return(render_template("languages.html"))

@app.route("/Rules/Multiclassing")
def multiclassing():
    return(render_template("multiclassing.html"))

@app.route("/Rules/Step-by-Step")
def stepByStep():
    return(render_template("step-by-step.html"))

## CHARACTERS
@app.route("/Characters")
def char():
    return(render_template("characters.html"))

@app.route("/Characters/Races")
def races():
    return(render_template("races.html"))

@app.route("/Characters/Backgrounds")
def backgrounds():
    return(render_template("backgrounds.html"))

@app.route("/Characters/Feats")
def feats():
    return(render_template("feats.html"))

@app.route("/Characters/Other")
def other():
    return(render_template("other.html"))

@app.route("/Characters/Stats")
def stats():
    return(render_template("stats.html"))

@app.route("/Characters/Backstory")
def backstory():
    return(render_template("backstory.html"))

@app.route("/Characters/Name")
def name():
    return(render_template("name.html"))

## QUICK REFERENCE
@app.route("/Quick-Reference")
def qref():
    return(render_template("quick-reference.html"))

@app.route("/Quick-Reference/Actions")
def actions():
    return(render_template("actions.html"))

@app.route("/Quick-Reference/Conditions")
def conditions():
    return(render_template("conditions.html"))

@app.route("/Quick-Reference/Items")
def items():
    return(render_template("items.html"))

@app.route("/Quick-Reference/Magic-Items")
def magicItems():
    return(render_template("magic-items.html"))

@app.route("/Quick-Reference/Languages")
def qrefLang():
    return(render_template("qref-lang.html"))

@app.route("/Quick-Reference/Spells")
def spells():
    return(render_template("spells.html"))

@app.route("/Quick-Reference/Vehicles")
def vehicles():
    return(render_template("vehicles.html"))

@app.route("/Quick-Reference/Recipes")
def recipes():
    return(render_template("recipes.html"))

## TOOLS
@app.route("/Tools")
def tools():
    return(render_template("tools.html"))

@app.route("/Tools/VTT")
def vtt():
    return(render_template("vtt.html"))

@app.route("/Tools/NPC-Gen")
def npcGen():
    return(render_template("npc-gen.html"))

@app.route("/Tools/Backstory-Gen")
def backstoryGen():
    return(render_template("backstory-gen.html"))

@app.route("/Tools/CR-Calc")
def crCalc():
    return(render_template("cr-calc.html"))

@app.route("/Tools/Encounter-Gen")
def encounterGen():
    return(render_template("encounter-gen.html"))

@app.route("/Tools/Loot-Gen")
def lootGen():
    return(render_template("loot-gen.html"))

@app.route("/Tools/Stat-Gen")
def statGen():
    return(render_template("stat-gen.html"))

if(__name__ == "__name__"):
	app.run(host="0.0.0.0")
