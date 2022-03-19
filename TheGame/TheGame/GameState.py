from turtle import distance


class GameState:
    distance = None

    def __init__(self, distance: int):
        self.distance = distance
