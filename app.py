import streamlit as st
import metricas
import mapa
import graficos
import pandas as pd
import palavrachave

st.set_page_config(page_title="Análise de Vendas de Peças", layout="wide")
st.sidebar.image('mercado.png', width=250)


st.sidebar.markdown(
        "<h1 style='color: #031d4d; text-align: center; font-size: 30px;  margin-top: 40px; '>Análise de vendas</h1>",
        unsafe_allow_html=True)

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
        col1, col2 = st.columns([3, 2])
        with col1:
            st.sidebar.markdown('----')
            num_produtos = st.sidebar.slider('Produtos mais vendidos ', min_value=1, max_value=30, value=10)
            # num_produtos = st.selectbox('Selecione quantos produtos mais vendidos você deseja ver:', options=[5, 10, 15, 20])
            st.plotly_chart(graficos.skuMaisVendido(file, num_produtos))
        with col2:
            # Mostrar o gráfico
            st.plotly_chart(graficos.freteAlto(file))
    with st.container():
        colu1, colu2, colu3 = st.columns([1, 1, 1])
        with colu1:
            st.plotly_chart(graficos.faturamentoDespesas(file))
        with colu2:
            st.plotly_chart(mapa.mapaEstados(file))
        with colu3:
            st.plotly_chart(graficos.estadosMaisVendidos(file))
        
    with st.container():
        st.sidebar.markdown('----')
        palavrachave.filtro(file)
else:
    st.markdown(
        "<h1 style='color: #031d4d; text-align: center; font-size: 60px;  margin-top: 50px; margin-bottom: 150px; '>Carregue o excel do Mercado livre</h1>",
        unsafe_allow_html=True)


with st.container():
    coluna1, coluna2, coluna3 = st.columns([1, 1, 1])
    with coluna1:
        st.image('alfredos.png', width=150)
    with coluna2:
        st.image('Box7.png', width=150)
    with coluna3:
        st.image('marrocos.png', width=150)



st.markdown("<p style='text-align: center; margin-top: 200px; '> </p>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 25px;'>Desenvolvido por Kaique Miranda - © 2024</p>", unsafe_allow_html=True)
