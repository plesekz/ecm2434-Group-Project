from typing import List
from TheGame.models import SpecificWeapon
from TheGame.unit import Damage
import json

class Action:
    type = None
    cost = None
    # attack action property
    dmg_dealt = None
    weapon = None
    # setup action type properties
    actor = None
    attVit = None
    defVit = None
    attShi = None
    defShi = None

    def __init__(self, type: str, cost: int) -> None:
        self.type = type
        self.cost = cost

    def setWeapon(self, weapon: SpecificWeapon):
        self.weapon = weapon

    def attackResolved(self, dmg_dealt: List[Damage]):
        self.type = "attack"
        self.dmg_dealt = dmg_dealt
        return self

    def setup(self, attVit: int, defVit: int, attShi: int, defShi: int):
        pass
        self.attVit = attVit
        self.defVit = defVit
        self.attShi = attShi
        self.defShi = defShi

    def toDict(self):
        dict = {}
        dict['type'] = self.type
        dict['cost'] = self.cost
        if self.dmg_dealt:
            dmg = []
            for di in self.dmg_dealt:
                dmg.append(di.toDict())
            dict['dmg_dealt'] = dmg
        if self.type == "setup":
            dict['actor'] = self.actor
            dict['attVit'] = self.attVit
            dict['defVit'] = self.defVit
            dict['attShi'] = self.attShi
            dict['defShi'] = self.defShi

        return dict
