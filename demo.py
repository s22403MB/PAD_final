import streamlit as st
import pandas as pd
import time
import joblib

# Funkcja do zmiany widoku w streamlicie, w pliku demo.py
def get_predict():
    st.session_state['formVisible'] = False
    progress_text = "Operacja w toku. Proszę czekać."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    st.session_state['resultVisible'] = True

# Funkcja do zmapowania edukacji na wartości liczbowe
def replace_education(value):
    mapping = {
        'illiterate': 0,
        'basic.4y': 1,
        'basic.6y': 2,
        'basic.9y': 3,
        'high.school': 4,
        'professional.course': 5,
        'university.degree': 6
    }
    return mapping.get(value, value)

# Funkcja do predykcji dla przypadku testowego z demo.py
def column_predictions(name, file, query):
    st.write(name)
    model = joblib.load(file)
    result = model.predict(query)[0]

    if result == 0:
        st.markdown(f"Przewidywany wynik reklamy: <span style='color: red;'>Porażka</span>",
                    unsafe_allow_html=True)
        if name == 'SVC':
            probability = model.predict_proba(query)[0] * 100
            st.markdown(f"Przewidywane prawdopodobieństwo.: {round(probability[0], 2)}%</div>", unsafe_allow_html=True)
            return
    else:
        st.markdown(f"Przewidywany wynik reklamy: <span style='color: green;'>Sukces</span>",
                    unsafe_allow_html=True)
        if name == "SVC":
            probability = model.predict_proba(query)[0] * 100
            st.markdown(f"Przewidywane prawdopodobieństwo.: {round(probability[1], 2)}%</div>", unsafe_allow_html=True)
            return

    probability = round(model.predict_proba(query).max() * 100, 2)
    st.markdown(f"Przewidywane prawdopodobieństwo.: {probability}%</div>", unsafe_allow_html=True)

# Funkcja do predykcji dla przypadku testowego z demo.py używająca VotingClassifiera
def final_prediction(file, query):
    main_model = joblib.load(file)
    result = main_model.predict(query)[0]
    if result == 0:
        st.markdown(f"<div align='center'><b>Ostateczny wynik reklamy: <span style='color: red;'>"
                    f"Porażka</span></b></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div align='center'><b>Ostateczny wynik reklamy: <span style='color: green;'>"
                    f"Sukces</span></b></div>", unsafe_allow_html=True)
        st.balloons()


if 'formVisible' not in st.session_state:
    st.session_state['formVisible'] = True

if 'resultVisible' not in st.session_state:
    st.session_state['resultVisible'] = False

# Widok startowy z formularzem 
if st.session_state['formVisible']:
    st.markdown("<i><h5>Wykorzystanie algorytmów uczenia maszynowego do analizy skuteczności reklamy bankowej.</h5></i>",
                unsafe_allow_html=True)
    st.session_state['age'] = st.slider("Age:", 15, 120, 15)
    st.session_state['job'] = st.selectbox("Job:", options=["admin.", "blue-collar", "entrepreneur", "housemaid",
                                                            "management", "retired", "self-employed", "services",
                                                            "student", "technician", "unemployed"])
    st.session_state['marital'] = st.selectbox("Marital:", options=["divorced", "married", "single", "widowed"])
    st.session_state['education'] = st.selectbox("Education:",
                                                 options=["illiterate", "basic.4y", "basic.6y", "basic.9y",
                                                          "high.school", "professional.course", "university.degree"])
    st.session_state['month'] = st.slider("Month:", 1, 12, 1)
    st.session_state['day_of_the_week'] = st.slider("Day of the week:", 1, 5, 1)
    st.session_state['housing_loan'] = st.radio("Has housing loan?", options=["no", "yes"], horizontal=True)
    st.session_state['personal_loan'] = st.radio("Has personal loan?", options=["no", "yes"],
                                                 horizontal=True)
    st.session_state['contact_type'] = st.radio("Contact communication type:", options=["cellular", "telephone"],
                                                horizontal=True)
    st.session_state['duration'] = st.number_input("Duration (in seconds):", min_value=1, max_value=5000)
    st.session_state['contacted_before'] = st.radio("Was the client contacted before?", options=["no", "yes"],
                                                    horizontal=True)

    if st.session_state['contacted_before'] == "yes":
        st.session_state['contacts_in_current_campaign'] = st.number_input("Number of contacts performed (in this "
                                                                           "campaign)", step=1, max_value=50)
        st.session_state['contacts_in_previous_campaigns'] = st.number_input("Number of contacts performed (before "
                                                                             "this campaign)", step=1)
        st.session_state['outcome'] = st.radio("Outcome of the previous marketing campaign",
                                               options=["failure", "nonexistent", "success"], horizontal=True)
    else:
        st.session_state['contacts_in_current_campaign'] = 0
        st.session_state['contacts_in_previous_campaigns'] = 0
        st.session_state['outcome'] = "nonexistent"

    sendButton = st.button("Send!", on_click=get_predict)

# Utworzenie query do predykcji, widok końcowy po wypełnieniu formularza
if st.session_state['resultVisible']:
    query = pd.DataFrame({
        'age': [st.session_state['age']],
        'job': [st.session_state['job']],
        'marital': ["divorced" if st.session_state['marital'] == "widowed" else st.session_state['marital']],
        'education': [replace_education(st.session_state['education'])],
        'housing': [st.session_state['housing_loan']],
        'loan': [st.session_state['personal_loan']],
        'contact': [st.session_state['contact_type']],
        'duration': [st.session_state['duration']],
        'month': [st.session_state['month']],
        'day_of_week': [st.session_state['day_of_the_week']],
        'campaign': [st.session_state['contacts_in_current_campaign']],
        'previous': [st.session_state['contacts_in_previous_campaigns']],
        'poutcome': [st.session_state['outcome']],
    })

    col1, col2, col3 = st.columns(3)
    with col1:
        column_predictions("SVC", "models/pip1_model.pkl", query)
    with col2:
        column_predictions('DecisionTreeClassifier', 'models/pip2_model.pkl', query)
    with col3:
        column_predictions('GaussianNB', 'models/pip3_model.pkl', query)

    final_prediction('models/main_model.pkl', query)
    st.info("SVM może wybrać inną odpowiedź niż tą z prawdopodobieństwem większym niż 50% "
            "https://scikit-learn.org/stable/modules/svm.html#scores-probabilities")

    with st.popover("O modelach"):
        st.write("Aby zminimalizować błąd, wdrożono rozwiązanie wykorzystujące "
                 "klaster trzech różnych modeli uczenia maszynowego.")
        st.write("-Maszyna wektorów nośnych (Support Vector Machine, SVM)\n")
        st.write("-Drzewo decyzyjne (Decision Tree)\n")
        st.write("-Klasyfikator naiwny Bayesa (Naive Bayes Classifier)\n")
        st.write("Poprzez zastosowanie klasyfikatora głosującego (VotingClassifier) z metodą twardego głosowania."
                 " To podejście pozwoliło na uzyskanie lepszych wyników niż jakikolwiek z testowanych modeli"
                 " indywidualnie..")
