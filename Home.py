import pandas as pd
import numpy as np
import streamlit as st
import math

import plotly.figure_factory as ff

st.set_page_config(layout="wide")

dno_current = ['445566', '556677', '112233']

number = st.number_input(
                        'グラフ数',
                        value=len(dno_current),
                        step=1
                        )

dno_list = []
check_dno = {}
dno = {}
color = {}
name = {}


col1, col2, col3 = st.columns(3)
with col1:
    check_dno['445566'] = st.checkbox('445566', value=True, key='445566')
    check_dno['556677'] = st.checkbox('556677', value=True, key='556677')
    check_dno['112233'] = st.checkbox('112233', value=True, key='112233')
    check_dno['223344'] = st.checkbox('223344', value=False, key='223344')
    check_dno['334455'] = st.checkbox('334455', value=False, key='334455')
    check_dno['667788'] = st.checkbox('667788', value=False, key='667788')

    # TODO
    dno_list = list(check_dno.keys())
    print(dno_list)

    check_dno_number = list(check_dno.values()).count(True)
    color_list = [None for i in range(check_dno_number)]
    name_list = ['nothing' for i in range(check_dno_number)]

with col2:
    for i in range(check_dno_number):
        dno[i] = st.text_input(
                            'DNO',
                            dno_list[i],
                            key='dno_'+str(i)
                            )
        color[i] = st.color_picker(
                                '色',
                                color_list[i],
                                key='color_'+str(i)
                                )
        name[i] = st.text_input(
                            'NAME',
                            name_list[i],
                            key='name_'+str(i)
                            )

with col3:
    st.write(dno)
    st.write(color)
    st.write(name)





