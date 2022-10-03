from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user

eptool = Blueprint('eptool', __name__)

## TOOLS
@eptool.route("/")
def tools():
    return(render_template("tools.html", user=current_user))

@eptool.route("/VTT")
def vtt():
    return(render_template("vtt.html", user=current_user))

@eptool.route("/NPC-Gen")
def npcGen():
    return(render_template("npc-gen.html", user=current_user))

@eptool.route("/Backstory-Gen")
def backstoryGen():
    return(render_template("backstory-gen.html", user=current_user))

@eptool.route("/CR-Calc")
def crCalc():
    return(render_template("cr-calc.html", user=current_user))

@eptool.route("/Encounter-Gen")
def encounterGen():
    return(render_template("encounter-gen.html", user=current_user))

@eptool.route("/Loot-Gen")
def lootGen():
    return(render_template("loot-gen.html", user=current_user))

@eptool.route("/Stat-Gen")
def statGen():
    return(render_template("stat-gen.html", user=current_user))

@eptool.route("/Backstory")
def backstory():
    return(render_template("backstory.html", user=current_user))
