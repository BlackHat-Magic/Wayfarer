from flask_login import current_user
from .models import User, Ruleset

def getForeignRulesets(user):
    if(not user.is_authenticated):
        return([])
    elif(not user.foreign_ruleset):
        return([])
    else:
        frulesets = []
        if(len(user.foreign_ruleset.split(",")) > 1):
            frulesetids = user.foreign_ruleset.split(",")
        else:
            frulesetids = [user.foreign_ruleset]
        index = 0
        for i in frulesetids:
            frulesets.append(Ruleset.query.filter_by(id=int(frulesetids[index])).first())
            index += 1
        return(frulesets)

def getCurrentRuleset(user):
    if(not user.is_authenticated):
        return(Ruleset.query.filter_by(is_admin=True).first())
    return(Ruleset.query.filter_by(id=current_user.current_ruleset).first())
