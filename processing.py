import streamlit as st
from import_data import import_df_local

st.header('Poniżej opiszę wszystkie procesy preprocessingu zastowane dla tego zbioru')
st.write("Szybkie spojrzenie na aktualne dane")
df = import_df_local('data/01_analyze.csv')
st.write(df.head(15))

st.write("Dla kolumn job, marital, housing, loan, contact oraz poutcome zastosujemy OneHotEncoder")
st.write("Dla kolumn age, education, month, day_of_week, duration, campaign oraz previous zastosujemy MinMaxScaler")

st.write("A tak wyglądają dane przeprocesowane do procesu uczenia maszynowego")
df = import_df_local('data/02_processed.csv')
st.write(df.head(15))
