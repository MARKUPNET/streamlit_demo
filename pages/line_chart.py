import json
import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go

# ページ設定
st.set_page_config(
    page_title='折れ線グラフ',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

# データ
df = {}
data = {}
params = {}
params['chartbox'] = {}
d_rows = None

with open('/Users/first/Site/streamlit/data_dir/sampledata/sattool.json') as f:
    data = json.load(f)
    df_json = pd.DataFrame(data)

# データフレーム生成
def create_dataframe(params):
    for n in range(int(params['elements'])):
        data[n] = df_json[df_json['dno'] == int(456331) ]['data'].values
        # データフレーム
        df[n] = pd.DataFrame(data[n][0])
    return df

# グラフデータ生成
def create_chart(params):
    try:
        # データフレーム生成
        df = create_dataframe(params)
        # データフレーム生成
        d_rows = int(np.ceil(params['elements'] / params['columns']))
        fig = go.Figure().set_subplots(d_rows, params['columns'])
        # 繰り返し
        for n in range(int(params['elements'])):
            # row
            f_row = int(np.ceil(int(n+1) / params['columns'] ))

            # column
            f_col = int(n+1)
            if f_col > params['columns']:
                f_col = int(f_col - params['columns'])

            # add
            fig.add_trace(
                go.Bar(
                    x=df[n]['datetime'].tolist(),
                    y=df[n]['data'].tolist(),
                    name='TITLE_' + str(n)
                ),
                row = f_row,
                col = f_col
            )
        # layout
        fig.update_layout(
            margin = dict(l=60, r=60, t=60, b=60),
            height = 400,
            paper_bgcolor = "rgba(255, 255, 255, 0.1)",
            showlegend = True
        )
        return fig
    except:
        print('やっちまったな～～！！')
        raise

# グラフ表示
def view_chart(params):
    fig = create_chart(params)
    st.plotly_chart(fig, use_container_width=True)

#メイン
tab1, tab2, tab3 = st.tabs(['param', 'dataframe', 'visualize'])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        col_1_1, col_1_2 = st.columns(2)
        with col_1_1:
            params['columns'] = st.number_input(
                                    'columns',
                                    min_value=1,
                                    max_value=3,
                                    value=2,
                                    step=1
                                )
        with col_1_2:
            st.empty()
        params['elements'] = st.number_input(
                                'elements',
                                min_value=1,
                                max_value=10,
                                value=2,
                                step=1
                            )
    with col2:
        for n in range(int(params['elements'])):
            with st.container():
                params['chartbox'][n] = st.multiselect(
                                            'ChartBox_' + str(n+1),
                                            [456331, 456728, 454322, 457242], [456331]
                                        )

with tab2:
    df = create_dataframe(params)
    for n in range(int(params['elements'])):
        st.dataframe(df[n])

with tab3:
    # グラフ表示
    view_chart(params)
