import pandas as pd
import numpy as np
import streamlit as st

st.title('Sample')

df = pd.DataFrame({"datetime": ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01'],
                   "str": ["n1", "n2", 'n3', np.nan, 'n5', 'n6'],
                   "flt": [5.5, 4.2, -1.2, np.nan, np.nan, np.nan],
                   "int": [5, np.nan, 4, 1, np.nan, 3]})

df


# df = df.iloc[:, 2:].fillna(0)

df.fillna(df.iloc[:, 1:].fillna(0), inplace=True)

df

