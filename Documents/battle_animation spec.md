#Animation Spec

##Functions

###leftMelee()
Parameters: none
Moves the left character 5% of the bounding box closer to the enemy , moves the arm (arm, armshield and weapon) to look like a swing of a weapon, and moves back

###rightMelee()
Parameters: none
Moves the right character 5% of the bounding box closer to the enemy , moves the arm (arm, armshield and weapon) to look like a swing of a weapon, and moves back

###leftRanged()
Parameters: none
Moves the left character's arm (arm, armshield and weapon) up to point the weapon at the enemy, moves it back slightly to replicate the look of recoil, and then returns to original position

###rightRanged()
Parameters: none
Moves the right character's arm (arm, armshield and weapon) up to point the weapon at the enemy, moves it back slightly to replicate the look of recoil, and then returns to original position

###leftTakeHealthDamage(dmg)
Parameters: the amount of damage done to the left character's health as a percentage of the maximum health (as a number without the % symbol, can be decimal)
Smoothly reduces the left character's health bar according to how much damage was done

###rightTakeHealthDamage(dmg)
Parameters: the amount of damage done to the right character's health as a percentage of the maximum health (as a number without the % symbol, can be decimal)
Smoothly reduces the right character's health bar according to how much damage was done

###leftTakeShieldDamage(dmg)
Parameters: the amount of damage done to the left character's shield as a percentage of the maximum shield (as a number without the % symbol, can be decimal)
Smoothly reduces the left character's shield bar according to how much damage was done
Also fades the left character's shield sprite to an opacity equal to what percentage of the shield is remaining

###rightTakeHealthDamage(dmg)
Parameters: the amount of damage done to the right character's shield as a percentage of the maximum shield (as a number without the % symbol, can be decimal)
Smoothly reduces the right character's shield bar according to how much damage was done
Also fades the right character's shield sprite to an opacity equal to what percentage of the shield is remaining



###setup(lClass, lWeapon, rClass, rWeapon)
Parameters: 
    lClass - string of what class the left character is
    lWeapon - string of what weapon the left character uses
    rClass - string of what class the right character is
    rWeapon - string of what weapon the right character uses
Assigns each css element the correct sprite based on class or weapon
Example
    if you were to set up a hacker with a shiv on the left, and ignoring the character on the right:
        you would pass lClass as "hacker" and lWeapon as "shiv"
        the hacker's arm sprite would be in "sprites/hacker/arm.png"
        the weapon would be in "sprites/weapons/shiv.png"
        and so forth for each sprite
    

###battle()
Parameters: the output of battle from root_combat
Takes the list of turns from the backend, and iterates over it, calling the corresponding animation function at each step


##Interface
The placement of where the element is will be where the "<div id="arena">" is, and every div contained within it must be present.
The css must all be there
The javascript must also all be there
Setup() must be called in order to display the sprites
Battle() must be called in order to start playing the battle animation
