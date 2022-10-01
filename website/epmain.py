from flask import Blueprint, Flask, render_template, redirect, url_for, request, session

epmain = Blueprint("epmain", __name__)

@epmain.route("/")
def home():
    return(render_template("index.html"))

