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
csvfile = {}
chartDataframe = {}

# データ取得
def get_jsondata():
    with open('/Users/first/Site/SampleCode/streamlit_demo/data_dir/sampledata/sattool.json') as f:
        data = json.load(f)
    return data

# dnoリスト取得
def get_dnolist(df_json):
    dno_list = df_json['dno'].tolist()
    return dno_list

# 全データフレーム生成
def get_dataframe_all(params):
    #初期設定
    data_json = {}
    df = {}
    df_all = pd.DataFrame()

    # データ取得
    data = get_jsondata()

    # json → データフレーム
    df_json = pd.DataFrame(data)

    # dnoリスト
    dno_list = df_json['dno'].tolist()

    # 繰り返し
    for n in range(len(dno_list)):
        # データのみを取り出し
        data_json[n] = df_json[df_json['dno'] == dno_list[n]]['data'].values
        # データフレーム
        df[n] = pd.DataFrame(data_json[n][0])
        # インデックス指定
        df[n] = df[n].set_index('datetime')
        # リネーム（data→dno）
        df[n] = df[n].rename(columns={'data': str(dno_list[n])})
        # 結合
        df_all = pd.concat([df_all, df[n]], axis=1)

    return df_all

# グラフデータ生成
def create_chart(params):
    try:

        # 全データフレーム
        df_all = get_dataframe_all(params)

        # チャートごとのdno
        chartboxs = params['chartbox']
        
        # 繰り返し
        for n in range(len(chartboxs)):
            # チャートごとのデータフレーム生成
            chartDataframe[n] = df_all[chartboxs[n]]

        # グラフのベース
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
            
            # データフレーム
            df = chartDataframe[n]
            df.reset_index(inplace= True)
            df = df.rename(columns={'index': 'datetime'})
            
            # 繰り返し
            for dno in chartboxs[n]:
                # add
                fig.add_trace(
                    go.Line(
                        x=df['datetime'].tolist(),
                        y=df[dno].tolist(),
                        name='data_' + str(dno)
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
            params['scale'] = st.radio(
                                    'scale',
                                    ['月','日','分']
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
                                            ['456331', '456728', '454322', '457242'], ['456331']
                                        )

with tab2:
    df_all = get_dataframe_all(params)
    chartboxs = params['chartbox']
    for n in range(len(chartboxs)):
        with st.container():
            col_2_1, col_2_2 = st.columns(2)
            with col_2_1:
                st.write('データ ' + str(n+1))
                st.dataframe(df_all[chartboxs[n]])
            with col_2_2:
                csvfile[n] = ''
                st.download_button(label='Data Download', 
                                        data=csvfile[n], 
                                        file_name='data_'+str(n+1)+'.csv',
                                        mime='text/csv',
                                    )

with tab3:
    # グラフ表示
    view_chart(params)
