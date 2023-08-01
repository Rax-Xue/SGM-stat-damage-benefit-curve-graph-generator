import streamlit as st
import numpy as np
import pandas as pd
import copy
import plotly.express as px
from utils import show_code

import sgm_stat as sgm

def getRandomColor():
    return np.array((np.random.random(), np.random.random(), np.random.random())).reshape(1,-1)

def merge_keys_with_same_value(original_dict):
    value_to_keys = {}
    for key, value in original_dict.items():
        value_key = tuple(value)
        if value_key in value_to_keys:
            value_to_keys[value_key].append(key)
        else:
            value_to_keys[value_key] = [key]

    merged_dict = {}
    for value, keys in value_to_keys.items():
        if len(keys) == 1:
            merged_dict[keys[0]] = list(value)
        else:
            merged_dict[",".join(keys)] = list(value)

    return merged_dict

def page_damageCalulator():

    # statistics api
    fighterStatApi = sgm.FighterStatistics()
    moveStatApi = sgm.MoveStatistics()
    buffManage = sgm.BuffStatistics()

    # main page
    tunes, ploter = st.columns([2,5])

    # tune options
    with tunes:
        col1, col2 = st.columns([1,1])
        ## fighter config
        with col1:
            st.write("## Fighter")
            # choose fighter
            # TODO: add later
            #fighterName = st.selectbox('Choose a fighter: ', fighterStatApi.getFighterNameList(), index=0, key='fighterSelector')
            
            # temporary input
            fighterName = "Default"
            fighterElement = st.selectbox('Choose fighter element', sgm.Fighter.ELEMENT_LIST.keys(), index=0, key='fighterElementSelector')
            F = sgm.Fighter(fighterName, fighterStatApi)
            F.ELEMENT = fighterElement

            # choose moves
            tab_moves = st.tabs([f"move{i}" for i in range(1, 6)])
            for index, tab_move in enumerate(tab_moves):
                with tab_move:
                    move_statList = st.multiselect(f'Choose move stats with {sgm.Move.STAT_SLOT} at most',sgm.Move.STAT_LIST, key=f'moveStatSelect{index}')
                    if len(move_statList) > sgm.Move.STAT_SLOT:
                        move_statList = move_statList[:sgm.Move.STAT_SLOT]
                    st.subheader(f"Move{index+1} rerolls")
                    move = sgm.Move()
                    #st.write(f"Move Level: {sgm.Move.MAXLVLTIME+1 - rerollLeft}") #bug
                    
                    for statIndex, stat  in enumerate(move_statList):
                        # TODO:add textinputer for alternative input
                        if move.rerollTime == 0:
                            single_stat_reroll = st.select_slider(stat,[0,0],key=f'move{index}StatReroll{statIndex}')
                        else:
                            single_stat_reroll = st.slider(stat,0,move.rerollTime,0,key=f'move{index}StatReroll{statIndex}')
                        move.rerollTime -= single_stat_reroll
                        move.stat[stat] = single_stat_reroll

                    F.equipMove(move, index) # update move stat

            ## opponent config
        with col2:  
            st.write("## Opponent")
            # choose opponent
            # TODO
            #opponentName = st.selectbox('Choose an opponent: ', fighterStatApi.getFighterNameList(), index=0, key='opponentSelector')
            
            # temporary input
            opponentName = "Default"
            opponentElement = st.selectbox('Choose opponent element', sgm.Fighter.ELEMENT_LIST.keys(), index=0, key='opponentElementSelector')
            D = sgm.Fighter(opponentName, fighterStatApi)
            D.ELEMENT = opponentElement
            
            # setup deffense stats
            st.subheader("Defense Stats")
            for stat in sgm.Fighter.STAT_DEF:
                statValue = st.slider(stat, 0, sgm.Fighter.CAP_STAT[stat], sgm.Fighter.INV_STAT[stat], step=sgm.Move.MOVE_UPGRAGE, key=f'opponent_{stat}_slider')
                D.setStat(stat, statValue)

        
            ## TODO: buffs config
            ## TODO: modifiers config
    
    dc =  sgm.DamageCalculator(F, D, moveStatApi, buffManage)

    # plotting part
    with ploter:
        # side bar 
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()

        damage = copy.deepcopy(F.BASE_STAT)

        # starter
        F.getStats()
        for item in damage:
            damage[item] = [dc.damageFormula()]
        
        progPerMove = 100/(len(F.EMPTY_STAT))

        # main data generation loop
        for statIndex, key in enumerate(F.stat):
            F.moveSetFake = copy.deepcopy(F.moveSet)
            perProg = int(progPerMove*(statIndex+1))
            status_text.text("%i%% Complete" % perProg)

            for index, move in enumerate(F.moveSetFake):
                if move == 0:  # if no new move
                    F.equipMoveFake(sgm.Move(),index) # add one new move
                    move = F.moveSetFake[index]  # replace the move item with the fake one
                rerollTime = move.rerollTime

                keys = move.getMoveStat().keys()                                   

                if key not in keys and len(keys) < 3:
                    F.moveSetFake[index].stat[key] = 0

                for i in range(1, rerollTime+1):
                    if rerollTime != 0:
                        if key not in keys and len(keys) >= 3:
                            dmgPoint = None
                        else:
                            F.moveSetFake[index].stat[key] += 1
                            F.getStatusFake()
                            dmgPoint = dc.damageFormula()
                        damage[key] += [dmgPoint]

            progress_bar.progress(perProg)
                
        # Remove overlapped lines
        mergedDamge = merge_keys_with_same_value(damage)

        fig = px.line(
            mergedDamge,
            markers=True,
            labels={'index': 'Move Reroll Time', 'value' : 'Damage', 'variable' : 'STATs'},
            height=650
        )

        st.plotly_chart(fig, use_container_width=True)

        fighterStat = F.getStats()
        fighterStatATK = dict()
        for item in list(fighterStat.keys()):
            if item in sgm.Fighter.STAT_ATK:
                fighterStatATK[item] = fighterStat.pop(item)

    #print(F.stat)
    name, formATK, formELSE = st.columns([1,2,3])
    with name:
        st.subheader("Fighter Status")
    with formATK:
        st.dataframe(pd.DataFrame(fighterStatATK, index=[0]), column_order=sgm.Fighter.STAT_ATK)
    with formELSE:
        st.dataframe(pd.DataFrame(fighterStat, index=[0]))

    progress_bar.empty()


    with st.expander('See Help'):
        f = open("help_damageCalculator.md")
        content = f.read()
        st.markdown(content)
        st.subheader('Damage Formula Code')
        show_code(sgm.DamageCalculator.damageFormula)



pageName = sgm.DamageCalculator.__name__
st.set_page_config(page_title=pageName, page_icon="", layout='wide')

#st.title(f"{pageName}")
st.sidebar.header(pageName)
# st.write(
#     """SGM fighter Stat-damage Curve generator"""
# )

page_damageCalulator()