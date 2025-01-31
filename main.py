import streamlit as st

# Ustawienie tytułu strony
st.set_page_config(page_title="Analiza sukcesu reklamy bankowej", layout="wide")

# Stworzenie podstron
pages = {
    "Analiza sukcesu reklamy bankowej": [
        st.Page("raw_data.py", title="Surowe dane"),
        st.Page("analysis.py", title="Analiza zbioru"),
        st.Page("processing.py", title="Przetwarzanie danych"),
        st.Page("models.py", title="Modele"),
    ],
    "Spróbuj sam!": [
        st.Page("demo.py", title="Model predykcyjny - demo"),
    ],
}
pg = st.navigation(pages)
pg.run()

# Ustawienie footera
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #CCCCFF;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #333;
        }
    </style>
    <div class="footer">
        Marek Burkot s22403 - projekt końcowy PAD | Created with Streamlit 2025
    </div>
""", unsafe_allow_html=True)
