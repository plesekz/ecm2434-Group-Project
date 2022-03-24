from __future__ import annotations
from TheGame.models import SpecificWeapon


class Unit:
    attA = None
    attB = None
    attC = None
    attH = None
    range = None
    shield = None
    armour = None
    vitality = None
    actionPoints = None
    vitality = None
    glory = None

    weapon = None

    def __init__(self, a: int, b: int, c: int, h: int,
                 shield: int, armour: int, glory: int):
        self.attA = a
        self.attB = b
        self.attC = c
        self.attH = h
        self.shield = shield
        self.armour = armour
        self.glory = glory

        self.vitality = max([self.attA, self.attB, self.attC])
        self.actionPoints = 0

    def setPrimaryWeapon(self, weapon: SpecificWeapon):
        self.weapon = weapon
        self.range = weapon.range

    def damage(self, dmg: int) -> Damage:
        dmgToShield = 0

        if(self.shield - dmg >= 0):
            self.shield = self.shield - dmg
            return Damage(0, dmg)
        else:
            dmgToShield = self.shield
            dmg = dmg - self.shield
            self.shield = 0

        dmg = dmg - self.armour
        if(dmg < 1):
            dmg = 1

        if(self.vitality - dmg >= 0):
            vitality = vitality - dmg
            return Damage(dmg, dmgToShield)
        else:
            damageToVit = dmg
            dmg = dmg - self.vitality
            self.vitality = 0
            self.attH = self.attH - dmg
            return Damage(damageToVit, dmgToShield)

    def newTurn(self):
        self.actionPoints = max([self.attA, self.attB, self.attC])

    def getAtt(self, c: str):
        if(c == "A"):
            return self.attA
        if(c == "B"):
            return self.attB
        if(c == "C"):
            return self.attC

    def spendActionPoints(self, ap: int):
        if(self.actionPoints - ap < 0):
            raise
        self.actionPoints = self.actionPoints - ap

    def getActionPoints(self) -> int:
        return self.actionPoints

    def getShield(self) -> int:
        return self.shield

    def getVitality(self) -> int:
        return self.attH + self.vitality


class Damage:
    dealtToShields = None
    dealtToVit = None

    def __init__(self, dealtToVit: int, dealtToShields: int):
        self.dealtToShields = dealtToShields
        self.dealtToVit = dealtToVit

    def toDict(self):
        dict = {}
        dict['toShield'] = self.dealtToShields
        dict['toVit'] = self.dealtToVit
        return dict