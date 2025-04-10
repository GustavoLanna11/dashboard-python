import streamlit as st

def titulo_principal():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Inventário de Máquinas</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

def filtro_departamento(df):
    st.markdown("<hr><h1 style='text-align: center;'>Filtrar por Departamento</h1>", unsafe_allow_html=True)
    departamentos = df["Departamento"].unique()
    filtro = st.selectbox("", ["Todos"] + list(departamentos))
    if filtro != "Todos":
        st.write(df[df["Departamento"] == filtro])
    else:
        st.write(df)