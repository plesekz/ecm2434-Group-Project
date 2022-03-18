from typing import List
from models import Champion
from unit import Unit
from GameState import GameState

def battle (attacker : Champion, defender : Champion) -> List:
    pAtt = preprocess(attacker)
    pDef = preprocess(defender)
    actions = []

    # main cycle

    actions = fight(pAtt, pDef)

    # resolution

    if(pAtt.attH>0):
        attacker.pHealth = pAtt.attH
    else:
        attacker.pHealth = 1
    if(pDef.attH>0):
        defender.pHealth = pDef.attH
    else:
        defender.pHealth = 1

    # return
    return actions

def fight(pAtt: Unit, pDef : Unit):
    actions = []
    GS = GameState(10)

    if(pDef.glory > pAtt.glory):
        for action in turn(pDef,pAtt,GS):
            actions.append(action)
    else:
        if(pDef.glory == pAtt.glory):
            resolve # who goes first randomly
            # if defender goes first, do their turn
            # if attacker goes first, just continue to the cycle
    
    while(True):
        if(pAtt.attH<=0):
            break
        for action in turn(pAtt,pDef,GS):
            actions.append(action)
        if(pDef.attH<=0):
            break
        for action in turn(pDef,pAtt,GS):
            actions.append(action)

    return actions

def turn(active : Unit, other : Unit, GS: GameState) -> List:
    finished = False
    actions = []
    while(not(finished)):
        action = decide(active, other, GS)
        match(action.type):
            case "attack":
                active.spendActionPoints(action.cost)
                action = attack(active, other)
            case "move_closer":
                active.spendActionPoints(1)
                GS.distance = GS.distance - 1
            case "move_away":
                active.spendActionPoints(1)
                GS.distance = GS.distance + 1
            case "finish":
                finished = True
        actions.append(action)
    return actions
    
def attack(attacker : Unit, weapon ,target : Unit):
    hits = None
    if(hits >= target.attA):
        for i in range(weapon.damageInstances):
            target.damage(weapon.damageNumber)

def preprocess(character : Champion) -> Unit:
    a = character.pAthletics
    b = character.pBrain
    c = character.pControl
    h = character.pHealth

    shield = 0
    armour = 0
    glory = 0

    return Unit(a, b, c, h, shield, armour, glory)