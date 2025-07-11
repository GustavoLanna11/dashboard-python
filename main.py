import streamlit as st
from src.loader import carregar_dados
from src.graph import grafico_barras, grafico_pizza
from src.layout import titulo_principal, filtro_departamento, mostrar_kpis
import pandas as pd

# ✅ Lista completa de colunas esperadas
colunas_esperadas = [
    "Nome da máquina", "Proprietário", "Etiqueta", "Cidade", "Departamento",
    "Unidade Residente", "Marca", "Número de Série", "Tipo", "Modelo",
    "Licença", "Processador", "Troca de máquina", "Tipo de memória", "Pentes",
    "Tamanho", "Armazenamento", "Tipo de armazenamento", "Licença Windows",
    "Troca ou Upgrade", "Prioridade", "Antivírus", "Upgrade?", "Em uso?",
    "Está no AD?", "Observações"
]

titulo_principal()
menu = st.sidebar.selectbox("Selecione uma opção", ["São Paulo", "Rio de Janeiro", "Planilha Personalizada"])

df = None
cores = ['#FF6347', '#4682B4', '#32CD32', '#FF0000']

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
            else:  # assume .xlsx
                df_temp = pd.read_excel(uploaded_file)

            # Verifica colunas obrigatórias
            colunas_faltando = [col for col in colunas_esperadas if col not in df_temp.columns]
            if colunas_faltando:
                st.warning("⚠️ A planilha está faltando as seguintes colunas:")
                st.write("- " + "\n- ".join(colunas_faltando))
            else:
                st.success("✅ Planilha carregada com sucesso!")
                df = df_temp  # Só atribui à variável principal se tudo estiver certo
        except Exception as e:
            st.error(f"❌ Erro ao carregar a planilha: {e}")
    else:
        with st.expander("📋 Ver colunas esperadas para o arquivo"):
            st.markdown("Sua planilha precisa conter **exatamente essas colunas** para funcionar corretamente:")
            st.markdown("- " + "\n- ".join(colunas_esperadas))


# Se houver DataFrame carregado, exibe os KPIs e gráficos
if df is not None:
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

    df_filtrado = filtro_departamento(df)
    csv = df_filtrado.to_csv(index=False, sep=";", encoding="latin1")
    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=csv,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )
