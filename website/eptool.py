from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, stream_with_context, Response
from .models import Ruleset, User
from flask_login import login_required, current_user
from .uservalidation import *
import time, openai

eptool = Blueprint('eptool', __name__)

## TOOLS
@eptool.route("/", subdomain="<ruleset>")
def tools(ruleset):
    return(redirect(url_for("epmain.home", ruleset=ruleset)))

@eptool.route("/VTT", subdomain="<ruleset>")
def vtt(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/NPC-Gen", subdomain="<ruleset>")
def npcGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "gen-npc.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Generate NPCs"
        )
    )

@eptool.route("/NPC-Gen/NLD", subdomain="<ruleset>")
def npcGenNLD(ruleset):
    if(not current_user.is_authenticated):
        return(Response("event: END\ndata: Stream ended\n\n", mimetype="text/event-stream"))
    description = request.args.get("description", "no")
    if(description == "no"):
        return(Response("event: END\ndata: Stream ended\n\n"))
    def describer():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "The user will provide you a bulleted list of traits a fantasy character has. Respond with only a natural language description of that character. Word your response like you would a text box found in an adventure book that the game master in a tabletop roleplaying game would read to the players when describing the character as though they were an NPC. If the list includes details that the players would not be able to discern just by looking at the character, ignore them. And don't be too specific with details that the players can discern; they've just met this person, they haven't had time to study them. Make up details if needed."
                    },
                    {
                        "role": "user",
                        "content": description
                    }
                ],
                stream=True
            )
            totality = ""
            for chunk in response:
                delta = chunk["choices"][0]["delta"].get("content", "")
                totality += delta
                yield f"data: {totality}\n\n"
            yield "event: END\ndata: Stream ended\n\n"
        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"
            yield "event: END\ndata: Stream ended\n\n"
    
    return(Response(describer(), mimetype="text/event-stream"))

@eptool.route("/Backstory-Gen", subdomain="<ruleset>")
def backstoryGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/CR-Calc", subdomain="<ruleset>")
def crCalc(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Encounter-Gen", subdomain="<ruleset>")
def encounterGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Loot-Gen", subdomain="<ruleset>")
def lootGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )

@eptool.route("/Stat-Gen", subdomain="<ruleset>")
def statGen(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(
        render_template(
            "unfinished.html", 
            cruleset=cruleset,
            adminrulesets=adminrulesets,
            title="Page Under Construction"
        )
    )
