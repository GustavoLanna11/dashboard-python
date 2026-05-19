import streamlit as st
import pandas as pd
import requests
import os

from src.auth import login
from src.loader import carregar_dados
from src.graph import grafico_barras, grafico_pizza
from src.layout import titulo_principal, filtro_departamento, mostrar_kpis

# ==========================
# 🔐 CONTROLE DE LOGIN
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ==========================
# 🚪 LOGOUT
# ==========================
if st.sidebar.button("🚪 Sair"):
    st.session_state.logged_in = False
    st.rerun()

# ==========================
# 🔐 CREDENCIAIS API (ENV)
# ==========================
API_URL = "https://api-inventario-wudx.onrender.com/dados"
API_USER = os.environ.get("API_USER")
API_PASSWORD = os.environ.get("API_PASSWORD")

# ==========================
# 📊 DASHBOARD
# ==========================

colunas_esperadas = [
    "Nome da máquina", "Proprietário", "Etiqueta", "Cidade", "Departamento",
    "Unidade Residente", "Marca", "Número de Série", "Tipo", "Modelo",
    "Licença", "Processador", "Troca de máquina", "Tipo de memória", "Pentes",
    "Tamanho", "Armazenamento", "Tipo de armazenamento", "Licença Windows",
    "Troca ou Upgrade", "Prioridade", "Antivírus", "Upgrade?", "Em uso?",
    "Está no AD?", "Observações"
]

def carregar_dados_api():
    try:
        response = requests.get(
            API_URL,
            auth=(API_USER, API_PASSWORD),
            timeout=30
        )

        if response.status_code == 401:
            st.error("🔒 Não autorizado na API. Verifique usuário/senha.")
            return pd.DataFrame(columns=colunas_esperadas)

        response.raise_for_status()
        dados_json = response.json()
        df = pd.DataFrame(dados_json)

        for col in colunas_esperadas:
            if col not in df.columns:
                df[col] = None

        df = df[colunas_esperadas]
        st.success("✅ Dados carregados automaticamente da API!")
        return df

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados da API: {e}")
        return pd.DataFrame(columns=colunas_esperadas)

# 🌐 Layout
titulo_principal()

menu = st.sidebar.selectbox(
    "Selecione uma opção",
    ["São Paulo", "Rio de Janeiro", "Planilha Personalizada", "Dados pela API"]
)

df = pd.DataFrame()
cores = ['#32CD32', '#FF0000', '#F39C12', '#2980B9']

# ==========================
# 🔄 MENU
# ==========================

if menu == "São Paulo":
    st.header("Dashboard São Paulo")
    df = carregar_dados("data/inventario_maquinas_exemplo.csv")

elif menu == "Rio de Janeiro":
    st.header("Dashboard Rio de Janeiro")
    df = carregar_dados("data/inventario_maquinas_exemplo2.csv")
    cores = ['#2980B9', '#F39C12', '#1ABC9C', '#E74C3C']

elif menu == "Planilha Personalizada":
    st.header("📤 Dashboard Personalizado")
    uploaded_file = st.file_uploader("Envie sua planilha (.csv ou .xlsx)", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_temp = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
            else:
                df_temp = pd.read_excel(uploaded_file)

            colunas_faltando = [col for col in colunas_esperadas if col not in df_temp.columns]

            if colunas_faltando:
                st.warning("⚠️ A planilha está faltando as seguintes colunas:")
                st.write("- " + "\n- ".join(colunas_faltando))
                for col in colunas_faltando:
                    df_temp[col] = None
            else:
                st.success("✅ Planilha carregada com sucesso!")

            df = df_temp[colunas_esperadas]

        except Exception as e:
            st.error(f"❌ Erro ao carregar a planilha: {e}")

    else:
        with st.expander("📋 Ver colunas esperadas para o arquivo"):
            st.markdown("Sua planilha precisa conter **exatamente essas colunas**:")
            st.markdown("- " + "\n- ".join(colunas_esperadas))

elif menu == "Dados pela API":
    st.header("📡 Dashboard Automático (dados da API)")

    if st.button("🔄 Atualizar dados"):
        st.rerun()

    df = carregar_dados_api()

# ==========================
# 📊 GRÁFICOS
# ==========================

if not df.empty:

    mostrar_kpis(df)

    if menu == "Dados pela API":

        col1, col2 = st.columns(2)
        with col1:
            grafico_pizza(df, 'Antivírus', "Antivírus", cores)
        with col2:
            grafico_pizza(df, 'Licença Windows', "Licença Windows", cores)

        col3, col4 = st.columns(2)
        with col3:
            grafico_barras(df, 'Tamanho', "Memória RAM", cores)
        with col4:
            grafico_barras(df, 'Tipo', "Tipo de Máquina", cores)

        grafico_pizza(df, 'Tipo de armazenamento', "Disco Rígido", cores)

    else:
        col3, col4, col6 = st.columns(3)
        with col6:
            grafico_pizza(df, 'Antivírus', "Antivírus", cores)
        with col3:
            grafico_pizza(df, 'Licença Windows', "Licença Windows", cores)
        with col4:
            grafico_barras(df, 'Troca de máquina', "Troca de Máquina", cores)

        col2, col5, col1, col7 = st.columns(4)
        with col1:
            grafico_barras(df, 'Tamanho', "Memória RAM", cores)
        with col2:
            grafico_barras(df, 'Tipo', "Tipo de Máquina", cores)
        with col5:
            grafico_pizza(df, 'Upgrade?', "Upgrade?", cores)
        with col7:
            grafico_pizza(df, 'Tipo de armazenamento', "Disco Rígido", cores)

    df_filtrado = filtro_departamento(df)

    csv = df_filtrado.to_csv(index=False, sep=";", encoding="latin1")

    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=csv,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )