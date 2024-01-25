import streamlit as st

st.set_page_config(layout="wide")

DNO_LIST = ['445566', '556677', '112233', '223344', '334455', '667788']

st.session_state['param'] = {
    '445566': True,
    '556677': True,
    '112233': True,
    '223344': False,
    '334455': False,
    '667788': False,
}

dno_current = [{"DNO":['445566', '556677', '112233']},{"DNO":['445566', '556677', '112233']},{"DNO":['445566', '556677', '112233']}]
color_current = [['#f00000','#f00000','#f00000'],['#f00000','#f00000','#f00000'],['#f00000','#f00000','#f00000']]
label_current = [['LABEL_1','LABEL_2','LABEL_3'],['LABEL_1','LABEL_2','LABEL_3'],['LABEL_1','LABEL_2','LABEL_3']]

col1, col2 = st.columns([3,7])
with col1:
    number = st.number_input(
                            'グラフ数',
                            value=len(dno_current),
                            step=1
                            )
with col2:
    check_dno  = [{'DNO':{}} for i in range(number)]
    dno_list   = [[] for i in range(number)]
    color_list = [[] for i in range(number)]
    label_list = [[] for i in range(number)]
    color      = [[] for i in range(number)]
    label      = [[] for i in range(number)]

    for n in range(number):

        col11, col12, col13 = st.columns(3)
        with col11:
            check_dno[n]['DNO']['445566'] = st.checkbox('445566', value=st.session_state['param']['445566'], key='445566'+str(n))
            check_dno[n]['DNO']['556677'] = st.checkbox('556677', value=st.session_state['param']['556677'], key='556677'+str(n))
            check_dno[n]['DNO']['112233'] = st.checkbox('112233', value=st.session_state['param']['112233'], key='112233'+str(n))
            check_dno[n]['DNO']['223344'] = st.checkbox('223344', value=st.session_state['param']['223344'], key='223344'+str(n))
            check_dno[n]['DNO']['334455'] = st.checkbox('334455', value=st.session_state['param']['334455'], key='334455'+str(n))
            check_dno[n]['DNO']['667788'] = st.checkbox('667788', value=st.session_state['param']['667788'], key='667788'+str(n))

            # TODO
            dno_list[n] = list(check_dno[n].keys())

            check_dno_number = list(check_dno[n].values()).count(True)

        with col12:
            for i in range(check_dno_number):
                st.subheader(dno_list[n][i])
                color[n][i] = st.color_picker(
                                        '色',
                                        color_list[i],
                                        key='color_'+str(n)+str(i)
                                        )
                label[n][i] = st.text_input(
                                    'NAME',
                                    label_list[n][i],
                                    key='label_'+str(n)+str(i)
                                    )

        with col13:
            st.write(dno_list)
            st.write(color)
            st.write(label)