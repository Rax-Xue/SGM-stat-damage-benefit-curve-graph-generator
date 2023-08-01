### Brief

This damage calculator mainly reveals **the relationship of fighter stat and attack damage**. You can tune fighter setup and opponent setup and generate the damage curve whose x coordinate is `move reroll time`. The more moves fixed the shorter the generated curve. If all move stats are assigned with full `reroll time`, then there will only be 1 point on the graph, indicating the damage. *The basic setup here is **Max level Djinn using her L1 ( ground attack stage 1 ) which is 15591 attack with 15% move scale**, would be replaced by variant selector once database api done*. 

The damage formula using here is: 

`damage = atkDamageWithSaBonus*moveScale*bonus*critExpect*elementEffect*penetration`

For more details, check the source code below.

### Fighter Setup

`Element selector` : choose element for fighter to determine whether fighter is in `element advantage`, `disadvantage` or `neutral`, *would be replaced by variant selector once database api done*

`Move selector`: There are 5 tabs representing 5 `moves` in sgm fighter, each move can add 3 `move stat  ` at most ( **your first 3 selections will be valid if exceeded** ), where you can adjust `move rerolls` whose max time is 14. **Basic move stat without reroll will not be added into calculation unless you select it in the selector**.

### Opponent Setup

`Element selector` : choose element for opponent same in fighter part.

`Defense Stats Sliders`: 4 sliders offering `BLKEFF`, `DEF`, `RESIST`, `CRESIST` tuning for opponent. 

`CRESIST` is subtracted directly from fighter `CRATE` as the sgm game implies. *block efficiency and resistance currently does **nothing**  because damage calculated here is hit damage, and resistance is for buff/ fighter SA mechanism which is not implemented here*. 

### Abbreviation

These stats are all in percentage

| ATK                    | PIERCE     | ACC           | CRATE                    | CDMG             | ELEBONUS        |
| ---------------------- | ---------- | ------------- | ------------------------ | ---------------- | --------------- |
| attack in percentage   | piercing   | accuracy      | critical rate            | critical damage  | element bonus   |
| **HP**                 | **DEF**    | **RESIST**    | **CRESIST**              | **BLKEFF**       | **ELEPENAL**    |
| hp in percentage       | deffense   | resistance    | critical rate resistance | block efficiency | element penalty |
| **SMCD**               | **METER**  | **TAGCD**     |                          |                  |                 |
| special move cool down | meter gain | tag cool down |                          |                  |                 |

