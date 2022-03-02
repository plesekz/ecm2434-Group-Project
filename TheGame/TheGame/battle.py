from random import randint
from TheGame.processes import getUserFromName
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

def getLocalPlayer(request):
    lps = getUserFromName(request) #localPlayerStats
    localPlayer = Player(lps)
    return localPlayer

def getOpponent(request):
    ops = getUserFromName(request) #This would need to be made to access the PVE database
    oppPlayer = Player(ops)
    return oppPlayer

def callBattle(request):
    battle(getLocalPlayer(request), getOpponent(request))

def battle(player1, player2):
    #to collapse the defensive stats once rather than every time its called
    p1 = Player(player1)
    p2 = Player(player2)
    
    #decides who goes first randomly
    #50% chance p1 goes first, 50% chance p2 goes first
    if (p1.num > p2.num): #I made it so the player with faster attack speed goes first #randint(0,1) == 1):
        #player 1's turn
        if check_if_dead(p1):
            return False #if player 2 wins
        take_turn(p1,p2)
    elif (p1.num == p2.num): #if speed tie,
        if (randint(0,1) == 1): #50% chance of each player going first
            if check_if_dead(p1):
                return False #if player 2 wins
        take_turn(p2,p1)
            
    
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
    def __init__(self, playerStats):
        self.hp = playerStats.pHealth + playerStats.aHealth
        self.tg = playerStats.pToughness + playerStats.aToughness
        self.ev = playerStats.pEvasion + playerStats.aEvasion
        self.dmg = playerStats.damage
        self.acc = playerStats.accuracy 
        self.num = playerStats.attackSpeed

#temp for testing purposes
#p1 = Player(100, 100, 10, 2, 100, 1, 0, 0, 0)
#p2 = Player(100, 100, 10, 2, 100, 1, 0, 0, 0)
#print(battle(p1, p2))