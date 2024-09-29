import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Dicionário para mapear nomes completos dos estados para suas siglas
estado_to_sigla = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amazonas': 'AM', 'Amapá': 'AP', 'Bahia': 'BA',
    'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO',
    'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
    'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI',
    'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rondônia': 'RO', 'Rio Grande do Sul': 'RS',
    'Roraima': 'RR', 'Santa Catarina': 'SC', 'Sergipe': 'SE', 'São Paulo': 'SP', 'Tocantins': 'TO'
}


def faturamentoDespesas(file):
    # Carregar os dados
    df = pd.read_excel(file, engine='openpyxl', skiprows=5)

    if df.empty or 'Título do anúncio' not in df.columns:
        # Se não funcionar, tentar ler pulando 6 linhas
        df = pd.read_excel(file, engine='openpyxl', skiprows=6)

    # Renomear a coluna Status.1 para 'estados' e substituir os nomes completos pelas siglas
    df['estados'] = df['Status.1'].map(estado_to_sigla)

    # Cálculos de faturamento e despesas
    faturamento_total = df['Receita por produtos (BRL)'].sum()
    tarifa_venda = abs(df['Tarifa de venda e impostos'].sum())  # Converter para positivo
    tarifa_frete = abs(df['Tarifas de envio'].sum())  # Converter para positivo

    # Cálculo do faturamento real
    faturamento_real = faturamento_total - tarifa_venda - tarifa_frete

    # Criar um novo DataFrame para o gráfico de rosca
    dados = {
        'Categoria': ['Faturamento Total', 'Tarifa de Venda', 'Tarifa de Frete'],
        'Valores': [faturamento_total, tarifa_venda, tarifa_frete]
    }

    df_grafico = pd.DataFrame(dados)

    # Criar gráfico de rosca
    fig = px.pie(
        df_grafico,
        names='Categoria',
        values='Valores',
        hole=0.4,  # Faz o gráfico ser de rosca
        title='Distribuição do Faturamento e Despesas'
    )

    fig.update_layout(
        title_x=0.15,  # Centraliza o título
        legend=dict(
            orientation="h",  # Coloca a legenda na horizontal
            yanchor="bottom",  # Alinha a legenda na parte inferior
            y=-0.3,  # Define a posição vertical (mais abaixo do gráfico)
            xanchor="center",  # Centraliza a legenda
            x=0.5  # Posição horizontal no centro
        )
    )

    # Retornar o gráfico
    return fig


# Função principal do Streamlit
def estadosMaisVendidos(file):
    df = pd.read_excel(file, engine='openpyxl', skiprows=5)
    if df.empty or 'Título do anúncio' not in df.columns:
        # Se não funcionar, tentar ler pulando 6 linhas
        df = pd.read_excel(file, engine='openpyxl', skiprows=6)

    # Renomear a coluna Status.1 para 'estados' e substituir os nomes completos pelas siglas
    df['estados'] = df['Status.1'].map(estado_to_sigla)

    # Contar vendas por estado
    vendas_por_estado = df['estados'].value_counts().reset_index()
    vendas_por_estado.columns = ['estado', 'vendas']

    # Calcular a porcentagem de vendas por estado
    total_vendas = vendas_por_estado['vendas'].sum()
    vendas_por_estado['percentual'] = (vendas_por_estado['vendas'] / total_vendas) * 100

    # Selecionar os 10 estados com mais vendas
    top_10_estados = vendas_por_estado.head(10)

    # Criar gráfico de pizza
    fig_pizza = px.pie(
        top_10_estados,
        values='vendas',
        names='estado',
        title='Estados com Mais Vendas',
        color='estado',
        color_discrete_sequence=px.colors.sequential.Magma,
        hole=0.3  # Para um gráfico de pizza
    )

    # Atualizar o layout para melhorar a visualização
    fig_pizza.update_layout(title_x=0.3)  # Centraliza o título

    # Mostrar o gráfico no Streamlit
    return fig_pizza


def skuMaisVendido(file):
    df = pd.read_excel(file, engine='openpyxl', skiprows=5)
    if df.empty or 'Título do anúncio' not in df.columns:
        # Se não funcionar, tentar ler pulando 6 linhas
        df = pd.read_excel(file, engine='openpyxl', skiprows=6)

    # Filtrar produtos que têm SKU (remover linhas onde SKU é vazio ou NaN)
    df = df[df['SKU'].notna() & (df['SKU'] != '')]

    # Agrupar e somar as unidades vendidas por SKU
    vendas_por_sku = df.groupby('SKU')['Unidades'].sum().reset_index()

    # Ordenar os produtos mais vendidos
    vendas_por_sku = vendas_por_sku.sort_values(by='Unidades', ascending=False)

    # Criar o gráfico de barras
    fig = px.bar(
        vendas_por_sku.iloc[1:11],
        x='SKU',
        y='Unidades',
        title='Produtos mais vendidos',
        labels={'SKU': 'SKU', 'Unidades': 'Quantidade de Vendas'},
        text_auto=True
    )

    fig.update_layout(title_x=0.3)

    return fig

