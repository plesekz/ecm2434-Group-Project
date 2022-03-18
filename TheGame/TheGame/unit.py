from __future__ import annotations


class Unit:
    attA = None
    attB = None
    attC = None
    attH = None
    shield = None
    armour = None
    vitality = None
    actionPoints = None
    vitality = None
    glory = None

    def __init__(self, a : int, b : int, c : int, h : int, shield : int, armour : int, glory : int):
        self.attA = a
        self.attB = b
        self.attC = c
        self.attH = h
        self.shield = shield
        self.armour = armour
        self.glory = glory

        self.vitality = max([self.attA, self.attB, self.attC])
        self.actionPoints = 0

    def damage(self, dmg: int) -> int:
        if(self.shield-dmg>=0):
            shield = shield - dmg
            return 0
        else:
            dmg = dmg - shield
            shield = 0

        dmg = dmg - self.armour
        if(dmg<1):
            dmg = 1

        if(vitality-dmg>=0):
            vitality = vitality - dmg
            return 0
        else:
            dmg = dmg - vitality
            vitality = 0
            attH = attH - dmg
            return dmg
    def newTurn(self):
        self.actionPoints = max([self.attA, self.attB, self.attC])

    def spendActionPoints(self, ap:int):
        if(self.actionPoints-ap<0):
            raise
        self.actionPoints = self.actionPoints - ap

    def getActionPoints(self) -> int:
        return self.actionPoints

    def getShield(self) -> int:
        return self.shield

    def getVitality(self) -> int:
        return self.attH + self.vitality