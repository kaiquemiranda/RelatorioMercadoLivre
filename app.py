import streamlit as st
import metricas
import mapa
import graficos


st.set_page_config(page_title="Análise de Vendas de Peças", layout="wide")
st.sidebar.image('mercado.png', width=250)
st.sidebar.title("Análise de Vendas")

with open("style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel", type=["xls", "xlsx"])

if uploaded_file:
    # LAYOUT
    with st.container():
        metricas.metric(uploaded_file)
    with st.container():
        colu1, colu2 = st.columns([1, 2])
        with colu1:
            st.plotly_chart(graficos.faturamentoDespesas(uploaded_file))
        with colu2:
            st.plotly_chart(mapa.mapaEstados(uploaded_file))
    with st.container():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.plotly_chart(graficos.skuMaisVendido(uploaded_file))
        with col2:
            # Mostrar o gráfico
            st.plotly_chart(graficos.estadosMaisVendidos(uploaded_file))
else:
    st.markdown(
        "<h1 style='color: #031d4d; text-align: center; font-size: 60px;  margin-top: -80px; '>Carregue o excel do Mercado livre</h1>",
        unsafe_allow_html=True)