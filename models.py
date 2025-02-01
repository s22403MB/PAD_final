import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt
from import_data import import_df_local, import_joblib
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB


# Metoda do stworzenia macierzy pomyłek w ładniejszej formie
def createMetrics(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred, labels=[1, 0])

    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(np.log1p(cm), interpolation='nearest', cmap='Greens')
    ax.set_title('Macierz pomyłek (log)')
    fig.colorbar(im)

    ax.set_xticks([])
    ax.set_yticks([])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if i == 0 and j == 0:
                ax.text(j, i, f'TP={cm[i, j]}', ha="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
            elif i == 0 and j == 1:
                ax.text(j, i, f'FN={cm[i, j]}', ha="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
            elif i == 1 and j == 0:
                ax.text(j, i, f'FP={cm[i, j]}', ha="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
            elif i == 1 and j == 1:
                ax.text(j, i, f'TN={cm[i, j]}', ha="center", color="white" if cm[i, j] > cm.max() / 2 else "black")

    plt.tight_layout()
    st.pyplot(fig)
    st.dataframe(classification_report(y_test, y_pred, output_dict=True))

# Pobranie danych do modeli oraz ich podział na zbiór treningowy i testowy
X = import_df_local('data/02_processed.csv')
Y = import_df_local('data/02a_Y.csv')
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=42)

# Narysowanie 6 macierzy pomyłek oraz metryk w trzecgh kolumnach
st.write("Poniżej porównanie kilku modeli uczenia maszynowego")
models = {
    'DecisionTreeClassifier': DecisionTreeClassifier(max_depth=3, class_weight='balanced', random_state=42),
    'RandomForestClassifier': RandomForestClassifier(),
    'GaussianNB': GaussianNB(),
    'AdaBoostClassifier': AdaBoostClassifier(),
    'GradientBoostingClassifier': GradientBoostingClassifier(),
    'SVC': SVC(class_weight='balanced', random_state=42, probability=True),
}
model_paths = {
    'DecisionTreeClassifier': 'models/testing/DecisionTreeClassifier.pkl',
    'RandomForestClassifier': 'models/testing/RandomForestClassifier.pkl',
    'GaussianNB': 'models/testing/GaussianNB.pkl',
    'AdaBoostClassifier': 'models/testing/AdaBoostClassifier.pkl',
    'GradientBoostingClassifier': 'models/testing/GradientBoostingClassifier.pkl',
    'SVC': 'models/testing/SVC.pkl',
}

col1, col2, col3 = st.columns(3)
for i, (model_name, model) in enumerate(models.items()):
    with [col1, col2, col3][i % 3]:
        st.write(model_name)
        model_path = model_paths[model_name]
        try:
            model = import_joblib(model_path)
        except FileNotFoundError:
            model.fit(X_train, y_train.values.ravel())
            joblib.dump(model, model_path)
        y_pred = model.predict(X_test)
        createMetrics(y_test, y_pred)

# Model końcowy, oraz podsumowanie
col1, col2 = st.columns(2)
with col1:
    st.header("Wybierając modele, które mylą się najrzadziej należałoby wybrać modele 2, 4 i 5.")
    st.header("Jednak jeśli głównym celem eksperymentu byłaby chęć maksymalizacyji zysków firmy należy wybrać te "
              "modele, które najczęściej trafiały w TP, ponieważ pozwoli to zmaksymalizować zyski - dokładając "
              "minimalnie więcej pracy.")
    st.header("W tym celu wybrałem modele 1, 3 i 6 tworząc z nich klaster z głosowaniem twardnym, wyniki po prawo ->")
    st.write("Innymi słowami, za cel zadania przyjąłem maksymalizacje pełności - przy zachowaniu pewnego stopnia "
             "dokładności. ")
with col2:
    st.write("Voting classifier")

    try:
        model = import_joblib('models/testing/VotingClassifier.pkl')
    except FileNotFoundError:
        model = VotingClassifier(
            estimators=[
                ('svc', SVC(class_weight='balanced', kernel='poly', probability=True, random_state=42)),
                ('dtc', DecisionTreeClassifier(max_depth=6, class_weight='balanced', random_state=42)),
                ('gnb', GaussianNB(var_smoothing=1e-7))
            ]
        )
        model.fit(X_train, y_train.values.ravel())
        joblib.dump(model, 'models/testing/VotingClassifier.pkl')
    y_pred = model.predict(X_test)
    createMetrics(y_test, y_pred)

try:
    st.write("Poniżej graficzna reprezentacja sposóbu podejmowania decyzji przez Drzewo Decyzyjne")
    model = import_joblib('models/testing/DecisionTreeClassifier.pkl')
    fig, ax = plt.subplots(figsize=(20, 10))
    class_names = list(map(str, model.classes_))

    plot_tree(model,
              feature_names=X_train.columns,
              class_names=class_names,
              filled=True,
              ax=ax)

    st.pyplot(fig)
finally:
    pass
