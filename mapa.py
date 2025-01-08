import pandas as pd
import plotly.express as px
import json
import requests



def mapaEstados(df):
    estado_to_sigla = {
        'Acre': 'AC', 'Alagoas': 'AL', 'Amazonas': 'AM', 'Amapá': 'AP', 'Bahia': 'BA',
        'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO',
        'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
        'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI',
        'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rondônia': 'RO', 'Rio Grande do Sul': 'RS',
        'Roraima': 'RR', 'Santa Catarina': 'SC', 'Sergipe': 'SE', 'São Paulo': 'SP', 'Tocantins': 'TO'
    }


    # Renomear a coluna Status.1 para 'estados' e substituir os nomes completos pelas siglas
    df['estados'] = df['Estado'].map(estado_to_sigla)

    # Contar vendas por estado (agora usando a coluna 'estados')
    vendas_por_estado = df['estados'].value_counts().reset_index()
    vendas_por_estado.columns = ['estado', 'vendas']

    # Calcular a porcentagem de vendas por estado
    total_vendas = vendas_por_estado['vendas'].sum()
    vendas_por_estado['percentual'] = (vendas_por_estado['vendas'] / total_vendas) * 100

    # URL do GeoJSON dos estados do Brasil
    geojson_url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
    geojson_data = requests.get(geojson_url).json()

    # Criar o gráfico de Choropleth
    fig = px.choropleth(
        vendas_por_estado,
        geojson=geojson_data,
        locations='estado',  # Nome dos estados no DataFrame (agora são siglas)
        featureidkey="properties.sigla",  # Atributo do GeoJSON que corresponde aos estados
        color='vendas',  # A cor será baseada na porcentagem de vendas
        hover_name='estado',  # Nome dos estados no hover
        hover_data={'vendas': True, 'percentual': ':.2f'},  # Mostrar vendas e percentual no hover
        color_continuous_scale='Cividis',
        labels={'percentual': 'Percentual de Vendas (%)'},
        title='Percentual de Vendas por Estado no Brasil'
    )
    
    fig.update_layout(title_x=0.1)

    # Ajustar o mapa para focar no Brasil
    fig.update_geos(
        fitbounds="locations",  # Ajustar os limites do mapa
        visible=False,  # Remover linhas de grade
    )


    return fig



