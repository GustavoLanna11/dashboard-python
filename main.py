import streamlit as st
import pandas as pd
import requests
import io
import math
import os
from datetime import datetime

st.set_page_config(
    page_title="Inventário de Máquinas",
    page_icon="💻",
    layout="wide"
)

API_URL = "https://api-inventario-wudx.onrender.com"

API_USER = os.getenv(
    "API_USER",
    "admin"
)

API_PASSWORD = os.getenv(
    "API_PASSWORD",
    "admin"
)


def api_auth():
    return (
        API_USER,
        API_PASSWORD
    )


def carregar_dados_api():
    try:
        response = requests.get(
            f"{API_URL}/dados",
            auth=api_auth(),
            timeout=60
        )

        if response.status_code == 200:
            return pd.DataFrame(
                response.json()
            )

        st.error(
            f"Erro ao carregar API: {response.status_code}"
        )

    except Exception as e:
        st.error(
            f"Erro de conexão: {e}"
        )

    return pd.DataFrame()


def carregar_tentativas(status="pendente"):
    try:
        response = requests.get(
            f"{API_URL}/tentativas_cadastro",
            params={"status": status},
            auth=api_auth(),
            timeout=60
        )

        if response.status_code == 200:
            return response.json()

        st.error(
            f"Erro ao carregar tentativas: "
            f"{response.status_code}"
        )

    except Exception as e:
        st.error(
            f"Erro ao carregar tentativas: {e}"
        )

    return []


def decidir_tentativa(tentativa_id, decisao):
    try:
        response = requests.post(
            f"{API_URL}/tentativas_cadastro/"
            f"{tentativa_id}/decidir",
            json={
                "decisao": decisao
            },
            auth=api_auth(),
            timeout=60
        )

        if response.status_code == 200:
            return True, response.json().get(
                "mensagem",
                "Operação concluída."
            )

        try:
            mensagem = response.json().get(
                "erro",
                "Erro desconhecido."
            )
        except Exception:
            mensagem = response.text

        return False, mensagem

    except Exception as e:
        return False, str(e)


st.title("💻 Inventário de Máquinas")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "São Paulo",
        "Rio de Janeiro",
        "Planilha Personalizada",
        "Dados pela API"
    ]
)


if menu == "Dados pela API":

    st.subheader("📡 Dados pela API")

    df = carregar_dados_api()

    if not df.empty:

        colunas = [
            coluna
            for coluna in df.columns
            if coluna != "_id"
        ]

        if "Cidade" in df.columns:
            cidades = [
                "Todas"
            ] + sorted(
                df["Cidade"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            cidade_filtro = st.selectbox(
                "Filtrar por cidade",
                cidades
            )

            if cidade_filtro != "Todas":
                df = df[
                    df["Cidade"].astype(str)
                    == cidade_filtro
                ]

        st.markdown("### 📊 Resumo")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Máquinas",
                len(df)
            )

        with col2:
            if "Cidade" in df.columns:
                st.metric(
                    "Cidades",
                    df["Cidade"]
                    .nunique()
                )
            else:
                st.metric(
                    "Cidades",
                    0
                )

        with col3:
            if "Departamento" in df.columns:
                st.metric(
                    "Departamentos",
                    df["Departamento"]
                    .nunique()
                )
            else:
                st.metric(
                    "Departamentos",
                    0
                )

        with col4:
            if "Unidade Residente" in df.columns:
                st.metric(
                    "Unidades",
                    df["Unidade Residente"]
                    .nunique()
                )
            else:
                st.metric(
                    "Unidades",
                    0
                )

        st.markdown("### 📈 Distribuição")

        col1, col2 = st.columns(2)

        with col1:
            if "Cidade" in df.columns:
                st.write(
                    "Máquinas por cidade"
                )

                cidade_data = (
                    df["Cidade"]
                    .fillna("Não informado")
                    .value_counts()
                )

                st.bar_chart(cidade_data)

        with col2:
            if "Departamento" in df.columns:
                st.write(
                    "Máquinas por departamento"
                )

                departamento_data = (
                    df["Departamento"]
                    .fillna("Não informado")
                    .value_counts()
                )

                st.bar_chart(
                    departamento_data
                )

        st.markdown("---")

        st.subheader(
            "⚠️ Tentativas de cadastro"
        )

        st.caption(
            "Máquinas que tentaram entrar no inventário "
            "com número de série já existente."
        )

        tentativas = carregar_tentativas(
            "pendente"
        )

        if not tentativas:
            st.success(
                "Nenhuma tentativa pendente."
            )

        else:

            st.info(
                f"{len(tentativas)} tentativa(s) "
                "aguardando decisão."
            )

            for tentativa in tentativas:

                tentativa_id = tentativa.get(
                    "_id"
                )

                maquina = tentativa.get(
                    "dados_maquina",
                    {}
                )

                nome = tentativa.get(
                    "Nome da máquina",
                    "Não informado"
                )

                serial = tentativa.get(
                    "Número de Série",
                    "Não informado"
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

                    col1, col2 = st.columns(
                        [4, 2]
                    )

                    with col1:

                        st.markdown(
                            f"### 🖥️ {nome}"
                        )

                        st.write(
                            f"**Número de Série:** "
                            f"`{serial}`"
                        )

                        st.write(
                            f"**Máquina que já possui "
                            f"esse serial:** "
                            f"`{maquina_existente}`"
                        )

                        st.write(
                            f"**Tentativas:** "
                            f"{quantidade}"
                        )

                        if maquina:
                            with st.expander(
                                "Ver dados enviados"
                            ):
                                st.json(maquina)

                    with col2:

                        st.write(
                            "### Decisão"
                        )

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

        st.markdown("---")

        st.subheader(
            "📋 Inventário"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Nenhum dado encontrado na API."
        )

        st.subheader(
            "⚠️ Tentativas de cadastro"
        )

        tentativas = carregar_tentativas(
            "pendente"
        )

        if not tentativas:
            st.info(
                "Nenhuma tentativa pendente."
            )

        for tentativa in tentativas:

            tentativa_id = tentativa.get(
                "_id"
            )

            maquina = tentativa.get(
                "dados_maquina",
                {}
            )

            nome = tentativa.get(
                "Nome da máquina",
                "Não informado"
            )

            serial = tentativa.get(
                "Número de Série",
                "Não informado"
            )

            with st.container(border=True):

                st.markdown(
                    f"### 🖥️ {nome}"
                )

                st.write(
                    f"**Número de Série:** `{serial}`"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Permitir",
                        key=f"aprovar_empty_{tentativa_id}",
                        use_container_width=True
                    ):

                        sucesso, mensagem = (
                            decidir_tentativa(
                                tentativa_id,
                                "aprovar"
                            )
                        )

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.error(mensagem)

                with col2:

                    if st.button(
                        "❌ Recusar",
                        key=f"recusar_empty_{tentativa_id}",
                        use_container_width=True
                    ):

                        sucesso, mensagem = (
                            decidir_tentativa(
                                tentativa_id,
                                "recusar"
                            )
                        )

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.error(mensagem)


elif menu == "Planilha Personalizada":

    st.title(
        "📊 Planilha Personalizada"
    )

    arquivo = st.file_uploader(
        "Envie uma planilha Excel",
        type=["xlsx", "xls"]
    )

    if arquivo:

        try:
            df = pd.read_excel(
                arquivo
            )

            st.success(
                "Planilha carregada com sucesso."
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            output = io.BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:
                df.to_excel(
                    writer,
                    index=False
                )

            st.download_button(
                "⬇️ Baixar planilha",
                data=output.getvalue(),
                file_name="inventario.xlsx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                )
            )

        except Exception as e:

            st.error(
                f"Erro ao ler planilha: {e}"
            )


else:

    st.title(
        f"💻 Inventário - {menu}"
    )

    df = carregar_dados_api()

    if not df.empty and "Cidade" in df.columns:

        df = df[
            df["Cidade"]
            .astype(str)
            .str.lower()
            == menu.lower()
        ]

    if df.empty:

        st.info(
            "Nenhuma máquina encontrada."
        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )