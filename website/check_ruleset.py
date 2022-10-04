from flask_login import current_user
from .models import User, Ruleset

def getForeignRulesets(user):
    if(not user.is_authenticated):
        return([])
    elif(not user.foreign_ruleset):
        return([])
    else:
        frulesets = []
        for i in frulesetids:
            frulesets.append(Ruleset.query.filter_by(id=frulesetids[i]))
        return(frulesets)

def  getCurrentRuleset(user):
    if(not user.is_authenticated):
        return(Ruleset.query.filter_by(id=1).first())
    return(Ruleset.query.filter_by(id=current_user.current_ruleset).first())
