# Character customisation logic

# Improvement options
The character menu is really just a shop where the user spends their resources to better their character. It will have buttons that "spend" the resources and in exchange improve the character's statistics.

# Character improvement database
This will hold all the characters stats and details for upgrading. It will be updated with the stats from the shop.

# Combat logic
The battle function takes two player IDs as inputs and they take turns to attack until one of them has been killed (reduced to <= 0hp). The player to go first is randomly decided, and in each turn the player attacking rolls to hit against the target a number of times that depends on the weapon, and applies damage depending on the number of hits, also determined by the weapon. The damage is reduced by a percentage, which is the toughness value of the target's armour. The chance to hit is determined by combining the player's weapon's accuracy with the target's evasion. Damage is rounded up upon application so that the minimum damage done per hit is 1.  

The player has base stats equal to the following:  
  -100 hp  
  -0 toughness  
  -10 evasion  
Armour is taken in addition to those stats  
Weapons have the following attributes that vary depending on the individual weapon:  
  -damage per hit  
  -accuracy  
  -number of hits per turn
