import streamlit as st
import numpy as np
import pandas as pd
import numpy as np
import sgm_stat as sgm

def page_damageCal():

    # Data generation
    fighterName = ['A', 'B', 'C', 'D']
    z = st.selectbox('Choose a fighter: ', fighterName, key='fighterSelector')

    F = sgm.Fighter()
    D = sgm.Fighter()
    moveSet = sgm.MoveStatistics()
    buffManage = sgm.BuffStatistics()

    dc =  sgm.DamageCalculator(F, D, moveSet, buffManage)

    # layout

    # side bar 
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # main page
    ploter,tunes = st.columns([3,1])

    # plotting part
    with ploter:
        chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

        st.line_chart(chart_data)

    # tune options
    with tunes:
        st.selectbox("Choose a Character", )
        st.slider()



    #x = st.slider("")
    #y = st.button('x',on_click=)

    




pageName = sgm.DamageCalculator.__name__
st.set_page_config(page_title=pageName, page_icon="")

st.markdown(f"# {pageName}")
st.sidebar.header(pageName)
# st.write(
#     """SGM fighter Stat-damage Curve generator"""
# )

page_damageCal()