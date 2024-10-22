import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO


def filtro(df):

        palavras_chave = st.sidebar.text_input("Buscar produto por palavras-chave.").strip()
        palavras_excluir = st.sidebar.text_input("Digite o que deseja excluir da busca.").strip()

        if st.sidebar.button("Buscar"):
            if palavras_chave:
                palavras_chave = palavras_chave.lower().split()
                palavras_excluir = palavras_excluir.lower().split() if palavras_excluir else []

                filtro_incluir = df['Título do anúncio'].str.contains(palavras_chave[0], case=False)
                for palavra in palavras_chave[1:]:
                    filtro_incluir &= df['Título do anúncio'].str.contains(palavra, case=False)

                filtro_excluir = ~df['Título do anúncio'].str.contains(palavras_excluir[0],
                                                                       case=False) if palavras_excluir else True
                for palavra in palavras_excluir[1:]:
                    filtro_excluir &= ~df['Título do anúncio'].str.contains(palavra, case=False)

                df_filtrado = df[filtro_incluir & filtro_excluir]

                df_filtrado['frete real'] = df_filtrado['Tarifas de envio'] + df_filtrado['Receita por envio (BRL)']

                if not df_filtrado.empty:

                    buffer = BytesIO()

                    vendas_por_sku = df_filtrado.groupby('SKU').agg({
                        'SKU': 'first',
                        'Título do anúncio': 'first',  # Mantém o primeiro título do anúncio
                        'Receita por produtos (BRL)': 'sum',  # Soma a receita
                        'Unidades': 'sum',  # Soma as unidades
                    }).sort_values(by='Unidades', ascending=False)



                    fig = px.bar(vendas_por_sku.head(10).sort_values(by='Unidades', ascending=True),
                                 y='SKU',
                                 x='Unidades',
                                 title=f'Produtos mais vendidos para as palavras-chave: {", ".join(palavras_chave).capitalize()}',
                                 labels={'SKU': 'SKU', 'Unidades': 'Quantidade de Vendas'},
                                 text_auto=True,
                                 hover_data={'Título do anúncio': True})

                    with st.container():
                        st.plotly_chart(fig, use_container_width=True)

                    with st.container():
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            vendas_por_sku.to_excel(writer, index=False, sheet_name='Vendas por SKU')

                        st.divider()
                        st.dataframe(
                            df_filtrado[['N.º de venda', 'SKU', 'Unidades', 'Data da venda', 'Título do anúncio',
                                         'Receita por produtos (BRL)', 'frete real',
                                         'Tarifa de venda e impostos', 'Total (BRL)', 'Loja oficial']])

                        st.markdown(f"Total: {df_filtrado['Unidades'].sum()}")

                        buffer.seek(0)

                        st.download_button(
                            label="Baixar Excel",
                            data=buffer,
                            file_name="vendas_por_sku.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                else:
                    st.warning("Nenhum resultado encontrado para as palavras-chave fornecidas.")
            else:
                st.info("Por favor, insira palavras-chave para realizar a busca.")