import plotly.express as px
import streamlit as st

def grafico_barras(df, coluna, titulo, cores):
    contagem = df[coluna].value_counts().reset_index(name="Quantidade")
    contagem.columns = [coluna, "Quantidade"]
    fig = px.bar(contagem, x=coluna, y="Quantidade", title=titulo, color=coluna, text="Quantidade", color_discrete_sequence=cores)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)

    # Botão para exportar o gráfico como imagem
    img_bytes = fig.to_image(format="png", width=800, height=600)
    st.download_button(
        label="📥 Baixar gráfico (PNG)",
        data=img_bytes,
        file_name=f"{titulo.replace(' ', '_')}.png",
        mime="image/png"
    )

def grafico_pizza(df, coluna, titulo, cores):
    contagem = df[coluna].value_counts().reset_index(name="Quantidade")
    contagem.columns = [coluna, "Quantidade"]
    fig = px.pie(contagem, names=coluna, values="Quantidade", title=titulo, color=coluna, color_discrete_sequence=cores)
    st.plotly_chart(fig)

    # Botão para exportar o gráfico como imagem
    img_bytes = fig.to_image(format="png", width=800, height=600)
    st.download_button(
        label="📥 Baixar gráfico (PNG)",
        data=img_bytes,
        file_name=f"{titulo.replace(' ', '_')}.png",
        mime="image/png"
    )