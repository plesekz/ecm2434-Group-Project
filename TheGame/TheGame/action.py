from typing import List
from TheGame.models import SpecificWeapon
from TheGame.unit import Damage


class Action:
    type = None
    cost = None
    dmg_dealt = None
    weapon = None

    def __init__(self, type: str, cost: int, weapon: SpecificWeapon) -> None:
        pass
        self.type = type
        self.cost = cost
        self.weapon = weapon

    def attackResolved(self, dmg_dealt: List[Damage]):
        self.type = "attack"
        self.dmg_dealt = dmg_dealt
        return self
