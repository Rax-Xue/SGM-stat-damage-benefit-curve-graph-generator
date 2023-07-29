import copy
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
        
class Move():
    MOVE_BASE_6 = 6 # base move stat for atk, hp, blockeff and cresist
    MOVE_BASE_3 = 3
    MOVE_UPGRAGE = 3
    MOVE_UPGRAGE_MIN = -3

    MAXLVLTIME = 14
    STAT_SLOT = 3

    STAT_LIST = ['ATK', 'HP', 'PIERCE', 'ACC', 'ELEBONUS', 'TAGCD', 'BLKEFF', 'CRATE', 'CDMG', 'DEF', 'RESIST', 'ELEPENAL', 'SMCD', 'METER', 'CRESIST']
    STAT_START_WITH_6 = ['ATK', 'HP', 'BLKEFF', 'CRESIST']

    def __init__(self) -> None:
        self.stat_slot = 0
        self.stat = {f'empty{k}' : 0 for k in range(self.STAT_SLOT)}
        self.statResult = dict()
        self.rerollTime = copy.deepcopy(self.MAXLVLTIME)

    def addStat(self, stat:str):
        if stat not in self.STAT_LIST:
            return f"{stat} not in stat list, abort"

        for k in self.stat:
            if k == stat:
                return f"repeated stat{stat} adding, abort"

            if 'empty' in k:
                self.stat.pop(k)
                self.stat[stat] = 1
                return
            
        return f"move stat slot full:{self.stat}, unable to add stat:{stat}"

    def setStatWithReroll(self, stat:str, reroll:int):
        self.addStat(stat)
        
        if self.rerollTime - reroll >= 0:
            self.rerollTime -= reroll
            self.stat[stat] = reroll
        else:
            self.stat[stat] = self.rerollTime
            self.rerollTime = 0
            return "move lvl maxed, unable to add reroll"

    def getMoveStat(self):
        self.statResult = copy.deepcopy(self.stat)
        for k in list(self.statResult.keys()):
            if 'empty' in k:
                self.statResult.pop(k)
                continue

            if k in self.STAT_START_WITH_6:
                self.statResult[k] = self.statResult[k]*self.MOVE_UPGRAGE + self.MOVE_BASE_6
            else:
                self.statResult[k] = self.statResult[k]*self.MOVE_UPGRAGE + self.MOVE_BASE_3

        return self.statResult
            

class MoveStatistics():
    def __init__(self) -> None:
        pass

    def getTotalScale(self, name):
        totalScale = 15 # Filia L1
        return totalScale


class FighterStatistics():
    def __init__(self) -> None:
        pass

    def getBasicStat(self, name):
        atk = 15591 # Djinn MAX LVL
        hp = 0
        ele = 'fire'

        # FIXME: get all stats
                
        return atk, hp, ele
    
    def getSABonus(self, name):
        sa = 0
        return sa
    def getMABonus(self, name):
        ma = 0
        return ma
    
    def getPABonus(self, name):
        pa = 0
        return pa
    
    def getFighterNameList(self):
        names = list()
        names.append('Default')
        names.append('Djinn')

        return names

        
class Fighter():
    EMPTY_STAT = {'ATK' : 0, 'HP' : 0, 'PIERCE' : 0, 'ACC' : 0, 'ELEBONUS' : 0, 'TAGCD' : 0, 'BLKEFF' :0, 'CRATE' : 0, 'CDMG' : 0, 'DEF' : 0, 'RESIST' : 0, 'ELEPENAL' : 0, 'SMCD' : 0, 'METER' : 0, 'CRESIST' : 0}

    BASE_STAT = {'ATK' : 0, 'HP' : 0, 'PIERCE' : 0, 'ACC' : 0, 'ELEBONUS' : 20, 'TAGCD' : 0, 'BLKEFF' :0, 'CRATE' : 5, 'CDMG' : 20, 'DEF' : 0, 'RESIST' : 0, 'ELEPENAL' : 20, 'SMCD' : 0, 'METER' : 0, 'CRESIST' : 0}

    INV_STAT = {'ATK' : 0, 'HP' : 0, 'PIERCE' : 0, 'ACC' : 0, 'ELEBONUS' : 20, 'TAGCD' : 15, 'BLKEFF' : 15, 'CRATE' : 20, 'CDMG' : 35, 'DEF' : 0, 'RESIST' : 0, 'ELEPENAL' : 20, 'SMCD' : 15, 'METER' : 0, 'CRESIST' : 0}

    CAP_STAT = {'ATK' : np.Infinity, 'HP' : np.Infinity, 'PIERCE' : 50, 'ACC' : 50, 'ELEBONUS' : 50, 'TAGCD' : 50, 'BLKEFF' : 100, 'CRATE' : 100, 'CDMG' : 200, 'DEF' : 50, 'RESIST' : 50, 'ELEPENAL' : 0, 'SMCD' : 50, 'METER' : 100, 'CRESIST' : 100}

    STAT_DEF = ['BLKEFF', 'DEF', 'RESIST', 'CRESIST']

    MAX_MOVE_NUMBER = 5
    def __init__(self,
                 name:str,
                 fighterStatApi:FighterStatistics,
                 stat_type = 1,
                 ) -> None:
        """
        stat_type: initial fighter stat types: 0 - all zeros stat, 1 - base stat, 2 - skill tree invested stat, 3 - cap stat
        """
        self.stat_type = stat_type
        self.stat = copy.deepcopy(self.BASE_STAT)

        self.name = name
        self.fsManage = fighterStatApi
        self.ATK_RAW , self.HP_RAW, self.ELEMENT = self.fsManage.getBasicStat(name)
        self.moveSet = [0 for x in range(5)]

        # # tunable
        # self.ATK_RAW = atk_in_kilo
        # self.move_scale = move_scale
        # self.sa_bouns = sa_bouns
        # self.bonus = bouns
        # self.is_eleAdv = is_eleAdv
        # self.is_dMark = is_dMark

    def equipMove(self, move:Move, index:int):
        if index >= self.MAX_MOVE_NUMBER-1:
            return "exceeded index for move"

        self.moveSet[index] = copy.deepcopy(move)
    
    def getStats(self):
        # move stats sumup
        moveStats = copy.deepcopy(self.EMPTY_STAT)
        for move in self.moveSet:
            if move != 0:
                move.getMoveStat()
                if move.statResult:    
                    for k,v in move.statResult.items():
                        moveStats[k] += v
                else:
                    print("empty move")
        
        # add to fighter stat
        if self.stat_type == 0:
            selfStat = self.EMPTY_STAT
        elif self.stat_type == 1:
            selfStat = self.BASE_STAT
        elif self.stat_type == 2:
            selfStat = self.INV_STAT
        elif self.stat_type == 3:
            selfStat = self.CAP_STAT
        self.stat = dict(Counter(moveStats)+Counter(selfStat))

        # cap stats
        for k,v in self.stat.items():         
            if k != 'ATK' or k != 'HP':
                self.stat[k] = v if v < self.CAP_STAT[k] else self.CAP_STAT[k]                        

    def setStat(self, stat:str, value:int):
        if stat in self.stat:
            self.stat[stat] = value if value < self.CAP_STAT[stat] else self.CAP_STAT[stat] 
        else:
            return f'no stat named{stat}'


class BuffStatistics():
    # debuff
    ARMORBREAK = 20 # all dmg buff
    DEATHMARK = 50 # critical dmg buff and blockeff debuff


    # damage debuff

    BLEED = 1
    HEAVYBLLED = 2
    
    
    # buff
    DEADEYE = 50

    # heal buff
    BARRIER = 10
    REGEN = 1
    HEAVYREGEN = 2

    def __init__(self) -> None:
        self.buff = list()
        self.healBuff = list()
        self.debuff = list()
        self.damageDebuff = list()
        pass

    def applyDeadEye(self, fighter_stat:Fighter, opponent_stat:Fighter):
        opponent_stat

    def applyDeathMark(self, fighter_stat:Fighter, opponent_stat:Fighter):
        opponent_stat


def elementCalculator(ele_fighter, ele_opponent):
    ELEMENT_LIST = {'fire' : 1000, 'wind' : 1010, 'water' : 1020, 'light' : 1, 'dark' : -1, 'neutral' : 0}
    
    f = ELEMENT_LIST.get(ele_fighter)
    p = ELEMENT_LIST.get(ele_opponent)
    if f == 0 or p == 0:
        return 0  # one is neutral
    if f+p == 0:
        return 1  # dark-light pair
    elif f-p == -10 or f-p == 20:
        return 1 # advange loop in triple
    elif f-p == 10 or f-p == -20:
        return -1 # the reverse in triple
    else:
        return 0


class DamageCalculator():
    BAD_FORMULA_FIGHTER_LIST = ['Flytrap', 'Jaw Breaker', 'Purrminator']  # whose sa apply on base atk only

    def __init__(self, 
                 fighter:Fighter,
                 opponent:Fighter,
                 moveManage:MoveStatistics,
                 buffManage:BuffStatistics) -> None:
        self.fighter = fighter
        self.opponent = opponent

        self.moveManage = moveManage
        self.buffManage = buffManage

        self.damage = 0

    def damageFormula(self):
        F = self.fighter
        D = self.opponent
        if F.name in self.BAD_FORMULA_FIGHTER_LIST:
            atkDamageWithSaBonus = F.ATK_RAW*(F.fsManage.getSABonus(F.name)+100)/100.0 + F.stat['ATK']/100.0*F.ATK_RAW
        else:
            atkDamageWithSaBonus = F.ATK_RAW*(F.stat['ATK'] + 100)/100.0*(F.fsManage.getSABonus(F.name) + 100)/100.0

        moveScale = self.moveManage.getTotalScale(F.name)
        bonus = 100/100.0 #FIXME
        
        # crit part
        crate = F.stat['CRATE'] - D.stat['CRESIST']
        crate = crate/100.0 if crate > 0 else 0.0
        cdmg = (F.stat['CDMG']+100 )/100.0*(1.5 if 'DMARK' in self.buffManage.buff else 1)  #FIXME: death mark application place?
        critExpect = (1-crate) + crate*cdmg
        
        # element part
        ele_adv = elementCalculator(F.ELEMENT, D.ELEMENT)
        elementEffect = ele_adv*(F.stat['ELEBONUS'] + 100)/100.0 if ele_adv > 0 else (100-F.stat['ELEPENAL'])/100.0
        elementEffect = elementEffect if ele_adv != 0 else 1.0

        # defense part
        penetration = F.stat['PIERCE'] - D.stat['DEF']
        penetration = penetration if penetration < 0 else 0
       
        penetration = (100 + penetration)/100.0 if 'DEADEYE' in self.buffManage.buff else 1.0 

        # damage formula
        self.damage = atkDamageWithSaBonus*moveScale*bonus*critExpect*elementEffect*penetration

        return self.damage
