import joblib
import kagglehub
import pandas as pd

# Metoda do importu danych z kaggle
def import_df():
    path = kagglehub.dataset_download("sahistapatel96/bankadditionalfullcsv")
    df = pd.read_csv(path + '/bank-additional-full.csv', sep=';', na_values='unknown')
    return df

# Metoda do importu danych lokalnych
def import_df_local(path):
    df = pd.read_csv(path)
    return df

# Metoda do importu danych lokalnych przy użyciu jobliba
def import_joblib(path):
    model = joblib.load(path)
    return model
