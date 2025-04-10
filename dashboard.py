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
col3, col4, col6 = st.columns(3)
st.markdown("<hr>", unsafe_allow_html=True)
col2, col5, col1, col7 = st.columns(4)

with col1:
    # Contagem das ocorrências por "Tipo" (sem agrupar por "Proprietário")
    df_tamanho_contagem = df['Tamanho'].value_counts().reset_index(name="Quantidade")
    df_tamanho_contagem.columns = ['Tamanho', 'Quantidade']
    
    # Criando o gráfico com a contagem
    fig = px.bar(df_tamanho_contagem, x="Tamanho", y="Quantidade", title="Tamanho de Memória Ram", color="Tamanho", text="Quantidade", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32', '#FF0000'])
    fig.update_traces(textposition='outside')

    st.plotly_chart(fig)

with col2:
    # Contagem das ocorrências por "Tipo" (sem agrupar por "Proprietário")
    df_tipo_contagem = df['Tipo'].value_counts().reset_index(name="Quantidade")
    df_tipo_contagem.columns = ['Tipo', 'Quantidade']
    
    # Criando o gráfico com a contagem
    fig = px.bar(df_tipo_contagem, x="Tipo", y="Quantidade", title="Tipo de Máquinas", color="Tipo", text="Quantidade", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    fig.update_traces(textposition='outside')
    
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
    fig3 = px.bar(df_troca_contagem, x="Troca de máquina", y="Quantidade", title="Máquinas para Troca",color="Troca de máquina", text="Quantidade", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    fig3.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig3)


with col5:
    # Contagem das ocorrências para "Upgrade?"
    df_upgrade_contagem = df['Upgrade?'].value_counts().reset_index(name="Quantidade")
    df_upgrade_contagem.columns = ['Upgrade?', 'Quantidade']
    
    # Criando o gráfico de pizza
    fig4 = px.pie(df_upgrade_contagem, names="Upgrade?", values="Quantidade", title="Máquinas para Upgrade",color="Upgrade?", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    # Exibindo o gráfico
    st.plotly_chart(fig4)

with col6:
    # Contagem das ocorrências para "Upgrade?"
    df_antivirus_contagem = df['Antivírus'].value_counts().reset_index(name="Quantidade")
    df_antivirus_contagem.columns = ['Antivírus', 'Quantidade']
    
    # Criando o gráfico de pizza
    fig5 = px.pie(df_antivirus_contagem, names="Antivírus", values="Quantidade", title="Máquinas sem Antivírus",color="Antivírus", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    # Exibindo o gráfico
    st.plotly_chart(fig5)

with col7:
    # Contagem das ocorrências para "Tipo de armazenamento"
    df_disco_contagem = df['Tipo de armazenamento'].value_counts().reset_index(name="Quantidade")
    df_disco_contagem.columns = ['Tipo de armazenamento', 'Quantidade']
    
    # Criando o gráfico de torta
    fig6 = px.pie(df_disco_contagem, 
                  names="Tipo de armazenamento", 
                  values="Quantidade", 
                  title="Tipos de Disco", 
                  color="Tipo de armazenamento", 
                  color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32', '#FF0000'])

    # Exibindo o gráfico
    st.plotly_chart(fig6)

# Filtro por departamento
st.markdown("<hr><h1 style='text-align: center;'>Filtrar por Departamento</h1>", unsafe_allow_html=True)
departamento = df["Departamento"].unique()
filtro_departamento = st.selectbox("", ["Todos"] + list(departamento))

if filtro_departamento != "Todos":
    df_filtrado = df[df["Departamento"] == filtro_departamento]
    st.write(df_filtrado)
else:
    st.write(df)


