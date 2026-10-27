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
EDITAR_URL = "https://api-inventario-wudx.onrender.com/editar_maquina"
EXCLUIR_URL = "https://api-inventario-wudx.onrender.com/excluir_maquina"

# NOVO: endpoint das tentativas de cadastro
TENTATIVAS_URL = "https://api-inventario-wudx.onrender.com/tentativas_cadastro"

API_USER = os.environ.get("API_USER")
API_PASSWORD = os.environ.get("API_PASSWORD")

# ==========================
# 📊 DASHBOARD
# ==========================

colunas_esperadas = [
    "Nome da máquina",
    "Proprietário",
    "Etiqueta",
    "Cidade",
    "Departamento",
    "Unidade Residente",
    "Marca",
    "Número de Série",
    "Tipo",
    "Modelo",
    "Licença",
    "Processador",
    "Troca de máquina",
    "Tipo de memória",
    "Pentes",
    "Tamanho",
    "Armazenamento",
    "Tipo de armazenamento",
    "Licença Windows",
    "Troca ou Upgrade",
    "Prioridade",
    "Antivírus",
    "Upgrade?",
    "Em uso?",
    "Está no AD?",
    "Observações"
]

# ==========================
# 📥 CARREGAR DADOS API
# ==========================

def carregar_dados_api():

    try:

        response = requests.get(
            API_URL,
            auth=(API_USER, API_PASSWORD),
            timeout=30
        )

        if response.status_code == 401:
            st.error("🔒 Não autorizado na API.")
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


# ==========================
# 📥 CARREGAR TENTATIVAS
# ==========================

def carregar_tentativas_cadastro():

    try:

        response = requests.get(
            TENTATIVAS_URL,
            params={"status": "pendente"},
            auth=(API_USER, API_PASSWORD),
            timeout=30
        )

        if response.status_code == 401:
            st.error("🔒 Não autorizado na API.")
            return []

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(
            f"❌ Erro ao carregar tentativas de cadastro: {e}"
        )

        return []


# ==========================
# ⚙️ DECIDIR TENTATIVA
# ==========================

def decidir_tentativa(tentativa_id, decisao):

    try:

        response = requests.post(
            f"{TENTATIVAS_URL}/{tentativa_id}/decidir",
            auth=(API_USER, API_PASSWORD),
            json={
                "decisao": decisao
            },
            timeout=30
        )

        if response.status_code == 200:
            return True, response.json().get(
                "message",
                "Operação realizada com sucesso."
            )

        try:
            mensagem = response.json().get(
                "error",
                "Erro desconhecido."
            )
        except Exception:
            mensagem = response.text

        return False, mensagem

    except Exception as e:

        return False, str(e)


# ==========================
# 🌐 LAYOUT
# ==========================

titulo_principal()

menu = st.sidebar.selectbox(
    "Selecione uma opção",
    [
        "São Paulo",
        "Rio de Janeiro",
        "Planilha Personalizada",
        "Dados pela API"
    ]
)

df = pd.DataFrame()

cores = ["#026141", "#9b1c1c", "#FEBE00", "#006A89"]

# ==========================
# 🔄 MENU
# ==========================

if menu == "São Paulo":

    st.header("Dashboard São Paulo")

    df = carregar_dados("data/inventario_maquinas_exemplo.csv")

    cores = ['#FF6347', '#4682B4', '#32CD32', '#FF0000']

elif menu == "Rio de Janeiro":

    st.header("Dashboard Rio de Janeiro")

    df = carregar_dados("data/inventario_maquinas_exemplo2.csv")

    cores = ['#2980B9', '#F39C12', '#1ABC9C', '#E74C3C']

elif menu == "Planilha Personalizada":

    st.header("📤 Dashboard Personalizado")

    uploaded_file = st.file_uploader(
        "Envie sua planilha (.csv ou .xlsx)",
        type=["csv", "xlsx"]
    )

    if uploaded_file:

        try:

            if uploaded_file.name.endswith(".csv"):
                df_temp = pd.read_csv(
                    uploaded_file,
                    sep=";",
                    encoding="latin1"
                )
            else:
                df_temp = pd.read_excel(uploaded_file)

            colunas_faltando = [
                col for col in colunas_esperadas
                if col not in df_temp.columns
            ]

            if colunas_faltando:

                st.warning(
                    "⚠️ A planilha está faltando as seguintes colunas:"
                )

                st.write("- " + "\n- ".join(colunas_faltando))

                for col in colunas_faltando:
                    df_temp[col] = None

            else:

                st.success("✅ Planilha carregada com sucesso!")

            df = df_temp[colunas_esperadas]

        except Exception as e:

            st.error(f"❌ Erro ao carregar a planilha: {e}")

    else:

        with st.expander(
            "📋 Ver colunas esperadas para o arquivo"
        ):

            st.markdown(
                "Sua planilha precisa conter **exatamente essas colunas**:"
            )

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
            grafico_pizza(
                df,
                "Antivírus",
                "Antivírus",
                cores
            )

        with col2:
            grafico_pizza(
                df,
                "Licença Windows",
                "Licença Windows",
                cores
            )

        col3, col4 = st.columns(2)

        with col3:
            grafico_barras(
                df,
                "Tamanho",
                "Memória RAM",
                cores
            )

        with col4:
            grafico_barras(
                df,
                "Tipo",
                "Tipo de Máquina",
                cores
            )

        grafico_pizza(
            df,
            "Tipo de armazenamento",
            "Disco Rígido",
            cores
        )

    else:

        col3, col4, col6 = st.columns(3)

        with col6:
            grafico_pizza(
                df,
                "Antivírus",
                "Antivírus",
                cores
            )

        with col3:
            grafico_pizza(
                df,
                "Licença Windows",
                "Licença Windows",
                cores
            )

        with col4:
            grafico_barras(
                df,
                "Troca de máquina",
                "Troca de Máquina",
                cores
            )

        col2, col5, col1, col7 = st.columns(4)

        with col1:
            grafico_barras(
                df,
                "Tamanho",
                "Memória RAM",
                cores
            )

        with col2:
            grafico_barras(
                df,
                "Tipo",
                "Tipo de Máquina",
                cores
            )

        with col5:
            grafico_pizza(
                df,
                "Upgrade?",
                "Upgrade?",
                cores
            )

        with col7:
            grafico_pizza(
                df,
                "Tipo de armazenamento",
                "Disco Rígido",
                cores
            )

    # ==========================
    # ⚠️ TENTATIVAS DE CADASTRO
    # ==========================

    if menu == "Dados pela API":

        st.markdown("---")

        st.subheader("⚠️ Tentativas de Cadastro")

        tentativas = carregar_tentativas_cadastro()

        if not tentativas:

            st.success(
                "✅ Nenhuma tentativa de cadastro pendente."
            )

        else:

            st.warning(
                f"⚠️ Existem {len(tentativas)} "
                f"tentativa(s) aguardando aprovação."
            )

            for tentativa in tentativas:

                tentativa_id = tentativa.get("_id")

                dados_maquina = tentativa.get(
                    "dados_maquina",
                    {}
                )

                nome_maquina = tentativa.get(
                    "Nome da máquina",
                    dados_maquina.get(
                        "Nome da máquina",
                        "Não informado"
                    )
                )

                numero_serie = tentativa.get(
                    "Número de Série",
                    dados_maquina.get(
                        "Número de Série",
                        "Não informado"
                    )
                )

                maquina_existente = tentativa.get(
                    "maquina_existente",
                    "Não informado"
                )

                quantidade = tentativa.get(
                    "quantidade_tentativas",
                    1
                )

                with st.container(border=True):

                    col_tentativa, col_acoes = st.columns(
                        [4, 1]
                    )

                    with col_tentativa:

                        st.markdown(
                            f"### 🖥️ {nome_maquina}"
                        )

                        st.write(
                            f"**Número de Série:** "
                            f"`{numero_serie}`"
                        )

                        st.write(
                            f"**Máquina que já possui esse "
                            f"número de série:** "
                            f"`{maquina_existente}`"
                        )

                        st.write(
                            f"**Quantidade de tentativas:** "
                            f"{quantidade}"
                        )

                        with st.expander(
                            "👁️ Ver dados da máquina"
                        ):

                            st.json(
                                dados_maquina
                            )

                    with col_acoes:

                        st.write("")

                        if st.button(
                            "✅ Permitir",
                            key=f"aprovar_{tentativa_id}",
                            use_container_width=True
                        ):

                            sucesso, mensagem = (
                                decidir_tentativa(
                                    tentativa_id,
                                    "aprovar"
                                )
                            )

                            if sucesso:

                                st.success(
                                    mensagem
                                )

                                st.rerun()

                            else:

                                st.error(
                                    mensagem
                                )

                        if st.button(
                            "❌ Recusar",
                            key=f"recusar_{tentativa_id}",
                            use_container_width=True
                        ):

                            sucesso, mensagem = (
                                decidir_tentativa(
                                    tentativa_id,
                                    "recusar"
                                )
                            )

                            if sucesso:

                                st.success(
                                    mensagem
                                )

                                st.rerun()

                            else:

                                st.error(
                                    mensagem
                                )

    # ==========================
    # 🔎 FILTRO
    # ==========================

    df_filtrado = filtro_departamento(df)

    # ==========================
    # ✏️ CAMPOS EDITÁVEIS
    # ==========================

    colunas_editaveis = [
        "Etiqueta",
        "Cidade",
        "Departamento",
        "Unidade Residente",
        "Observações"
    ]

    colunas_bloqueadas = [
        col for col in df_filtrado.columns
        if col not in colunas_editaveis
    ]

    # ==========================
    # 🔽 ÁREA EDITÁVEL
    # ==========================

    with st.expander(
        "✏️ Editar Informações",
        expanded=False
    ):

        df_editado = st.data_editor(
            df_filtrado,
            use_container_width=True,
            disabled=colunas_bloqueadas,
            num_rows="fixed",
            hide_index=True
        )

        # ==========================
        # 💾 SALVAR ALTERAÇÕES
        # ==========================

        if st.button("💾 Salvar Alterações"):

            progresso = st.progress(0)

            total = len(df_editado)

            for i, (_, row) in enumerate(df_editado.iterrows()):

                try:

                    # ✅ Corrige NaN / None
                    dados_limpos = (
                        row.fillna("")
                        .replace([float("inf"), float("-inf")], "")
                        .to_dict()
                    )

                    response = requests.put(
                        EDITAR_URL,
                        auth=(API_USER, API_PASSWORD),
                        json=dados_limpos,
                        timeout=30
                    )

                    if response.status_code != 200:

                        st.warning(
                            f"⚠️ Erro ao atualizar "
                            f"{row['Nome da máquina']}"
                        )

                except Exception as e:

                    st.error(f"❌ Erro: {e}")

                progresso.progress((i + 1) / total)

            progresso.empty()

            st.success(
                "✅ Alterações salvas com sucesso!"
            )

            st.rerun()


    # ==========================
    # 🗑️ EXCLUIR MÁQUINA
    # ==========================

    if menu == "Dados pela API" and not df_filtrado.empty:

        with st.expander("🗑️ Remover máquina do inventário", expanded=False):

            st.warning(
                "A exclusão remove permanentemente o registro do MongoDB."
            )

            maquinas = sorted(
                df_filtrado["Nome da máquina"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            if maquinas:
                maquina_selecionada = st.selectbox(
                    "Selecione a máquina que deseja remover",
                    options=maquinas,
                    key="maquina_para_excluir"
                )

                confirmar = st.checkbox(
                    f"Confirmo a exclusão da máquina {maquina_selecionada}",
                    key="confirmar_exclusao"
                )

                if st.button(
                    "🗑️ Excluir máquina",
                    type="primary",
                    disabled=not confirmar,
                    key="botao_excluir_maquina"
                ):
                    try:
                        response = requests.delete(
                            EXCLUIR_URL,
                            auth=(API_USER, API_PASSWORD),
                            json={
                                "Nome da máquina": maquina_selecionada
                            },
                            timeout=30
                        )

                        if response.status_code == 200:
                            st.success(
                                f"Máquina {maquina_selecionada} excluída com sucesso!"
                            )
                            st.rerun()

                        elif response.status_code == 404:
                            st.error(
                                "A máquina não foi encontrada no banco de dados."
                            )

                        elif response.status_code == 401:
                            st.error(
                                "Não autorizado. Verifique as credenciais da API."
                            )

                        else:
                            st.error(
                                f"Falha ao excluir: {response.status_code} - "
                                f"{response.text}"
                            )

                    except requests.RequestException as e:
                        st.error(f"Erro de comunicação com a API: {e}")


    # ==========================
    # 📥 DOWNLOAD CSV
    # ==========================

    csv = df_filtrado.to_csv(
        index=False,
        sep=";",
        encoding="latin1"
    )

    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=csv,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )