# pip install streamlit
# pip install plotly
# python -m streamlit run dashboard.py - para rodar o projeto localhost

# biblioteca para construir os dashboards
import streamlit as st 

# manipulação de dados no python
import pandas as pd

# construção de gráficos
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("inventario_maquinas_exemplo.csv", sep=";", encoding="ISO-8859-1")
df = pd.read_csv("inventario_maquinas_exemplo.csv", sep=";", encoding="latin1")

# Centralizar o título e criar um divisor
st.markdown("<h1 style='text-align: center;'>Inventário de Máquinas</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Definição da divisão de colunas para aplicação de gráficos
col1 = st.columns(1)
col2, col3, col4, col5 = st.columns(4)

with col2:
    # Contagem das ocorrências por "Tipo" (sem agrupar por "Proprietário")
    df_tipo_contagem = df['Tipo'].value_counts().reset_index(name="Quantidade")
    df_tipo_contagem.columns = ['Tipo', 'Quantidade']
    
    # Criando o gráfico com a contagem
    fig = px.bar(df_tipo_contagem, x="Tipo", y="Quantidade", title="Tipo de Máquinas", color="Tipo", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    fig.update_traces(text=df_tipo_contagem["Quantidade"], textposition='outside')
    
    st.plotly_chart(fig)

with col3:
    # Contagem das ocorrências para "Licença Windows"
    df_licenca_contagem = df['Licença Windows'].value_counts().reset_index(name="Quantidade")
    df_licenca_contagem.columns = ['Licença Windows', 'Quantidade']
    
    fig2 = px.pie(df_licenca_contagem, names="Licença Windows", values="Quantidade", title="Máquinas sem licença",  color="Licença Windows", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    st.plotly_chart(fig2)

with col4:
    # Contagem das ocorrências para "Troca de máquina"
    df_troca_contagem = df['Troca de máquina'].value_counts().reset_index(name="Quantidade")
    df_troca_contagem.columns = ['Troca de máquina', 'Quantidade']
    
    # Criando o gráfico com a contagem
    fig3 = px.bar(df_troca_contagem, x="Troca de máquina", y="Quantidade", title="Máquinas para Troca",color="Troca de máquina", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    fig3.update_traces(text=df_troca_contagem["Quantidade"], textposition='outside')
    st.plotly_chart(fig3)

with col5:
    # Contagem das ocorrências para "Upgrade?"
    df_upgrade_contagem = df['Upgrade?'].value_counts().reset_index(name="Quantidade")
    df_upgrade_contagem.columns = ['Upgrade?', 'Quantidade']
    
    # Criando o gráfico de pizza
    fig4 = px.pie(df_upgrade_contagem, names="Upgrade?", values="Quantidade", title="Máquinas para Upgrade",color="Upgrade?", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    # Exibindo o gráfico
    st.plotly_chart(fig4)

# Filtro por departamento
st.markdown("<hr><h1 style='text-align: center;'>Filtrar por Departamento</h1>", unsafe_allow_html=True)
departamento = df["Departamento"].unique()
filtro_departamento = st.selectbox("", ["Todos"] + list(departamento))

if filtro_departamento != "Todos":
    df_filtrado = df[df["Departamento"] == filtro_departamento]
    st.write(df_filtrado)
else:
    st.write(df)


