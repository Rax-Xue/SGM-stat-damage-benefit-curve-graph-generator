import copy
import numpy as np
import matplotlib.pyplot as plt
        
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
        self.stat = {f'empty{k}' : 1 for k in range(self.STAT_SLOT)}
        self.statResult = dict()
        self.rerollTime = 0

  
    def addStat(self, stat:str):
        if stat not in self.STAT_LIST:
            print(f"{stat} not in stat list, abort")
            return -1

        for k in self.stat:
            if k == stat:
                print(f"repeated stat{stat} adding, abort")
                return -2

            if 'empty' in k:
                self.stat.pop(k)
                self.stat[stat] = 1
                return 0
            
        print(f"move stat slot full:{self.stat}, unable to add stat:{stat}")

    def addReroll(self, stat:str):
        if stat not in self.stat.keys():
            print(f"{stat} not in move stat, abort")
            return -1

        if self.rerollTime >= self.MAXLVLTIME:
            print("move lvl maxed, unable to add reroll")
            return -2
        
        self.rerollTime += 1
        self.stat[stat] += 1


    def getMoveStat(self):
        self.statResult = copy.deepcopy(self.stat)
        for k in self.statResult:
            if 'empty' in k:
                print(f"incomplete set moves detected")

            if k in self.STAT_START_WITH_6:
                self.statResult[k] = self.statResult[k]*self.MOVE_UPGRAGE + self.MOVE_BASE_6
            else:
                self.statResult[k] = self.statResult[k]*self.MOVE_UPGRAGE + self.MOVE_BASE_3

        return self.statResult
            

class MoveStatistics():
    def __init__(self) -> None:
        self.totalScale = 0
        pass


    def getTotalScale(self):

        return self.totalScale


class FighterStatistics():
    def __init__(self) -> None:
        pass

    def getBasicStat(self):
        atk = 0
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
        
class Fighter():

    BASE_STAT = {'ATK' : 0, 'HP' : 0, 'PIERCE' : 0, 'ACC' : 0, 'ELEBONUS' : 20, 'TAGCD' : 0, 'BLKEFF' :0, 'CRATE' : 5, 'CDMG' : 20, 'DEF' : 0, 'RESIST' : 0, 'ELEPENAL' : 20, 'SMCD' : 0, 'METER' : 0, 'CRESIST' : 0}

    INV_STAT = {'ATK' : 0, 'HP' : 0, 'PIERCE' : 0, 'ACC' : 0, 'ELEBONUS' : 20, 'TAGCD' : 15, 'BLKEFF' : 15, 'CRATE' : 20, 'CDMG' : 35, 'DEF' : 0, 'RESIST' : 0, 'ELEPENAL' : 20, 'SMCD' : 15, 'METER' : 0, 'CRESIST' : 0}

    CAP_STAT = {'ATK' : np.Infinity, 'HP' : np.Infinity, 'PIERCE' : 50, 'ACC' : 50, 'ELEBONUS' : 50, 'TAGCD' : 50, 'BLKEFF' : 100, 'CRATE' : 100, 'CDMG' : 200, 'DEF' : 50, 'RESIST' : 50, 'ELEPENAL' : 0, 'SMCD' : 50, 'METER' : 100, 'CRESIST' : 100}

    MAX_MOVE_NUMBER = 5
    def __init__(self,
                 name = 'none',
                 stat_type = 0,
                 ) -> None:
        """
        stat_type: initial fighter stat types: 0 - all zeros stat, 1 - base stat, 2 - skill tree invested stat, 3 - cap stat
        """
        
        self.stat = copy.deepcopy(self.BASE_STAT)
        if stat_type == 0:
            for k in self.stat:
                self.stat[k] = 0
        elif stat_type == 2:
            self.stat = copy.deepcopy(self.INV_STAT)
        elif stat_type == 3:
            self.stat = copy.deepcopy(self.CAP_STAT)

        self.name = name
        self.fsManage = FighterStatistics()
        self.ATK_RAW , self.HP_RAW, self.ELEMENT = self.fsManage.getBasicStat()

        # # tunable
        # self.ATK_RAW = atk_in_kilo
        # self.move_scale = move_scale
        # self.sa_bouns = sa_bouns
        # self.bonus = bouns
        # self.is_eleAdv = is_eleAdv
        # self.is_dMark = is_dMark

    def equipMove(self, move:Move):
        if len(self.moveSet) >= self.MAX_MOVE_NUMBER:
            print("too much moves")

        if move.statResult:
            self.moveSet.append(move)
            for k,v in move.statResult.items():
                if k == 'ATK' or 'HP':
                    self.stat[k] += v
                else:
                    sum = self.stat[k] + v
                    self.stat[k] = sum if sum < self.CAP_STAT[k] else self.CAP_STAT[k]
                    
        else:
            print("incomplete move")

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


    def getBuffBonus(self):
        bonus = 0
        return bonus


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
            atkDamageWithSaBonus = F.ATK_RAW*(F.fsManage.getSABonus()+100)/100.0 + F.stat['ATK']/100.0*F.ATK_RAW
        else:
            atkDamageWithSaBonus = F.ATK_RAW*(F.stat['ATK'] + 100)/100.0*(F.fsManage.getSABonus() + 100)/100.0

        moveScale = self.moveManage.getTotalScale()
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
        damage = atkDamageWithSaBonus*moveScale*bonus*critExpect*elementEffect*penetration

        return damage



def getRandomColor():
    return np.array((np.random.random(), np.random.random(), np.random.random())).reshape(1,-1)

def rerollAssigner( times ):
    basic = MOVE_BASE_STAT()
    assert times in range(0, basic.MAXLVLTIME*basic.MAXMOVE+1), f'too many assigns{times}'

    res = list()
    for i in range(basic.MAXMOVE):
        res.append( basic.MAXLVLTIME if times-basic.MAXLVLTIME>0 else times )
        times -= basic.MAXLVLTIME
        times = times if times > 0 else 0

    #print(res)
    return res

def STAT2DMG(types):
    basic = MOVE_BASE_STAT()
    stat = list()
    dmg = list()
    OPPONENT_DEF = 50
    OPPONENT_CRESIT = 0
    # single stat evaluate
    # # build is: atk
    for i in range(basic.MAXLVLTIME*basic.MAXMOVE+1):
        fighter = Fighter(15591, 75) # Filia Djinn with L1 against test partner
        build = MoveSet_build()
        stat.append(i)
        for j in rerollAssigner(i):
            if types == 'atk':
                build.addMove(atk=j)
            elif types == 'crate':
                build.addMove(crate=j)
            elif types == 'cdmg':
                build.addMove(cdmg=j)
            elif types == 'elebonus':
                fighter.is_eleAdv = 1
                build.addMove(elebouns=j)
            elif types == 'pierce':
                build.addMove(pierce=j)

        fighter.getALL(move_atkP=build.ATK,
                        move_pierce=build.PIERCE,
                        move_crate=build.CRATE,
                        move_cdmg=build.CDMG,
                        move_elebouns=build.ELEBONUS)
        dmg.append(fighter.damageFormulaGood(OPPONENT_DEF, OPPONENT_CRESIT))
    return stat, dmg


if __name__ == '__main__':
    
    # plot
    plt.figure(figsize=(20, 10), dpi=100)

    atk, dmg = STAT2DMG('atk')
    plt.plot(atk, dmg, c='red', label='ATK')
    plt.scatter(atk, dmg, c='red')
    crate, dmg2 = STAT2DMG('crate')
    plt.plot(crate, dmg2, c='blue', label='CRATE')
    plt.scatter(crate, dmg2, c='blue')
    cdmg, dmg3 = STAT2DMG('cdmg')
    plt.plot(cdmg, dmg3, c='purple', label='CDMG')
    plt.scatter(cdmg, dmg3, c='purple')
    elebonus, dmg4 = STAT2DMG('elebonus')
    plt.plot(elebonus, dmg4, c='green', label='ELEMENT_BONUS')
    plt.scatter(elebonus, dmg4, c='green')
    pierce, dmg5 = STAT2DMG('pierce')
    plt.plot(pierce, dmg5, c='orange', label='PIERCE')
    plt.scatter(pierce, dmg5, c='orange')

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("STAT with defense 50% opponent in eleadvantage using D2", fontdict={'size': 16})
    plt.ylabel("DMG", fontdict={'size': 16})
    plt.title("Stat-damage benefit curve", fontdict={'size': 20})
    plt.legend(loc='best')

    # plt.text(x=atk[-1]*1.03, y=dmg[-1]*1.03, # text pos 
    #      s='Max defense opponent', # content
    #      fontdict=dict(fontsize=12, color='black',family='monospace',),
    #      bbox={'facecolor': '#74C476', # fill
    #           'edgecolor':'blue',# outline color
    #            'alpha': 0.5, # transparent
    #            'pad': 0.8,# text to outline distance
    #            #'boxstyle':'sawtooth'
    #           }
         
    #     )
    plt.show()

