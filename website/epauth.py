from flask import Blueprint, Flask, render_template, redirect, url_for, request, session

epauth = Blueprint('epauth', __name__)

@epauth.route("/login")
def login():
    return("under construction")

@epauth.route("/logout")
def logout():
    return("under construction")

@epauth.route("/signup")
def signUp():
    return(render_template("signup.html"))
