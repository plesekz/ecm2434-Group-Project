from random import randint
import TheGame.models
import math

def take_turn(player, target):
    for i in range(0, player.num):
        #take a shot
        roll = randint(1,100)
        if ((player.acc - target.ev) >= roll):
            #hit
            target.hp -= math.ceil((player.num/(target.tg / 100)))
        #print(f"Attack {i} rolled {roll} against {(player.acc - target.ev)}, leaving opponent on {target.hp}")

def check_if_dead(player):
    if (player.hp <= 0):
        return True
    return False 

def battle(player1, player2):
    #to collapse the defensive stats once rather than every time its called
    p1 = Player(player1)
    p2 = Player(player2)
    
    #decides who goes first randomly
    #50% chance p1 goes first, 50% chance p2 goes first
    if (randint(0,1) == 1):
        #player 1's turn
        if check_if_dead(p1):
            return False #if player 2 wins
        take_turn(p1,p2)
    
    #loop forever, breaks out when a player is dead
    while(True):
        #player 2's turn
        if check_if_dead(p2):
            return True #if player 1 wins
        take_turn(p2,p1)
        
        #player 1's turn
        if check_if_dead(p1):
            return False #if player 2 wins
        take_turn(p1,p2)

class Player:
    def __init__(self, pStat):
        self.hp = pStat.pHealth + pStat.aHealth
        self.tg = pStat.pToughness + pStat.aToughness
        self.ev = pStat.pEvasion + pStat.aEvasion
        self.dmg = pStat.damage
        self.acc = pStat.accuracy 
        self.num = pStat.attackSpeed

#temp for testing purposes
#p1 = Player(100, 100, 10, 2, 100, 1, 0, 0, 0)
#p2 = Player(100, 100, 10, 2, 100, 1, 0, 0, 0)
#print(battle(p1, p2))