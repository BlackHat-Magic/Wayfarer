from flask import Blueprint, Flask, render_template, redirect, url_for, request, session

eptool = Blueprint('eptool', __name__)

## TOOLS
@eptool.route("/")
def tools():
    return(render_template("tools.html"))

@eptool.route("/VTT")
def vtt():
    return(render_template("vtt.html"))

@eptool.route("/NPC-Gen")
def npcGen():
    return(render_template("npc-gen.html"))

@eptool.route("/Backstory-Gen")
def backstoryGen():
    return(render_template("backstory-gen.html"))

@eptool.route("/CR-Calc")
def crCalc():
    return(render_template("cr-calc.html"))

@eptool.route("/Encounter-Gen")
def encounterGen():
    return(render_template("encounter-gen.html"))

@eptool.route("/Loot-Gen")
def lootGen():
    return(render_template("loot-gen.html"))

@eptool.route("/Stat-Gen")
def statGen():
    return(render_template("stat-gen.html"))
