from flask import Blueprint, Flask, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user

epmain = Blueprint("epmain", __name__)

@epmain.route("/")
def home():
    return(render_template("index.html", user=current_user))

