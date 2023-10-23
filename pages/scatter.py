import json
import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go

# ページ設定
st.set_page_config(
    page_title='散布図',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

# データ
df = {}
data = {}
params = {}
params['graph_dno'] = {}
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
    # 初期設定
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

        # グラフごとのdno
        dnolist = params['graph_dno']
        
        # 繰り返し
        for n in range(len(dnolist)):
            # チャートごとのデータフレーム生成
            chartDataframe[n] = df_all[dnolist[n]]

        # グラフのベース
        d_rows = int(np.ceil(params['graph_multiple'] / params['columns']))
        fig = go.Figure().set_subplots(d_rows, params['columns'])
        
        # 繰り返し
        for n in range(int(params['graph_multiple'])):

            # row
            f_row = int(np.ceil(int(n+1) / params['columns'] ))

            # column
            f_col = int(n+1)
            if f_col > params['columns']:
                f_col = int(f_col - params['columns'])
            if params['columns'] == 1:
                f_col = 1
            
            # データフレーム
            df = chartDataframe[n]
            df.reset_index(inplace= True)
            df = df.rename(columns={'index': 'datetime'})

            # add
            fig.add_trace(
                go.Scatter(
                    x=df[dnolist[n][0]].tolist(),
                    y=df[dnolist[n][1]].tolist(),
                    mode='markers'
                ),
                row = f_row,
                col = f_col
            )

            # 近似直線
            if approximation:
                xx = df[dnolist[n][0]].tolist()
                yy = df[dnolist[n][1]].tolist()
                # 近似直線の式の　a と b が入ったタプルを得る
                p = np.polyfit(xx, yy, 1)
                
                # 一次関数の式のオブジェクトを生成する
                f = np.poly1d(p)

                fig.add_trace(
                    go.Scatter(
                        x=xx,
                        y=f(xx),
                        mode='lines'
                    ),
                    row = f_row,
                    col = f_col
                )


        # layout
        fig.update_layout(
            margin = dict(l=60, r=60, t=60, b=60),
            height = int(params['height']),
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

# CSV生成
def convert_df(df):
    return df.to_csv().encode('utf-8')

# メイン
tab1, tab2, tab3 = st.tabs(['param', 'dataframe', 'visualize'])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        col_1_1, col_1_2 = st.columns(2)
        with col_1_1:
            # 今日の日付
            today = dt.date.today()
            
            # n日前の日付
            n = 10
            n_days_ago = today - dt.timedelta(days=n)

            params['datetime_start'] = st.date_input('datetime-start', value=n_days_ago)
            params['axis_x'] = st.radio(
                                    'axis-x',
                                    ['月','日','分'],
                                    horizontal=True
                                )
            params['columns'] = st.number_input(
                                    'columns',
                                    min_value=1,
                                    max_value=3,
                                    value=2,
                                    step=1
                                )
            params['graph_multiple'] = st.number_input(
                                    'graph-multiple',
                                    min_value=1,
                                    max_value=10,
                                    value=2,
                                    step=1
                                )
            params['height'] = st.text_input('height', value=400)
        with col_1_2:
            params['datetime_end'] = st.date_input('datetime-end', value=today)
            st.empty()
    with col2:
        for n in range(int(params['graph_multiple'])):
            with st.container():
                params['graph_dno'][n] = st.multiselect(
                                            'Graph_' + str(n+1),
                                            ['456331', '456728', '454322', '457242'], ['456331', '456728'],
                                            max_selections=2
                                        )

with tab2:
    df_all = get_dataframe_all(params)
    dnolist = params['graph_dno']
    for n in range(len(dnolist)):
        df = df_all[dnolist[n]]
        with st.container():
            col_2_1, col_2_2 = st.columns(2)
            with col_2_1:
                st.write('データ ' + str(n+1))
                st.dataframe(df)
            with col_2_2:
                csvfile[n] = convert_df(df)
                st.download_button(label='Data Download(CSV)', 
                                        data=csvfile[n], 
                                        file_name='data_'+str(n+1)+'.csv',
                                        mime='text/csv',
                                    )

with tab3:
    # 近似直線ボタン
    approximation = st.checkbox('近似直線を表示する', value=False, key='approximation')

    # グラフ表示
    view_chart(params)
