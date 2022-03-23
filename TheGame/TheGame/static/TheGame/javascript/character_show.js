function setupCharacter(Class, Weapon) {
    //left character variables
    var Body = document.getElementById("Body");
    var bShield = document.getElementById("BodyShield");
    var Arm = document.getElementById("Arm");
    var aShield = document.getElementById("ArmShield");
    var weapon = document.getElementById("Weapon");
    
    //sets sprites to the correct sprite and size
    Body.style.background = 'url(/static/TheGame/sprites/' + Class + '/body.png)'; //sets image
    Body.style.backgroundSize = '100% 100%';                                  //scales image to the correct size
    bShield.style.background = 'url(/static/TheGame/sprites/' + Class + '/bodyshield.png)';
    bShield.style.backgroundSize = '100% 100%';
    Arm.style.background = 'url(/static/TheGame/sprites/' + Class + '/arm.png)';
    Arm.style.backgroundSize = '100% 100%';
    aShield.style.background = 'url(/static/TheGame/sprites/' + Class + '/armshield.png)';
    aShield.style.backgroundSize = '100% 100%';
    weapon.style.background = 'url(/static/TheGame/sprites/weapons/' + Weapon + '.png)';
    weapon.style.backgroundSize = '100% 100%';
}