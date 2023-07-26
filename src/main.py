import numpy as np
import matplotlib.pyplot as plt

class BASICSTAT:
    def __init__(self):
        self.PIERCE_BASE = 0
        self.ELEBONUS_BASE = 20
        
        self.CRATE_BASE = 5
        self.CRATE_BASE2 = 20
        self.CDMG_BASE = 20
        self.CDMG_BASE2 = 35

        self.DEF_BASE = 15

        self.PIERCE_CAP = 50
        self.ELEBONUS_CAP = 50
        self.CRATE_CAP = 100
        self.CDMG_CAP = 200

        
class MOVESTAT:
    def __init__(self):
        self.MOVE_BASE_ATK = 6
        self.MOVE_BASE_ELSE = 3
        self.MOVE_UPGRAGE = 3

        self.MAXLVLTIME = 14
        self.MAXMOVE = 5


class Fighter:
    def __init__(self, atk_in_kilo,
                 move_scale = 20,
                 sa_bouns = 100,
                 bouns = 100,
                 is_eleAdv = 0,
                 is_dMark = 0
                 ) -> None:
        self.BASIC = BASICSTAT()
        self.ATK = 0

        self.ATKP = 0
        self.CRATE = 0
        self.CDMG = 0
        self.PIERCE = 0
        self.ELEBOUNS = 0

        # tunable
        self.ATK_RAW = atk_in_kilo
        self.move_scale = move_scale
        self.sa_bouns = sa_bouns
        self.bonus = bouns
        self.is_eleAdv = is_eleAdv
        self.is_dMark = is_dMark

    def getATK(self, move_atkP):
        self.ATKP = move_atkP
        self.ATK = self.ATK_RAW * (self.ATKP+100)/100.0
        return self.ATK

    def getCRATE(self, move_crate):
        sum = move_crate + self.BASIC.CRATE_BASE2
        self.CRATE = sum if sum < self.BASIC.CRATE_CAP else self.BASIC.CRATE_CAP
        return self.CRATE
    
    def getCDMG(self, move_cdmg):
        sum = move_cdmg + self.BASIC.CDMG_BASE2
        self.CDMG = sum if sum < self.BASIC.CDMG_CAP else self.BASIC.CDMG_CAP
        return self.CDMG
    
    def getPIERCE(self, move_pierce):
        self.PIERCE = move_pierce if move_pierce < self.BASIC.PIERCE_CAP else self.BASIC.PIERCE_CAP
        return self.PIERCE
    
    def getELEBOUNS(self, move_elebouns):
        sum = move_elebouns + self.BASIC.ELEBONUS_BASE
        self.ELEBOUNS = sum if sum < self.BASIC.ELEBONUS_CAP else self.BASIC.ELEBONUS_CAP
        return self.ELEBOUNS
    
    def getALL(self, move_atkP,
               move_crate,
               move_cdmg,
               move_pierce,
               move_elebouns):
        
        self.getATK(move_atkP)
        self.getCRATE(move_crate)
        self.getCDMG(move_cdmg)
        self.getPIERCE(move_pierce)
        self.getELEBOUNS(move_elebouns)

    def damageFormulaGood(self, opp_def, opp_cresit):
        # make sure all stats calculated
        DMARK_MTP = 100 # check true stat, and decide if to enable
        dmg = self.ATK*(self.sa_bouns+100)/100.0*self.move_scale/100.0*self.bonus/100.0 
        crate = self.CRATE - opp_cresit  # FIXME: is crit resist decrease crate or cdmg
        crate = crate/100.0 if crate > 0 else 0.0
        dmg = (1-crate)*dmg + crate*(self.CDMG+100)/100.0*dmg  # crit expect dmg
        dmg = dmg if not self.is_dMark else dmg*DMARK_MTP/100.0
        dmg = dmg if not self.is_eleAdv else dmg*(self.ELEBOUNS+100)/100.0  

        # defense FIXME: right? will crit damage be defended too?
        penetration = self.PIERCE - opp_def
        penetration = penetration if penetration < 0 else 0
        dmg = dmg*(100 + penetration)/100.0
        return dmg

    def damageFormulaBad(self, opp_def, opp_cresit):
        # for flytrap, jaw, purrminator
        DMARK_MTP = 100 # check true stat, and decide if to enable
        dmg = (self.ATK_RAW*(self.sa_bouns+100)/100.0+self.ATKP*self.ATK_RAW)*self.move_scale/100.0*self.bonus/100.0
        crate = self.CRATE - opp_cresit  # FIXME: check
        crate = crate/100.0 if crate > 0 else 0.0
        dmg = (1-crate)*dmg + crate*(self.CDMG+100)/100.0*dmg  # crit expect dmg
        dmg = dmg if not self.is_dMark else dmg*DMARK_MTP/100.0
        dmg = dmg if not self.is_eleAdv else dmg*(self.ELEBOUNS+100)/100.0

        # defense FIXME: right? will crit damage be defended too?
        penetration = self.PIERCE - opp_def
        penetration = penetration if penetration < 0 else 0
        dmg = dmg*(100 + penetration)/100.0
        return dmg
    

class Build:
    def __init__(self):
        self.BASICMOVE = MOVESTAT()

        self.ATK = 0
        self.PIERCE = 0
        self.ELEBONUS = 0
        self.CRATE = 0
        self.CDMG = 0
        self.ELSES = 0

        self.moveCount = 0

    def addMove(self,
                atk = 0,
                pierce = 0,
                elebouns = 0,
                crate = 0,
                cdmg = 0):
        valuable = atk + pierce + elebouns + crate + cdmg
        assert valuable <= self.BASICMOVE.MAXLVLTIME, 'wrong move reroll number'
        
        self.moveCount += 1
        assert self.moveCount <= self.BASICMOVE.MAXMOVE, f'too many moves{self.moveCount}'

        self.ATK += atk if atk == 0 else atk*self.BASICMOVE.MOVE_UPGRAGE + self.BASICMOVE.MOVE_BASE_ATK
        self.PIERCE += pierce if pierce == 0 else pierce*self.BASICMOVE.MOVE_UPGRAGE + self.BASICMOVE.MOVE_BASE_ELSE
        self.ELEBONUS += elebouns if elebouns == 0 else elebouns*self.BASICMOVE.MOVE_UPGRAGE + self.BASICMOVE.MOVE_BASE_ELSE
        self.CRATE += crate if crate == 0 else crate*self.BASICMOVE.MOVE_UPGRAGE + self.BASICMOVE.MOVE_BASE_ELSE
        self.CDMG += cdmg if cdmg == 0 else cdmg*self.BASICMOVE.MOVE_UPGRAGE + self.BASICMOVE.MOVE_BASE_ELSE
        self.ELSES += self.BASICMOVE.MAXLVLTIME - valuable

        return self.moveCount

    def printMoveSet(self):
        print(f"MoveSet stats: atk={self.ATK}, pierce={self.PIERCE}, element bonus={self.ELEBONUS}, crit rate:{self.CRATE}, crit damage:{self.CDMG}")


def getRandomColor():
    return np.array((np.random.random(), np.random.random(), np.random.random())).reshape(1,-1)

def rerollAssigner( times ):
    basic = MOVESTAT()
    assert times in range(0, basic.MAXLVLTIME*basic.MAXMOVE+1), f'too many assigns{times}'

    res = list()
    for i in range(basic.MAXMOVE):
        res.append( basic.MAXLVLTIME if times-basic.MAXLVLTIME>0 else times )
        times -= basic.MAXLVLTIME
        times = times if times > 0 else 0

    #print(res)
    return res

def STAT2DMG(types):
    basic = MOVESTAT()
    stat = list()
    dmg = list()
    OPPONENT_DEF = 50
    OPPONENT_CRESIT = 0
    # single stat evaluate
    # # build is: atk
    for i in range(basic.MAXLVLTIME*basic.MAXMOVE+1):
        fighter = Fighter(15591, 75) # Filia Djinn with L1 against test partner
        build = Build()
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

