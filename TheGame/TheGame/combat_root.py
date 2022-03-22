from typing import List
from models import Champion, SpecificWeapon, SpecificItem
from unit import Unit, Damage
from GameState import GameState
from random import seed, randint
from action import Action
from processes import getArmour, getGlory, getShields


def battle(attacker: Champion, defender: Champion) -> List:
    seed()

    pAtt = preprocess(attacker)
    pDef = preprocess(defender)
    actions = []

    # main cycle

    actions = fight(pAtt, pDef)

    # resolution

    if(pAtt.attH >= 0):
        attacker.pHealth = pAtt.attH
    else:
        attacker.pHealth = 1
    if(pDef.attH >= 0):
        defender.pHealth = pDef.attH
    else:
        defender.pHealth = 1

    # return
    return actions


def fight(pAtt: Unit, pDef: Unit):
    actions = []
    GS = GameState(10)

    if(pDef.glory > pAtt.glory):
        for action in turn(pDef, pAtt, GS):
            actions.append(action)
    else:
        if(pDef.glory == pAtt.glory):
            if(randint(0, 1) > 0):
                for action in turn(pDef, pAtt, GS):
                    actions.append(action)

    while(True):
        if(pAtt.attH <= 0):
            break
        for action in turn(pAtt, pDef, GS):
            actions.append(action)
        if(pDef.attH <= 0):
            break
        for action in turn(pDef, pAtt, GS):
            actions.append(action)

    return actions


def decide(active: Unit, other: Unit, GS: GameState):
    a = None
    if(active.weapon.range > GS.distance):
        a = Action("move_closer", 1)
        return a

    a = Action("attack", active.weapon.ap_cost)

    return a


def turn(active: Unit, other: Unit, GS: GameState) -> List:
    finished = False
    actions = []
    active.newTurn()

    while(not(finished)):
        action = decide(active, other, GS)
        match(action.type):
            case "attack":
                active.spendActionPoints(action.cost)
                action = attack(active, action.weapon, other, GS)
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


def attack(attacker: Unit, weapon: SpecificWeapon,
           target: Unit, GS: GameState):
    hits = 0
    a = Action("attack", weapon.ap_cost)
    if(GS.distance > weapon.range):

        return a.attackResolved([Damage(0, 0)])

    for _ in range(attacker.getAtt(weapon.associated)):
        if(randint(0, 1) > 0):
            hits += 1
    if(hits >= target.attA):
        dmgs = []
        for _ in range(weapon.damageInstances):
            dmg = target.damage(weapon.damageNumber)
            dmgs.append(dmg)
    return a.attackResolved(dmgs)


def preprocess(character: Champion) -> Unit:
    a = character.pAthletics
    b = character.pBrain
    c = character.pControl
    h = character.pHealth

    shield = getShields(champion=character)
    armour = getArmour(champion=character)
    glory = getGlory(champion=character)

    u = Unit(a, b, c, h, shield, armour, glory)

    u.setPrimaryWeapon = character.primaryWeapon

    return u
