import streamlit as st

import streamlit as st

def mostrar_kpis(df):
    total = len(df)

    # Padroniza os valores pra evitar erro com maiúsculas, espaços etc.
    df["Antivírus"] = df["Antivírus"].astype(str).str.strip().str.capitalize()
    df["Licença Windows"] = df["Licença Windows"].astype(str).str.strip().str.capitalize()

    com_antivirus = df["Antivírus"].value_counts().get("Sim", 0)
    com_licenca = df["Licença Windows"].value_counts().get("Sim", 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; text-align:center; background-color:#333; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);">
                <h4 style="margin-bottom:5px; color:white;">💻 Total de Máquinas</h4>
                <h2 style="color:white;">{total}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; text-align:center; background-color:#333; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);">
                <h4 style="margin-bottom:5px; color:white;">🛡️ Com Antivírus</h4>
                <h2 style="color:white;">{com_antivirus}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; text-align:center; background-color:#333; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);">
                <h4 style="margin-bottom:5px; color:white;">🪟 Com Licença Windows</h4>
                <h2 style="color:white;">{com_licenca}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)

def titulo_principal():
    st.set_page_config(layout="wide", page_title="Dashboard de Máquinas", page_icon="🖥️", initial_sidebar_state="expanded")
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