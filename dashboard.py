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

# Gráfico de tamanho de memória RAM
with col1:
    df_tamanho_contagem = df['Tamanho'].value_counts().reset_index(name="Quantidade")
    df_tamanho_contagem.columns = ['Tamanho', 'Quantidade']
    
    fig = px.bar(df_tamanho_contagem, x="Tamanho", y="Quantidade", title="Tamanho de Memória Ram", color="Tamanho", text="Quantidade", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32', '#FF0000'])
    fig.update_traces(textposition='outside')

    st.plotly_chart(fig)

# Gráfico de tipo da máquinas
with col2:
    df_tipo_contagem = df['Tipo'].value_counts().reset_index(name="Quantidade")
    df_tipo_contagem.columns = ['Tipo', 'Quantidade']
    
    fig = px.bar(df_tipo_contagem, x="Tipo", y="Quantidade", title="Tipo de Máquinas", color="Tipo", text="Quantidade", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    fig.update_traces(textposition='outside')
    
    st.plotly_chart(fig)

# Gráfico de Licenças Windows
with col3:
    df_licenca_contagem = df['Licença Windows'].value_counts().reset_index(name="Quantidade")
    df_licenca_contagem.columns = ['Licença Windows', 'Quantidade']
    
    fig2 = px.pie(df_licenca_contagem, names="Licença Windows", values="Quantidade", title="Máquinas sem licença",  color="Licença Windows", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    st.plotly_chart(fig2)

# Gráfico para troca de máquinas
with col4:
    df_troca_contagem = df['Troca de máquina'].value_counts().reset_index(name="Quantidade")
    df_troca_contagem.columns = ['Troca de máquina', 'Quantidade']
    
    fig3 = px.bar(df_troca_contagem, x="Troca de máquina", y="Quantidade", title="Máquinas para Troca",color="Troca de máquina", text="Quantidade", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    fig3.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig3)

# Gráfico de máquinas para melhorar
with col5:
    df_upgrade_contagem = df['Upgrade?'].value_counts().reset_index(name="Quantidade")
    df_upgrade_contagem.columns = ['Upgrade?', 'Quantidade']
    
    fig4 = px.pie(df_upgrade_contagem, names="Upgrade?", values="Quantidade", title="Máquinas para Upgrade",color="Upgrade?", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    st.plotly_chart(fig4)

# Gráfico para antivírus
with col6:
    df_antivirus_contagem = df['Antivírus'].value_counts().reset_index(name="Quantidade")
    df_antivirus_contagem.columns = ['Antivírus', 'Quantidade']
    
    fig5 = px.pie(df_antivirus_contagem, names="Antivírus", values="Quantidade", title="Máquinas sem Antivírus",color="Antivírus", color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32'])
    st.plotly_chart(fig5)

# Gráfico para o tipo de disco rígido
with col7:
    df_disco_contagem = df['Tipo de armazenamento'].value_counts().reset_index(name="Quantidade")
    df_disco_contagem.columns = ['Tipo de armazenamento', 'Quantidade']
    
    fig6 = px.pie(df_disco_contagem, 
                  names="Tipo de armazenamento", 
                  values="Quantidade", 
                  title="Tipos de Disco", 
                  color="Tipo de armazenamento", 
                  color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32', '#FF0000'])

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


