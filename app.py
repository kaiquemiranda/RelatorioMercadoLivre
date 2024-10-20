import streamlit as st
import metricas
import mapa
import graficos
import pandas as pd

st.set_page_config(page_title="Análise de Vendas de Peças", layout="wide")
st.sidebar.image('mercado.png', width=250)
st.sidebar.title("Análise de Vendas")

with open("style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


lista = []
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xls", "xlsx"])
    if uploaded_file:
        df1 = pd.read_excel(uploaded_file, engine='openpyxl', skiprows=5)
        if df1.empty or 'Título do anúncio' not in df1.columns:
            # Se não funcionar, tentar ler pulando 6 linhas
            df1 = pd.read_excel(uploaded_file, engine='openpyxl', skiprows=6)
    if uploaded_file:
        lista.append(df1)
with col2:
    uploaded_file2 = st.file_uploader("Carregar arquivo Excel", type=["xls", "xlsx"], key='chave2')
    if uploaded_file2:
        df2 = pd.read_excel(uploaded_file2, engine='openpyxl', skiprows=5)
        if df2.empty or 'Título do anúncio' not in df2.columns:
            # Se não funcionar, tentar ler pulando 6 linhas
            df2 = pd.read_excel(uploaded_file2, engine='openpyxl', skiprows=6)
    if uploaded_file2:
        lista.append(df2)
with col3:
    uploaded_file3 = st.file_uploader("Carregar arquivo Excel", type=["xls", "xlsx"], key='chave3')
    if uploaded_file3:
        df3 = pd.read_excel(uploaded_file3, engine='openpyxl', skiprows=5)
        if df3.empty or 'Título do anúncio' not in df3.columns:
            # Se não funcionar, tentar ler pulando 6 linhas
            df3 = pd.read_excel(uploaded_file2, engine='openpyxl', skiprows=6)
    if uploaded_file3:
        lista.append(df3)


if uploaded_file and (uploaded_file2 or uploaded_file3):
    file = pd.concat(lista)
elif uploaded_file:
    file = df1

st.divider()

if lista:
    # LAYOUT
    with st.container():
        metricas.metric(file)
    with st.container():
        colu1, colu2 = st.columns([1, 2])
        with colu1:
            st.plotly_chart(graficos.faturamentoDespesas(file))
        with colu2:
            st.plotly_chart(mapa.mapaEstados(file))
    with st.container():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.sidebar.markdown('----')
            num_produtos = st.sidebar.slider('Produtos mais vendidos ', min_value=1, max_value=30, value=10)
            # num_produtos = st.selectbox('Selecione quantos produtos mais vendidos você deseja ver:', options=[5, 10, 15, 20])
            st.plotly_chart(graficos.skuMaisVendido(file, num_produtos))
        with col2:
            # Mostrar o gráfico
            st.plotly_chart(graficos.estadosMaisVendidos(file))
else:
    st.markdown(
        "<h1 style='color: #031d4d; text-align: center; font-size: 60px;  margin-top: 80px; '>Carregue o excel do Mercado livre</h1>",
        unsafe_allow_html=True)
