from flask import flash
from .models import User, Ruleset
from . import db

def validateRuleset(current_user, ruleset):
    adminrulesets = Ruleset.query.filter_by(is_admin=True)
    cruleset = Ruleset.query.filter_by(identifier=ruleset).first_or_404()
    if(current_user.is_authenticated):
        if(cruleset.userid != current_user.id and not cruleset.is_shareable):
            flash("Ruleset is private. Switched to a ruleset you have access to.", "red")
            if(current_user.current_ruleset == cruleset.id):
                current_user.current_ruleset = adminrulesets[0]
                db.session.commit()
            cruleset = adminrulesets[0]
        if(current_user.current_ruleset != cruleset.id):
            current_user.current_ruleset = cruleset.id
            db.session.commit()
            flash(f"Switched to viewing ruleset \"{cruleset.name}\"", "green")
    elif(not cruleset.is_shareable):
        flash("Ruleset is private. Switched to a ruleset you have access to.", "red")
        cruleset = adminrulesets[0]
    return(adminrulesets, cruleset)