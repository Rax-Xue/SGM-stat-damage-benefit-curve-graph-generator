import numpy as np

import streamlit as st
import inspect
import textwrap
import pandas as pd
import altair as alt
import plotly.express as px
import sgm_stat as sgm

# with st.expander('Setup moves'):
#     tab_moves = st.tabs([f"move{i}" for i in range(1, 6)])

#     for index, tab_move in enumerate(tab_moves):
#         with tab_move:
#             move = sgm.Move()
#             move_statList = st.multiselect('Choose move stats',sgm.Move.STAT_LIST,sgm.Move.STAT_LIST[:3], key=f'moveStatSelect{index}')
#             move_statList = move_statList[:3]
#             st.header(f"Move{index+1} rerolls")
#             rerollLeft = sgm.Move.MAXLVLTIME
#             st.write(f"Move Level: {sgm.Move.MAXLVLTIME+1 - rerollLeft}")
#             for statIndex, stat  in enumerate(move_statList):
#                 # TODO:add textinputer for alternative input
#                 if rerollLeft == 0:
#                     single_stat_reroll = st.select_slider(stat,[0,0],key=f'move{index}StatReroll{statIndex}')
#                 else:
#                     single_stat_reroll = st.slider(stat,0,rerollLeft,0,key=f'move{index}StatReroll{statIndex}')
#                 rerollLeft -= single_stat_reroll
#                 res = move.setStatWithReroll(stat, single_stat_reroll)
#                 if res:
#                     st.error(res)

fighterStatApi = sgm.FighterStatistics()
moveStatApi = sgm.MoveStatistics()
buffManage = sgm.BuffStatistics()

fighter = sgm.Fighter('Default',fighterStatApi,2)



# index = 0
# for item, v in stat.items():
#     index  += 1
#     stat[item] = [v, index]

# df = pd.DataFrame(
#     stat)

# fig = px.line(df,
#               markers=True,
#               labels={'index': 'X', 'value': 'Y'})
# st.plotly_chart(fig)

fighter.getStats()
print(fighter.stat)