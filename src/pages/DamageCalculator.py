import streamlit as st
import numpy as np
import pandas as pd
import copy
import plotly.express as px

import sgm_stat as sgm

def getRandomColor():
    return np.array((np.random.random(), np.random.random(), np.random.random())).reshape(1,-1)

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
            fighterName = st.selectbox('Choose a fighter: ', fighterStatApi.getFighterNameList(), index=0, key='fighterSelector')
            F = sgm.Fighter(fighterName, fighterStatApi)

            # choose moves
            tab_moves = st.tabs([f"move{i}" for i in range(1, 6)])
            for index, tab_move in enumerate(tab_moves):
                with tab_move:
                    move_statList = st.multiselect('Choose move stats',sgm.Move.STAT_LIST, key=f'moveStatSelect{index}')
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
            opponentName = st.selectbox('Choose an opponent: ', fighterStatApi.getFighterNameList(), index=0, key='opponentSelector')
            D = sgm.Fighter(opponentName, fighterStatApi)
            
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
        for item in damage:
            damage[item] = [dc.damageFormula()]
        
        progPerMove = 100/(len(F.EMPTY_STAT))

        # main data generation loop
        for statIndex, key in enumerate(F.stat):
            F.moveSetFake = copy.deepcopy(F.moveSet)
            perProg = int(progPerMove*(statIndex+1))
            status_text.text("%i%% Complete" % perProg)

            for index, move in enumerate(F.moveSetFake):
                if move == 0:
                    F.equipMoveFake(sgm.Move(),index) # add one new move
                    move = F.moveSetFake[index]
                rerollTime = move.rerollTime

                keys = move.getMoveStat().keys()
                if key not in keys:
                    if len(keys) >= 3:
                        continue
                    else:
                        F.moveSetFake[index].stat[key] = 0                    

                for i in range(1, rerollTime+1):
                    if rerollTime != 0:
                        F.moveSetFake[index].stat[key] += 1
                        F.getStatusFake()
                        dmgPoint = dc.damageFormula()
                        damage[key] += [dmgPoint]

            progress_bar.progress(perProg)



        # for index, move in enumerate(F.moveSet):
        #     if move == 0:
        #         rerollTime = sgm.Move.MAXLVLTIME
        #         F.equipMove(sgm.Move(),index) # add one new move
        #         move = F.moveSet[index]
        #     else:
        #         rerollTime = move.rerollTime

        #     keys = move.getMoveStat().keys()

        #     for i in range(1, rerollTime+1):
        #         if rerollTime == 0:
        #             perProg = int(progPerMove*(index+1))
        #             status_text.text("%i%% Complete" % perProg)
        #         else:
        #             perProg = int(progPerMove*index +  progPerMove/rerollTime*i)
        #             status_text.text("%i%% Complete" % perProg)

        #             for key in F.stat.keys():
        #                 if len(keys) == 3 and (key not in keys):
        #                     dmgPoint = None
        #                 else:
        #                     F.moveSetFake[index].stat[key]


        #                     F.moveSet[index].stat[key] = i
        #                     F.equipMove(F.moveSet[index], index)  # replace old with updated move
        #                     dmgPoint = dc.damageFormula()
        #                 damage[key] += [dmgPoint]

        #         progress_bar.progress(perProg)
                
        fig = px.line(
            damage,
            markers=True,
            labels={'index': 'Move Reroll Time', 'value' : 'Damage', 'variable' : 'STATs'},
            height=800
        )

        st.plotly_chart(fig, use_container_width=True)

        F.getStats()
        print(F.stat)
        name, form = st.columns([1,4])
        with name:
            st.subheader("Fighter Status")
        with form:
            st.dataframe(pd.DataFrame(F.stat, index=[0]))

    progress_bar.empty()

pageName = sgm.DamageCalculator.__name__
st.set_page_config(page_title=pageName, page_icon="", layout='wide')

#st.title(f"{pageName}")
st.sidebar.header(pageName)
# st.write(
#     """SGM fighter Stat-damage Curve generator"""
# )

page_damageCalulator()