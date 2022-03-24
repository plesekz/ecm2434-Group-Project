//keeps track of if an animation is playing
var animating = false; 

//keeps track of health and shield values as a percentage
var lhealthleft = 100;
var lshieldleft = 100;
var rhealthleft = 100;
var rshieldleft = 100;


function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

async function leftMelee() {
    //variables
    var character = document.getElementById("leftCharacter");
    var arm = document.getElementById("lArm");
    var shield = document.getElementById("lArmShield");
    var weapon = document.getElementById("lWeapon");
    pos = 2;
    deg = 60;
    
    //waits until no other animations are playing
    while (animating) {
        await sleep(100);
    }
    animating = true;
    
    //move forward
    while (pos < (7)) {
        pos+=(0.25);
        character.style.left = pos + '%';
        await sleep(5);
    }
    
    //ready swing
    while (deg > -40) {
        if (deg < -40) {
            //resets arm position if it goes past
            deg = -39;
        }
        deg-=1;
        arm.style.transform = 'rotate(' + deg + 'deg)';
        shield.style.transform = 'rotate(' + deg + 'deg)';
        weapon.style.transform = 'rotate(' + deg + 'deg)';
        await sleep(5);
    }
    
    //swing
    while (deg < 90) {
        if (deg > 90) {
            //resets arm position if it goes past
            deg = 88;
        }
        deg+=2;
        arm.style.transform = 'rotate(' + deg + 'deg)';
        shield.style.transform = 'rotate(' + deg + 'deg)';
        weapon.style.transform = 'rotate(' + deg + 'deg)';
        await sleep(5);
    }
    
    //return arm to position
    while (deg > 60) {
        if (deg < 60) {
            //resets arm position if it goes past
            deg = 59;
        }
        deg-=1;
        arm.style.transform = 'rotate(' + deg + 'deg)';
        shield.style.transform = 'rotate(' + deg + 'deg)';
        weapon.style.transform = 'rotate(' + deg + 'deg)';
        await sleep(5);
    }
    
    //move back
    while (pos > 2) {
        pos-=0.25;
        character.style.left = pos + '%';
        await sleep(5);
    }
    
    animating = false; //no longer animating
    
    return true; //function has ended
}
async function rightMelee() {
    //variables
    var character = document.getElementById("rightCharacter");
    var arm = document.getElementById("rArm");
    var shield = document.getElementById("rArmShield");
    var weapon = document.getElementById("rWeapon");
    pos = 2;
    deg = 60;
    
    //waits until no other animations are playing
    while (animating) {
        await sleep(40);
    }
    animating = true;
    
    //move forward
    while (pos < 7) {
        pos+=0.25;
        character.style.right = pos + '%';
        await sleep(5);
    }
    
    //ready swing
    while (deg > -40) {
        if (deg < -40) {
            //resets arm position if it goes past
            deg = -39;
        }
        deg-=1;
        arm.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        shield.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        weapon.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        await sleep(5);
    }
    
    //swing
    while (deg < 90) {
        if (deg > 90) {
            //resets arm position if it goes past
            deg = 88;
        }
        deg+=2;
        arm.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        shield.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        weapon.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        await sleep(5);
    }
    
    //return arm to position
    while (deg > 60) {
        if (deg < 60) {
            //resets arm position if it goes past
            deg = 59;
        }
        deg-=1;
        arm.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        shield.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        weapon.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        await sleep(5);
    }
    
    //move back
    while (pos > 2) {
        pos-=0.25;
        character.style.right = pos + '%';
        await sleep(5);
    }
    
    animating = false; //no longer animating
    
    return true; //function ended
}

async function leftRanged() {
    //variables
    var character = document.getElementById("leftCharacter");
    var arm = document.getElementById("lArm");
    var shield = document.getElementById("lArmShield");
    var weapon = document.getElementById("lWeapon");
    pos = 2;
    deg = 60;
    
    //waits until no other animations are playing
    while (animating) {
        await sleep(40);
    }
    animating = true;
    
    while (deg > 45) {
        if (deg < 45) {
            //resets arm position if it goes past
            deg = 45;
        }
        deg-=1;
        arm.style.transform = 'rotate(' + deg + 'deg)';
        shield.style.transform = 'rotate(' + deg + 'deg)';
        weapon.style.transform = 'rotate(' + deg + 'deg)';
        await sleep(15);
    }
    
    
    //recoil
    weapon.style.left = '-55%';
    arm.style.left = '-54.5%';
    shield.style.left = '-54.5%';
    await sleep(100);
    weapon.style.left = '-54.5%';
    arm.style.left = '-54.25%';
    shield.style.left = '-54.25%';
    await sleep(100);
    weapon.style.left = '-54%';
    arm.style.left = '-54.1%';
    shield.style.left = '-54.1%';
    await sleep(100);
    weapon.style.left = '-54%';
    arm.style.left = '-54%';
    shield.style.left = '-54%';
    
    //return to position
    while (deg < 60) {
        if (deg > 60) {
            //resets arm position if it goes past
            deg = 61;
        }
        deg+=1;
        arm.style.transform = 'rotate(' + deg + 'deg)';
        shield.style.transform = 'rotate(' + deg + 'deg)';
        weapon.style.transform = 'rotate(' + deg + 'deg)';
        await sleep(20);
    }
    
    animating = false; //no longer animating
    
    return true; //function ended
}
async function rightRanged() {
    //variables
    var character = document.getElementById("rightCharacter");
    var arm = document.getElementById("rArm");
    var shield = document.getElementById("rArmShield");
    var weapon = document.getElementById("rWeapon");
    pos = 2;
    deg = 60;
    
    //waits until no other animations are playing
    while (animating) {
        await sleep(40);
    }
    animating = true;
    
    while (deg > 45) {
        if (deg < 45) {
            deg = 45;
            //resets arm position if it goes past
        }
        deg-=1;
        arm.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        shield.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        weapon.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        await sleep(15);
    }
    
    
    //recoil
    weapon.style.left = '-55%';
    arm.style.left = '-54.5%';
    shield.style.left = '-54.5%';
    await sleep(100);
    weapon.style.left = '-54.5%';
    arm.style.left = '-54.25%';
    shield.style.left = '-54.25%';
    await sleep(100);
    weapon.style.left = '-54%';
    arm.style.left = '-54.1%';
    shield.style.left = '-54.1%';
    await sleep(100);
    weapon.style.left = '-54%';
    arm.style.left = '-54%';
    shield.style.left = '-54%';
    
    //return to position
    while (deg < 60) {
        if (deg > 60) {
            //resets arm position if it goes past
            deg = 61;
        }
        deg+=1;
        arm.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        shield.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        weapon.style.transform = 'scaleX(-1) rotate(' + deg + 'deg)';
        await sleep(20);
    }
    
    animating = false; //no longer animating
    
    return true; //function ended
}

async function leftTakeHealthDamage(dmg) {
    //waits until no other animations are playing
    while (animating) {
        await sleep(40);
    }
    animating = true;

    var bar = document.getElementById("lHealthFill");
    var current = lhealthleft; //counter
    lhealthleft -= dmg; 
    
    for (var i = current; i>=lhealthleft; i-=0.25) {
        //reduces the health bar gradually
        bar.style.width = i + '%';
        await sleep(1);
    }
    animating = false; //no longer animating
    
    return true; //function ended
}
async function leftTakeShieldDamage(dmg) {
    //waits until no other animations are playing
    while (animating) {
        await sleep(40);
    }
    animating = true;
    
    var bar = document.getElementById("lShieldFill");
    var bodyshield = document.getElementById("lBodyShield");
    var armshield = document.getElementById("lArmShield");
    var current = lshieldleft;
    lshieldleft -= dmg;
    
    for (var i = current; i>=lshieldleft; i-=0.25) {
        //reduces the shield bar and shields opacity gradually
        bar.style.width = i + '%';
        bodyshield.style.opacity = (i/100);
        armshield.style.opacity = (i/100);                
        await sleep(1);
    }
    animating = false; //no longer animating
    
    return true; //function ended
}
async function rightTakeHealthDamage(dmg) {
    //waits until no other animations are playing
    while (animating) {
        await sleep(40);
    }
    animating = true;
    
    var bar = document.getElementById("rHealthFill");
    var current = rhealthleft;
    rhealthleft -= dmg;
    
    for (var i = current; i>=rhealthleft; i-=0.25) {
        //reduces the health bar gradually
        bar.style.width = i + '%';
        await sleep(1);
    }
    animating = false; //no longer animating
    
    return true; //function ended
}
async function rightTakeShieldDamage(dmg) {
    //waits until no other animations are playing
    while (animating) {
        await sleep(40);
    }
    animating = true;
    
    var bar = document.getElementById("rShieldFill");
    var bodyshield = document.getElementById("rBodyShield");
    var armshield = document.getElementById("rArmShield");
    var current = rshieldleft;
    rshieldleft -= dmg;
    
    for (var i = current; i>=rshieldleft; i-=0.25) {
        //reduces the shield bar and shields opacity gradually
        bar.style.width = i + '%';
        bodyshield.style.opacity = (i/100);
        armshield.style.opacity = (i/100);                
        await sleep(1);
    }
    animating = false; //no longer animating
    
    return true; //function ended
}


//assigns sprites to each character based on which class they are and what weapon they are using
function setup(lClass, leftWeapon, rClass, rightWeapon) {
    //left character variables
    var lBody = document.getElementById("lBody");
    var lbShield = document.getElementById("lBodyShield");
    var lArm = document.getElementById("lArm");
    var laShield = document.getElementById("lArmShield");
    var lWeapon = document.getElementById("lWeapon");
    
    //right character variables
    var rBody = document.getElementById("rBody");
    var rbShield = document.getElementById("rBodyShield");
    var rArm = document.getElementById("rArm");
    var raShield = document.getElementById("rArmShield");
    var rWeapon = document.getElementById("rWeapon");
    
    
    //sets sprites to the correct sprite and size
    lBody.style.background = 'url(/static/TheGame/sprites/' + lClass + '/body.png) no-repeat'; //sets image
    lBody.style.backgroundSize = '100% 100%';                                  //scales image to the correct size
    lbShield.style.background = 'url(/static/TheGame/sprites/' + lClass + '/bodyshield.png)';
    lbShield.style.backgroundSize = '100% 100%';
    lArm.style.background = 'url(/static/TheGame/sprites/' + lClass + '/arm.png)';
    lArm.style.backgroundSize = '100% 100%';
    laShield.style.background = 'url(/static/TheGame/sprites/' + lClass + '/armshield.png)';
    laShield.style.backgroundSize = '100% 100%';
    lWeapon.style.background = 'url(/static/TheGame/sprites/weapons/' + leftWeapon + '.png)';
    lWeapon.style.backgroundSize = '100% 100%';
    
    rBody.style.background = 'url(/static/TheGame/sprites/' + rClass + '/body.png) no-repeat';
    rBody.style.backgroundSize = '100% 100%';            
    rbShield.style.background = 'url(/static/TheGame/sprites/' + rClass + '/bodyshield.png)';
    rbShield.style.backgroundSize = '100% 100%';
    rArm.style.background = 'url(/static/TheGame/sprites/' + rClass + '/arm.png)';
    rArm.style.backgroundSize = '100% 100%';
    raShield.style.background = 'url(/static/TheGame/sprites/' + rClass + '/armshield.png)';
    raShield.style.backgroundSize = '100% 100%';
    rWeapon.style.background = 'url(/static/TheGame/sprites/weapons/' + rightWeapon + '.png)';
    rWeapon.style.backgroundSize = '100% 100%';
       
}

async function battle() {
    //currently testing the functions
    await leftTakeHealthDamage(30);
    await leftTakeShieldDamage(40);
    await rightTakeHealthDamage(20);
    await rightTakeShieldDamage(100);
    
    await leftMelee();
    await rightMelee();
    await leftRanged();
    await rightRanged();
    //gets turn order and plays it out
}

var defCurV;
var attCurV;
var defCurS;
var attCurS;
var paused;
var singleStep = false;

async function battleOnList(actionList){
    // alternate side and do the action

    // setting up the battlefield
    let leftTurn = null;
    paused = false;

    if (actionList[0].actor == 'att'){
        leftTurn = true;
    } else {
        leftTurn = false;
    }
    let distance = 10;
    let attMaxV = actionList[0].attVit;
    let defMaxV = actionList[0].defVit;
    let attMaxS = actionList[0].attShi;
    let defMaxS = actionList[0].defShi;

    defCurS = defMaxS;
    defCurV = defMaxV;
    attCurS = attMaxS;
    attCurV = attMaxV;

    // visualise
    if(attMaxS==0){
        leftTakeShieldDamage(100);
    }
    if(defMaxS==0){
        rightTakeShieldDamage(100);
    }
    actionList.shift();
    // set up reporting
    const parent = document.getElementById("combat-log");
    // report on current state of things
    let child = document.createElement('div');
    parent.appendChild(child);
    child.style.borderStyle = "dashed";
    child.classList.add("p-2");
    child.innerHTML = "Combat begins<br>Your shields: "+attMaxS+"<br>Your health: "+attMaxV+"<br>Defender shields: "+defMaxS+"<br>Defender health: "+defMaxV;

    // start alternating
    while(actionList.length !== 0){
        if(paused) {
            sleep(100);
            continue;
        };
        if (actionList[0].type == "attack"){
            if (leftTurn){
                // play either shoot or melee animation
                if(distance == 1){
                    await leftMelee();
                } else {
                    await leftRanged();
                }
                if(actionList[0].dmg_dealt){
                    await actionList[0].dmg_dealt.forEach(element => {
                        rightTakeHealthDamage(100*element.toVit/defMaxV);
                        defCurV-=element.toVit;
                        
                        if(defMaxS>0){
                            rightTakeShieldDamage(100*element.toShi/defMaxS);
                            defCurS-=element.toShi;
                        }
                        console.log(element);
                    });
                }
                let child = document.createElement('div');
                parent.appendChild(child);
                child.style.borderStyle = "dashed";
                child.classList.add("p-2");
                child.innerHTML = "You attack.<br>"+"Defender shields: "+defCurS+"<br>Defender health: "+defCurV;
            } else {
                // play either shoot or melee animation
                if(distance == 1){
                    await rightMelee();
                } else {
                    await rightRanged();
                }
                if(actionList[0].dmg_dealt){
                    await actionList[0].dmg_dealt.forEach(element => {
                        leftTakeHealthDamage(100*element.toVit/attMaxV);
                        attCurV-=element.toVit;
                        if(defMaxS>0){
                            leftTakeShieldDamage(100*element.toShi/attMaxS);
                            attCurS-=element.toShi;
                        }
                        console.log(element);
                    });
                }
                let child = document.createElement('div');
                parent.appendChild(child);
                child.style.borderStyle = "dashed";
                child.classList.add("p-2");
                child.innerHTML = "You are attacked.<br>Your shields: "+attCurS+"<br>Your health: "+attCurV;
            }
        }
        if(actionList[0].type == "move_closer"){
            distance--;
            let child = document.createElement('div');
            parent.appendChild(child);
            child.style.borderStyle = "dashed";
            child.classList.add("p-2");
            if(leftTurn){
                child.innerHTML = "You move closer.<br>Current distance: "+distance;
            } else {
                child.innerHTML = "Enemy moves closer.<br>Current distance: "+distance;
            }
        }
        if(actionList[0].type == "move_away"){
            distance++;
            if(leftTurn){
                child.innerHTML = "You move away.<br>Current distance: "+distance;
            } else {
                child.innerHTML = "Enemy moves away.<br>Current distance: "+distance;
            }
        }
        if(actionList[0].type == "finish"){
            leftTurn = !leftTurn;
        }
        actionList.shift();
        if(singleStep){
            paused = true;
            singleStep = false;
        }
    }

}