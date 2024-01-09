import pandas as pd
import numpy as np
import streamlit as st

import plotly.figure_factory as ff

st.title('Sample')

df = pd.DataFrame({"number": ['BE2250', 'BE2260', 'BE2270', 'BE2280', 'BE2290', 'BE2300'],
                   "品名": ["商品１", "商品２", '商品３', '商品４', '商品５', '商品６'],
                   "単価": ["200", "210", '220', np.nan, '240', '250'],
                   "2023-01-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-02-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-03-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-04-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-05-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-06-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-07-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-08-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-09-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-10-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-11-01": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "2023-12-01": [5, np.nan, 4, 1, np.nan, 3]})

df

df.fillna(df.iloc[:, 1:].fillna(0), inplace=True)

df

df = df.melt(id_vars=["number", "品名", "単価"], 
               value_vars=["2023-01-01",
                           "2023-02-01",
                           "2023-03-01",
                           "2023-04-01",
                           "2023-05-01",
                           "2023-06-01",
                           "2023-07-01",
                           "2023-08-01",
                           "2023-09-01",
                           "2023-10-01",
                           "2023-11-01",
                           "2023-12-01"],
                           var_name="DATETIME",
                           value_name="Price")

df.set_index("DATETIME",inplace=True)

df

df.query('品名 in ["商品１"]' ,inplace=True)

df_select = df.loc[:, ['Price']]
df_select.rename(columns={'Price': '商品１'} ,inplace=True)



# TEST
list = []
parent = []
txt = "TEST_TEXT"

number = 8
cols = 3

rows = math.floor(np.ceil(number / cols))
remainder = number % cols

for a in range(rows):
    if a == rows - 1:
        list.append(remainder)
    else:
        list.append(cols)

for n in range(len(list)):
    child = []
    for i in range(list[n]):
        child.append(txt)
    parent.append(child)
df_select
st.line_chart(df_select)
