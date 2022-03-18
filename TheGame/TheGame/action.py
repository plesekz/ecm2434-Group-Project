from typing import List
from unit import Damage

class Action:
    type = None
    cost = None
    dmg_dealt = None

    def __init__(self, type: str, cost: int) -> None:
        pass
        self.type = type
        self.cost = cost

    def attackResolved(self, dmg_dealt: List[Damage]):
        self.type = "attack"
        self.dmg_dealt = dmg_dealt
        