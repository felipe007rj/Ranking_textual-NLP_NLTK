import pandas as pd
import re

def preprocess_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl', header=None)
    df = df.iloc[1:]
    df[0] = df[0].apply(split_except_quotes)
    df = df[0].apply(pd.Series)
    colunas_desejadas = [0, 1, 2, 3, 4, 5, 6, 7]
    df = df[colunas_desejadas]
    df.columns = ['name', 'description', 'employees', 'total_funding', 'city', 'subcountry', 'lat', 'lng']
    df = df.dropna()
    df.to_csv('./data/canada.csv', index=False)
    df.columns = ['name', 'description', 'employees', 'total_funding', 'city', 'subcountry', 'lat', 'lng']
    df_subset = df.iloc[:, [0, 1]]
    df_subset = df_subset.dropna(subset=['description'])
    df_subset.to_csv('./data/frases.csv', index=False)
    return df_subset

def split_except_quotes(text):
    return re.split(r',(?=(?:(?:[^"]*"){2})*[^"]*$)', text)