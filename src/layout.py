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
            <div style="padding:20px; border-radius:10px; text-align:center; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-bottom:5px;">💻 Total de Máquinas</h4>
                <h2 style="color:#333;">{total}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style=" padding:20px; border-radius:10px; text-align:center; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-bottom:5px;">🛡️ Com Antivírus</h4>
                <h2 style="color:#333;">{com_antivirus}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; text-align:center; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-bottom:5px;">🪟 Com Licença Windows</h4>
                <h2 style="color:#333;">{com_licenca}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ➕ Divisor abaixo dos cards
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