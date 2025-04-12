import time
import streamlit as st
from src.loader import carregar_dados
from src.graph import grafico_barras, grafico_pizza
from src.layout import titulo_principal, filtro_departamento, mostrar_kpis  


titulo_principal()
menu = st.sidebar.selectbox("Selecione uma região", ["São Paulo", "Rio de Janeiro"])

if menu == "São Paulo":
    st.header("Dashboard São Paulo")
    df = carregar_dados("data/inventario_maquinas_exemplo.csv")
    cores = ['#FF6347', '#4682B4', '#32CD32', '#FF0000']
    mostrar_kpis(df)

elif menu == "Rio de Janeiro":
    st.header("Dashboard Rio de Janeiro")
    df = carregar_dados("data/inventario_maquinas_exemplo2.csv")
    cores = ['#2980B9', '#F39C12', '#1ABC9C', '#E74C3C']
    mostrar_kpis(df)

col3, col4, col6 = st.columns(3)
with col6: grafico_pizza(df, 'Antivírus', "Antivírus", cores)
with col3: grafico_pizza(df, 'Licença Windows', "Licença Windows", cores)
with col4: grafico_barras(df, 'Troca de máquina', "Troca de Máquina", cores)

col2, col5, col1, col7 = st.columns(4)
with col1: grafico_barras(df, 'Tamanho', "Memória RAM", cores)
with col2: grafico_barras(df, 'Tipo', "Tipo de Máquina", cores)
with col5: grafico_pizza(df, 'Upgrade?', "Upgrade?", cores)
with col7: grafico_pizza(df, 'Tipo de armazenamento', "Disco Rígido", cores)

filtro_departamento(df)
