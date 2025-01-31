import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from import_data import import_df
from scipy.stats import chi2_contingency

st.write("Po przyjrzeniu się danym i określeniu celu (jakim jest zbadanie jakie cechy klienta wpływają na pozytywny"
         " odbiór reklamy telefonicznej) odrzucamy następujące cechy:  \n"
         "1. default - zawiera prawie same wartości nie albo null  \n"
         "2. emp.var.rate/cons.price.idx/cons.conf.idx/euribor3m/nr.employed - dane dot. pracowników/ekonomiczne  \n")
df = import_df()
df.drop(columns=['default', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed'],
        inplace=True)

st.header("Poniżej poddałem niektóre kolumny kategoryczne przekształceniom")
st.write(
    "Edukacja została zmieniona na skalę 0-6 (zgodnie z poziomem szkoły), a wartości brakujące uzupełnione średnią")
education_mapping = {
    'illiterate': 0,
    'basic.4y': 1,
    'basic.6y': 2,
    'basic.9y': 3,
    'high.school': 4,
    'professional.course': 5,
    'university.degree': 6
}
df['education'] = df['education'].map(education_mapping)
df['education'] = df['education'].fillna(df['education'].mean())

st.write("To samo podejście zostało zastosowane dla dni, miesięcy, kredytów oraz zmiennej decyzyjnej"
         " - brak wartości brakujących ")
month_mapping = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
    'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
    'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}
df['month'] = df['month'].map(month_mapping)

day_mapping = {
    'mon': 1, 'tue': 2, 'wed': 3,
    'thu': 4, 'fri': 5
}
df['day_of_week'] = df['day_of_week'].map(day_mapping)

y_mapping = {'no': 0, 'yes': 1}
df['y'] = df['y'].map(y_mapping)

st.header("Tak wygląda dataFrame po odrzuceniu zbędnych kolumn, i wstępnym przetworzeniu przed dalszą analizą")
st.write(df.head(15))

st.write("Z poniższego wykresu możemy odczytać, że najbardziej skorelowanymi cechami są:  \n"
         "1. Czas trwania rozmowy  \n"
         "2. Ilość kontaktów w poprzednich kampaniach  \n"
         "3. Oraz liczba dni od ostatniego kontaktu - co należy dalej przeanalizować")

numeric_columns = df.select_dtypes(include=[np.number]).columns
correlation_matrix = df[numeric_columns].corr()

st.plotly_chart(px.imshow(correlation_matrix, color_continuous_scale="RdBu_r",
                          text_auto=True, height=1000, width=1000))

st.write("Bezpośrednim wnioskiem jaki można wyciągnąć, to czym dłuższa rozmowa tym częściej uda się przekonać klienta")
st.plotly_chart(px.histogram(df, x='duration', color='y', histnorm='probability density',
                             barmode='overlay',
                             title='Rozkład długości trwania rozmowy z '
                                   'podziałem na sukces reklamy (gęstość prawdopodobieństwa)',
                             labels={'duration': 'Długość trwania rozmowy', 'y': 'Sukces reklamy'},
                             ))

st.write("Poniżej możemy zaobserować, że sukcesy cechują się zdecydowanie dłuższym średnim czasem rozmów")
st.plotly_chart(px.box(df, x='duration', color='y',
                       title='Wykresy pudełkowe, dla sukcesu (czerwony) oraz porażki (niebieski) reklamy',
                       labels={'duration': 'Długość trwania rozmowy', 'y': 'Sukces reklamy'},
                       color_discrete_map={0: '#636EFA', 1: '#EF553B'}))

st.write("Wniosek z poniższego wykresu jest prosty, większa ilość kontaktów wpływa na odsetek sukcesu reklamy  \n"
         "warto jednak odnotować, że ponad 86% klientów nie uświadczyło wcześniejszych połączeń")
success_rate = df.groupby('previous')['y'].mean().reset_index()

st.plotly_chart(px.bar(
    success_rate,
    x='previous',
    y='y',
    title='Zależność sukcesu reklamy od liczby kontaktów w poprzednich kampaniach',
    labels={'previous': 'Liczba poprzednich kontaktów', 'y': 'Odsetek sukcesów'},
))

st.write("Z kolumną pdays występują poniższe problemy:  \n"
         "1. Dla znaczącej większości występuje wartość 999 oznaczająca tak naprawdę null  \n"
         "2. Jest mocno skorelowana z previous w sposób naturalny, jednak dla nas problematyczny  \n"
         "Po analizie postanowiłem usunąć tą kolumnę.")

st.plotly_chart(px.pie(df, names='pdays', title='Kiedy wystąpił ostatni kontakt?',
                       color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.3))

columns_to_analyze = ['job', 'marital', 'contact', 'poutcome']
col1, col2, col3, col4 = st.columns(4)

for i, column in enumerate(columns_to_analyze):
    with [col1, col2, col3, col4][i % 4]:
        cross_tab = pd.crosstab(df[column], df['y'])
        st.write(f"**Tabela krzyżowa dla {column} vs y:**")
        st.write(cross_tab)

        chi2, p, _, _ = chi2_contingency(cross_tab)
        st.write(f"**Statystyka chi-kwadrat:** {chi2}")
        st.write(f"**Wartość p:** {p}")

st.write("Wszystkie powyższe p są bardzo niskie, co oznacza zależność ze zmienną decyzyjną")
st.write("Chi2 jest dość wysokie dla job i contact, bardzo wysokie dla poutcome i dość niskie dla marital. "
         "Czym większe chi2 tym większa zależność.")
st.write("1. Studenci byli częściej zainteresowani ofertą bankową, niż pozostałe zawody "
"- ale może to wynikać z małej grupy badaweczej")
st.write("2. Single byli częściej zainteresowani ofertą lokaty bankowej niż pozostałe grupy")
st.write("3. Marketing kierowany na telefony komórkowy był skuteczniejszy niż na telefony stacjonarne")
st.write("4. W przypadku sukcesu wcześniejszych reklam bankowych, aż 2x częściej udało uzyskać się go ponownie")
df.drop(columns=['pdays'], inplace=True)

st.write("Dodatkowo obetniemy część wartości odstających w kolumnie campaign "
         "do usunięcia zostało oznaczone 0.5% rekordów z największą ilością kontaktów "
         "powodem jest bardzo niski współczynik sukcesu w tej grupie czyli 1/186")
quantile_995 = df['campaign'].quantile(0.995)
filtered_df = df[df['campaign'] >= quantile_995]
st.plotly_chart(px.histogram(filtered_df, x='campaign', color='y', barmode='group',
                             title='Liczba porażek i sukcesów reklamy w największym 0.5% w aktualnej kampanii',
                             labels={'campaign': 'Liczba kontaktów w tej kampanii', 'y': 'Sukces reklamy',
                                     'count': 'Liczba'},
                             color_discrete_map={0: '#636EFA', 1: '#EF553B'}))
df = df[df['campaign'] <= quantile_995]

st.write("Przetworzone już wstępnie dane zapisujemy do dalszej analizy")
df.to_csv('data/01_analyze.csv', index=False)
