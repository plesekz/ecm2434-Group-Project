from typing import List
from TheGame.models import SpecificWeapon
from TheGame.unit import Damage
import json

class Action:
    type = None
    cost = None
    dmg_dealt = None
    weapon = None
    actor = None

    def __init__(self, type: str, cost: int) -> None:
        self.type = type
        self.cost = cost

    def setWeapon(self, weapon: SpecificWeapon):
        self.weapon = weapon

    def attackResolved(self, dmg_dealt: List[Damage]):
        self.type = "attack"
        self.dmg_dealt = dmg_dealt
        return self

    def toJson(self):
        dict = {}
        dict['type'] = self.type
        dict['cost'] = self.cost
        dict['dmg_dealt'] = self.dmg_dealt
        dict['actor'] = self.actor

        return json.dumps(self, default=lambda o: dict)
