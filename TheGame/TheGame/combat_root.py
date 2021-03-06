import json
from typing import List
from Resources.models import Resource
from TheGame.models import Champion, SpecificWeapon, SpecificItem
from TheGame.unit import Unit, Damage
from TheGame.GameState import GameState
from random import seed, randint
from TheGame.action import Action
from TheGame.processes import getArmour, getGlory, getShields, createNewSpecificItem, createNewBaseWeapon

"""The entry function, call this function with two champions to have them battle.
"""
def battle(attacker: Champion, defender: Champion) -> List:
    seed()

    pAtt = preprocess(attacker)
    pDef = preprocess(defender)
    actions = []

    # main cycle

    #print("starting battle")
    actions = fight(pAtt, pDef)
    #print("finished battle")

    # resolution

    if(pAtt.attH >= 0):
        attacker.pHealth = pAtt.attH + 5
    else:
        attacker.pHealth = 5
    if(pDef.attH >= 0):
        defender.pHealth = pDef.attH + 5
    else:
        defender.pHealth = 5

    attacker.save()
    defender.save()
    # return
    #
    # retusn json object with all the actions inside it
    return actions

"""Function alternating turns through through the champions until one of them is felled."""
def fight(pAtt: Unit, pDef: Unit) -> List:
    actions = []
    GS = GameState(10)
    actions.append(Action(type="setup",cost=0))
    actions[0].setup(pAtt.vitality+pAtt.attH, pDef.vitality+pDef.attH, pAtt.shield, pDef.shield)

    if(pDef.glory > pAtt.glory):
        actions[0].actor = 'def'
        for action in turn(pDef, pAtt, GS):
            actions.append(action)
    else:
        if(pDef.glory == pAtt.glory):
            if(randint(0, 1) > 0):
                actions[0].actor = 'def'
                for action in turn(pDef, pAtt, GS):
                    actions.append(action)
    if not actions[0].actor:
        actions[0].actor = 'att'

    #print("set up complete")

    while(True):
        #print(GS.distance)
        if(pAtt.attH <= 0):
            #print("player 1 is dead")
            break
        for action in turn(pAtt, pDef, GS):
            #print(action.type)
            actions.append(action)

        
        if(pDef.attH <= 0):
            #print(action.type)
            break
        for action in turn(pDef, pAtt, GS):
            actions.append(action)

        if (actions[-1].type == "finish") and (actions[-2].type == "finish") and (actions[-3].type == "finish"):
            break
        
    json_actions = []
    for action in actions:
        json_actions.append(action.toDict())

    return json_actions

"""An 'ai' function deciding the champion's next move."""
def decide(active: Unit, other: Unit, GS: GameState):
    a = Action("finish", 0)

    #print("remaining action: " + str(active.actionPoints))
    #print("weapon cost:" + str(active.weapon.ap_cost))
    #print("distance:" + str(GS.distance))

    #print((active.weapon.range >= GS.distance) and (active.weapon.ap_cost<=active.actionPoints))

    if(active.weapon.range >= GS.distance) and (active.weapon.ap_cost<=active.actionPoints):
        a = Action("attack", active.weapon.ap_cost)
        a.setWeapon(active.weapon)

    elif(active.actionPoints>0):
        a = Action("move_closer", 1)
        
    return a

"""Function represting one champion's turn"""
def turn(active: Unit, other: Unit, GS: GameState) -> List:
    finished = False
    actions = []
    active.newTurn() 

    while(not(finished)):
        action = decide(active, other, GS)
        if action.type == "attack":
            active.spendActionPoints(action.cost)
            action = attack(active, action.weapon, other, GS)
        elif action.type == "move_closer":
            active.spendActionPoints(1)
            GS.distance = GS.distance - 1
        elif action.type == "move_away":
            active.spendActionPoints(1)
            GS.distance = GS.distance + 1
        elif action.type == "finish":
            finished = True
        actions.append(action)
    return actions

"""Function for handling champion's attack"""
def attack(attacker: Unit, weapon: SpecificWeapon,
           target: Unit, GS: GameState) -> Action:
    hits = 0
    a = Action("attack", weapon.ap_cost)
    dmgs = []
    if(GS.distance > weapon.range):

        return a.attackResolved([Damage(0, 0)])

    for _ in range(attacker.getAtt(weapon.associated)):
        if(randint(0, 1) > 0):
            hits += 1
    if(hits >= target.attA/2):
        for _ in range(weapon.damageInstances):
            dmg = target.damage(weapon.damageNumber)
            dmgs.append(dmg)
    return a.attackResolved(dmgs)

"""Function to preprocess the champions and compile them into a Unit class object."""
def preprocess(character: Champion) -> Unit:
    a = character.pAthletics
    b = character.pBrain
    c = character.pControl
    h = character.pHealth

    shield = getShields(champion=character)
    armour = getArmour(champion=character)
    glory = getGlory(champion=character)

    u = Unit(a, b, c, h, shield, armour, glory)

    configData = json.load(open("config.json"))
    damage = configData["unarmedWeapon"]['damage']
    damageInstances = configData["unarmedWeapon"]['damageInstances']
    range = configData["unarmedWeapon"]['range']
    association = configData["unarmedWeapon"]['association']
    apCost = configData["unarmedWeapon"]['apCost']

    if character.primaryWeapon is None:
        u.setPrimaryWeapon(createNewSpecificItem(createNewBaseWeapon("Unarmed", "weapon", damage, damageInstances, range, association, apCost, Resource.objects.get(name="Books"), 1), 0, 0))
        return u

    u.setPrimaryWeapon(character.primaryWeapon)

    return u
