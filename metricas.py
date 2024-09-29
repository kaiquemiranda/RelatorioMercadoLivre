import pandas as pd
import streamlit as st

# Função principal do Streamlit
def metric(file):
    df = pd.read_excel(file, engine='openpyxl', skiprows=5)
    if df.empty or 'Título do anúncio' not in df.columns:
        # Se não funcionar, tentar ler pulando 6 linhas
        df = pd.read_excel(file, engine='openpyxl', skiprows=6)

    # Calcular as métricas
    faturamento_total = df['Receita por produtos (BRL)'].sum()  # Supondo que a coluna se chama 'Receita'
    tarifa_venda = df['Tarifa de venda e impostos'].sum()
    tarifa_frete = df['Tarifas de envio'].sum()
    faturamento_real = faturamento_total - (tarifa_venda - tarifa_venda - tarifa_venda) - (tarifa_frete - tarifa_frete - tarifa_frete)

    coluna1, coluna2, coluna3, coluna4 = st.columns([1, 1, 1, 1])
    with coluna1:
        st.metric(label="Faturamento bruto", value=f"R$ {faturamento_total:,.2f}")
    with coluna2:
        st.metric(label="Tarifas de venda", value=f"R$ {tarifa_venda:,.2f}")
    with coluna3:
        st.metric(label="Tarifas de frete", value=f"R$ {tarifa_frete:,.2f}")
    with coluna4:
        st.metric(label="Faturamento Real", value=f"R$ {faturamento_real:,.2f}")






