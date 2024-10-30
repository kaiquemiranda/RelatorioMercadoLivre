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


def faturamentoDespesas(df):

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
def estadosMaisVendidos(df):


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


def skuMaisVendido(df, num_produtos):


    # Agrupar e somar as unidades vendidas por SKU
    vendas_por_sku = df.groupby('SKU').agg({
    'SKU': 'first',
    'Título do anúncio': 'first',  # Mantém o primeiro título do anúncio
    'Receita por produtos (BRL)': 'sum',  # Soma a receita
    'Unidades': 'sum'  # Soma as unidades
}).sort_values(by='Unidades', ascending=False).head(num_produtos+1)

    # Ordenar os produtos mais vendidos
    vendas_por_sku = vendas_por_sku.sort_values(by='Unidades', ascending=False)

    # Criar o gráfico de barras
    fig = px.bar(
        vendas_por_sku.iloc[1:],
        x='SKU',
        y='Unidades',
        title=f'Os {num_produtos} Produtos mais vendidos',
        labels={'SKU': 'SKU', 'Unidades': 'Quantidade de Vendas'},
        text_auto=True,
        hover_data={'Título do anúncio': True}
    )

    fig.update_layout(title_x=0.3)

    return fig


def freteAlto(df):
    # Calculo de porcentagem de frete
    df['frete real'] = df['Tarifas de envio'] + df['Receita por envio (BRL)']
    fretePositivo = df['frete real'] - df['frete real'] - df['frete real']
    df['Porcentagem frete'] = fretePositivo / (df['Receita por produtos (BRL)'] / 100)
    frete30 = df[['Data da venda', 'Título do anúncio', 'N.º de venda', 'SKU', 'Receita por produtos (BRL)', 'Porcentagem frete', 'frete real']]
    maior_frete = frete30[frete30['Porcentagem frete'] > 29].sort_values('Porcentagem frete')
    maior100 = frete30[frete30['frete real'] < -120]
    media = df['frete real'].mean()
    lista = [maior100, maior_frete]
    maior100conc = pd.concat(lista)

    maior_frete_sku = maior100conc.groupby('SKU').agg({
    'SKU': 'first',
    'Título do anúncio': 'first',  # Mantém o primeiro título do anúncio
    'Receita por produtos (BRL)': 'sum',  # Soma a receita
    'N.º de venda': "first"
    })
    maior_frete_sku = maior100conc.sort_values(by='Porcentagem frete', ascending=False)

    fig = px.bar(maior_frete_sku, x='SKU', y='Porcentagem frete',
                 title='Vendas com frete maior que 30%',
                 labels={'Porcentagem frete': 'Porcentagem frete', 'SKU': 'SKU'},
                 hover_data={'Título do anúncio': True, 'Receita por produtos (BRL)': True, 'frete real': True})

    if maior_frete_sku is not None:
        # Ajustar a rotação do eixo x e alinhamento dos rótulos
        fig.update_layout(title_x=0.3)
        return fig
    else:
        return st.markdown("Não há vendas com frete maior que 30% no período informado")

    
