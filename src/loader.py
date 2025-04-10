# Carrega as planilhas
import pandas as pd

def carregar_dados(caminho):
    return pd.read_csv(caminho, sep=";", encoding="latin1")