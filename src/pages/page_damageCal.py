import streamlit as st
import numpy as np
import pandas as pd
import numpy as np
import sgm_stat as sgm
import copy

def getRandomColor():
    return np.array((np.random.random(), np.random.random(), np.random.random())).reshape(1,-1)

def page_damageCal():

    # statistics api
    fighterStatApi = sgm.FighterStatistics()
    moveStatApi = sgm.MoveStatistics()
    buffManage = sgm.BuffStatistics()

    # main page
    tunes, ploter = st.columns([1,3])

    # tune options
    with tunes:

        ## fighter config
        with st.container():
            st.write("## Fighter configuration ")
            # choose fighter
            fighterName = st.selectbox('Choose a fighter: ', fighterStatApi.getFighterNameList(), index=0, key='fighterSelector')
            F = sgm.Fighter(fighterName, fighterStatApi)

            # choose moves
            tab_moves = st.tabs([f"move{i}" for i in range(1, 6)])
            for index, tab_move in enumerate(tab_moves):
                with tab_move:
                    move = sgm.Move()
                    move_statList = st.multiselect('Choose move stats',sgm.Move.STAT_LIST,default=sgm.Move.STAT_LIST[0:3], key=f'moveStatSelect{index}')
                    if len(move_statList) > 3:
                        move_statList = move_statList[:3]
                    st.header(f"Move{index+1} rerolls")
                    rerollLeft = sgm.Move.MAXLVLTIME
                    st.write(f"Move Level: {sgm.Move.MAXLVLTIME+1 - rerollLeft}")
                    for statIndex, stat  in enumerate(move_statList):
                        # TODO:add textinputer for alternative input
                        if rerollLeft == 0:
                            single_stat_reroll = st.select_slider(stat,[0,0],key=f'move{index}StatReroll{statIndex}')
                        else:
                            single_stat_reroll = st.slider(stat,0,rerollLeft,0,key=f'move{index}StatReroll{statIndex}')
                        rerollLeft -= single_stat_reroll
                        res = move.setStatWithReroll(stat, single_stat_reroll)
                        if res:
                            st.error(res)

                    F.equipMove(move, index)

            F.getStats()
            st.subheader("Fighter Status")
            st.dataframe(pd.DataFrame(F.stat, index=[0]), use_container_width=True)

            ## opponent config
            with st.container():  
                st.write("## Opponent configuration")
                # choose opponent
                opponentName = st.selectbox('Choose an opponent: ', fighterStatApi.getFighterNameList(), index=0, key='opponentSelector')
                D = sgm.Fighter(opponentName, fighterStatApi)
                
                # setup deffense stats
                st.subheader("setup defense stats")
                for stat in sgm.Fighter.STAT_DEF:
                    statValue = st.slider(stat, 0, sgm.Fighter.CAP_STAT[stat], sgm.Fighter.INV_STAT[stat], step=sgm.Move.MOVE_UPGRAGE, key=f'opponent_{stat}_slider')
                    D.setStat(stat, statValue)

        
            ## TODO: buffs config
            ## TODO: modifiers config
    
    dc =  sgm.DamageCalculator(F, D, moveStatApi, buffManage)

    # plotting part
    with ploter:
        chart = st.line_chart()
        # side bar 
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()

        damage = copy.deepcopy(F.BASE_STAT)
        rerolls = 0

        # starter
        for item in damage:
            damage[item] = [dc.damageFormula()]
            chart.add_rows((item[0], rerolls))
        progPerMove = 100/(F.MAX_MOVE_NUMBER)

        # main data generation loop
        for index, move in enumerate(F.moveSet):
            if move != 0:
                if move.rerollTime == 0:
                    perProg = progPerMove*(index+1)
                    status_text.text("%i%% Complete" % perProg)
                    progress_bar.progress(perProg)
                    continue
                else:
                    keys = move.statResult.keys()
                    for i in range(move.rerollTime):
                        perProg = progPerMove*(index+1) +  progPerMove/move.rerollTime*(i+1)
                        status_text.text("%i%% Complete" % perProg)
                        rerolls += 1
                        if len(keys) == 3:
                            for key in keys:
                                F.moveSet[index].setStatWithReroll(key, 1)
                                F.equipMove(F.moveSet[index], index)
                                F.getStats()
                                damage[key] += dc.damageFormula()
                                for item in damage:
                                    chart.add_rows((item[rerolls], rerolls))
                            progress_bar.progress(perProg)
                        else:
                            for key in F.stat.keys():
                                F.moveSet[index].setStatWithReroll(key, 1)
                                F.equipMove(F.moveSet[index], index)
                                F.getStats()
                                damage[key] += dc.damageFormula()
                                for item in damage:
                                    chart.add_rows(( item[rerolls], rerolls))
                            progress_bar.progress(perProg) 
            else:
                for i in range(sgm.Move.MAXLVLTIME):
                    perProg = progPerMove*(index+1) +  progPerMove/sgm.Move.MAXLVLTIME*(i+1)
                    status_text.text("%i%% Complete" % perProg)
                    rerolls += 1
                    for key in F.stat.keys():
                        F.moveSet[index].setStatWithReroll(key, 1)
                        F.equipMove(F.moveSet[index], index)
                        F.getStats()
                        damage[key] += dc.damageFormula()
                        for item in damage:
                            chart.add_rows(( item[rerolls], rerolls))
                    progress_bar.progress(perProg) 
    
    progress_bar.empty()
    #x = st.slider("")
    #y = st.button('x',on_click=)

pageName = sgm.DamageCalculator.__name__
st.set_page_config(page_title=pageName, page_icon="", layout='wide')

st.markdown(f"# {pageName}")
st.sidebar.header(pageName)
# st.write(
#     """SGM fighter Stat-damage Curve generator"""
# )

page_damageCal()