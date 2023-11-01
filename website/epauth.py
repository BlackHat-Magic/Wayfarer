from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash
from .models import User, Ruleset
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .uservalidation import *

epauth = Blueprint('epauth', __name__)

# Login endpoints
# Redirect with no subdomain
@epauth.route("/Login")
def noRulesetLogin():
    return(noRuleset(current_user, "epauth.login"))
# Subdomain
@epauth.route("/Login", methods=["GET", "POST"], subdomain="<ruleset>")
def login(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # Login user with POST request
    if(request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username = username).first()
        # If user exists, validate credentials
        if(user):
            if(check_password_hash(user.password, password)):
                login_user(user, remember=True)
                flash(f"Welcome back, {username}.", "green")
                adminrulesets, cruleset = validateRuleset(current_user, ruleset)
                return(redirect(url_for("epmain.home", ruleset=cruleset.identifier)))
            else:
                flash("Incorrect password.", "red")
        # Else, flash error that user does not exist
        else:
            flash("User does not exist.", "red")  
    # Else return login page
    return(
        render_template(
            "login.html", 
            user=current_user, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Log In"
        )
    )

# Logout endpoints; login required
# Redirect with no subdomain
@epauth.route("/Logout")
@login_required
def noRulesetLogout():
    return(noRuleset(current_user, "epauth.logout"))
# Subdomain
@epauth.route("/Logout", subdomain="<ruleset>")  
@login_required
def logout(ruleset):
    logout_user()
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    return(redirect(url_for("epmain.home", ruleset=cruleset.identifier)))

# Signup endpoints
# Redirect with no subdomain
@epauth.route("/Signup")
def noRulesetSignup():
    return(noRuleset(current_user, "epauth.signup"))
# Subdomain
@epauth.route("/Signup", methods=["GET", "POST"], subdomain="<ruleset>")
def signUp(ruleset):
    adminrulesets, cruleset = validateRuleset(current_user, ruleset)
    # If POST request, process signup info
    if(request.method == "POST"):
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(username=username).first()
        # Validate input data
        if(user):
            flash("Username already in use. Please pick another username.", "red")
        elif(len(username) < 4):
            flash("Username must be at least 4 characters.", "red")
        elif(len(username) > 255):
            flash("Username must be fewer than 256 characters.", "red")
        elif(password1 != password2):
            flash("Passwords do not match", "red")
        elif(len(password1) < 8):
            flash("Password must be at least 8 characters", "red")
        else:
            # Create user with admin ruleset as current ruleset if admin rulesets exist
            try:
                new_user = User(username = username, email = email, password=generate_password_hash(password1, method="pbkdf2"), current_ruleset=Ruleset.query.filter_by(is_admin=True).first().id)
            # Otherwise create user with no current ruleset
            except:
                new_user = User(username = username, email = email, password=generate_password_hash(password1, method="pbkdf2"))
            db.session.add(new_user)
            db.session.commit()
            login_user(User.query.filter_by(username = username).first(), remember = True)
            flash(f"Welcome, {username}.", "green")
            return(redirect(url_for("epmain.home", ruleset=cruleset.identifier)))
    # Else return signup page
    return(
        render_template(
            "signup.html", 
            user=current_user, 
            cruleset=cruleset, 
            adminrulesets=adminrulesets, 
            title="Sign Up"
        )
    )