from random import randint
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

def battle(p1, p2):
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
    def __init__(self, pHealth, pToughness, pEvasion, damage, accuracy, attackSpeed, aHealth, aToughness, aEvasion):
        self.hp = pHealth + aHealth
        self.tg = pToughness + aToughness
        self.ev = pEvasion + aEvasion
        self.dmg = damage
        self.acc = accuracy 
        self.num = attackSpeed

#temp for testing purposes
#p1 = Player(100, 100, 10, 2, 100, 1, 0, 0, 0)
#p2 = Player(100, 100, 10, 2, 100, 1, 0, 0, 0)
#print(battle(p1, p2))