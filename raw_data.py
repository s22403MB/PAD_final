import streamlit as st
import plotly.express as px
from import_data import import_df


st.header("Spójrzmy na surowe dane")
df = import_df()
st.write(df.head(15))
st.header("Podgląd na istotne wartości w kolumnach")
# WIEK
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(px.histogram(df, x='age', title='Rozkład wieku',
                                 color_discrete_sequence=['#1122EE'], range_x=[0, 100]))
with col2:
    st.plotly_chart(px.box(df, x='age', title='Wykres pudełkowy dla wieku', color_discrete_sequence=['#EF553B']))

# ZAWOD, STAN CYWILNY, WYKSZTALCENIE
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(px.pie(df, names='job', title='Wykonywany zawód',
                           color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.3))
with col2:
    st.plotly_chart(px.pie(df, names='marital', title='Stan cywilny',
                           color_discrete_sequence=px.colors.qualitative.Bold_r, hole=0.3))
with col3:
    st.plotly_chart(px.pie(df, names='education', title='Wykształcenie',
                           color_discrete_sequence=px.colors.qualitative.Bold, hole=0.3))

# KREDYT, HIPOTEKA, POZYCZKA
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(px.pie(df, names='default', title='Czy ma kredyt?',
                           color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.3))
with col2:
    st.plotly_chart(px.pie(df, names='housing', title='Czy ma kredyt hipoteczny?',
                           color_discrete_sequence=px.colors.qualitative.Bold_r, hole=0.3))
with col3:
    st.plotly_chart(px.pie(df, names='loan', title='Czy ma pożyczkę?',
                           color_discrete_sequence=px.colors.qualitative.Bold, hole=0.3))

# CZAS TRWANIA ROZMOWY
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(px.histogram(df, x='duration',
                                 title='Rozkład czasu trwania rozmowy', color_discrete_sequence=['#1122EE']))
with col2:
    st.plotly_chart(px.box(df, x='duration', title='Wykres pudełkowy dla czasu trwania rozmowy',
                           color_discrete_sequence=['#EF553B']))

# MIESIACE, DNI TYGODNIA, RODZAJ KONTAKTU
col1, col2, col3 = st.columns(3)
with col1:
    monthly_contacts = df.groupby('month')['campaign'].count().reset_index()
    month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    st.plotly_chart(px.bar(monthly_contacts, x='month', y='campaign',
                           title='Ilość połączeń w każdym miesiącu',
                           labels={'campaign': 'Ilość połączeń', 'month': 'Miesiąc'},
                           category_orders={'month': month_order}))
with col2:
    daily_contacts = df.groupby('day_of_week')['campaign'].count().reset_index()
    day_order = ['mon', 'tue', 'wed', 'thu', 'fri']

    st.plotly_chart(px.bar(daily_contacts, x='day_of_week', y='campaign',
                           title='Ilość połączeń w każdym dniu tygodnia',
                           labels={'campaign': 'Ilośc połączeń', 'day_of_week': 'Dzień tygodnia'},
                           category_orders={'day_of_week': day_order}))
with col3:
    st.plotly_chart(px.bar(df, x='contact', title="Rodzaj połączenia telefonicznego"))

# ILOSC POLACZEN W RAMACH KAMPANII
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(px.histogram(df, x='campaign', title="Ilość kontaktów w ramach kampanii",
                                 color_discrete_sequence=['#1122EE']))
with col2:
    st.plotly_chart(px.box(df, x='campaign', title='Wykres pudełkowy dla ilości kontaktów - w ramach kampanii',
                           color_discrete_sequence=['#EF553B']))

# DNI OD OSTATNIEGO KONTAKTU
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(px.histogram(df, x='pdays', title="Ilość dni od ostatniego kontaktu - 999 oznacza brak takiego",
                                 color_discrete_sequence=['#1122EE']))
with col2:
    df_without_999 = df.where(df.pdays < 999)
    st.plotly_chart(px.histogram(df_without_999, x='pdays', title="Ilość dni od ostatniego kontaktu - w skali bez 999",
                                 color_discrete_sequence=['#1122EE']))

# ILOSC KONTAKTOW W POPRZEDNICH KAMPANIACH, ICH REZULTAT, ZMIENNA DECYZYJNA
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(px.histogram(df, x='previous', title="Ilość kontaktów w ramach POPRZEDNICH kampanii",
                                 color_discrete_sequence=['#1122EE']))
with col2:
    st.plotly_chart(px.pie(df, names='poutcome', title='Wynik poprzednich reklam',
                           color_discrete_sequence=px.colors.qualitative.Bold_r, hole=0.3))
with col3:
    st.plotly_chart(px.pie(df, names='y', title='Czy klient został nakłoniony do założenia lokaty?',
                           color_discrete_sequence=px.colors.qualitative.Bold, hole=0.3))
