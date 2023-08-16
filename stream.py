import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Função para carregar os dados
def load_data(file):
    if file is not None:
        data = pd.read_csv(file)
        return data
    return None

# Função para filtrar os dados com base nas seleções
def apply_filters(data, filters):
    for col, values in filters.items():
        if 'all' not in values:
            data = data[data[col].isin(values)]
    return data

# Função principal da aplicação
def main():
    st.set_page_config(
        page_title='Telemarketing analysis',
        page_icon='telemarketing_icon.png',
        layout="wide",
        initial_sidebar_state='expanded'
    )

    st.write('# Telemarketing analysis')
    st.markdown("---")

    image = Image.open("Bank-Branding.jpg")
    st.sidebar.image(image)

    st.sidebar.write("## Suba o arquivo")
    data_file = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])

    if data_file is not None:
        bank_raw = load_data(data_file)

        if bank_raw is not None and not bank_raw.empty:
            st.write('## Antes dos filtros')
            st.write(bank_raw.head())

            # Filtros
            filters = {
                'job': ['all'],
                'marital': ['all'],
                'default': ['all'],
                'housing': ['all'],
                'loan': ['all'],
                'contact': ['all'],
                'month': ['all'],
                'day_of_week': ['all']
            }

            # Criação de seletores de filtro
            for col in filters.keys():
                unique_values = bank_raw[col].unique()
                filters[col] = st.multiselect(f"{col.capitalize()}:", unique_values, ['all'])

            # Aplica os filtros
            bank = apply_filters(bank_raw, filters)

            if not bank.empty:
                st.write('## Após os filtros')
                st.write(bank.head())

                st.write('## Proporção de aceite')

                # Calcula a proporção de aceite para os dados brutos
                bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True) * 100
                bank_raw_target_perc = bank_raw_target_perc.sort_index()

                # Calcula a proporção de aceite para os dados filtrados
                bank_target_perc = bank['y'].value_counts(normalize=True) * 100
                bank_target_perc = bank_target_perc.sort_index()

                # Gráficos de barras
                fig, ax = plt.subplots(1, 2, figsize=(10, 5))
                sns.barplot(x=bank_raw_target_perc.index, y='y', data=bank_raw_target_perc.to_frame(), ax=ax[0])
                sns.barplot(x=bank_target_perc.index, y='y', data=bank_target_perc.to_frame(), ax=ax[1])

                ax[0].set_title('Dados brutos', fontweight="bold")
                ax[0].set_xlabel('y')
                ax[0].set_ylabel('Porcentagem')
                ax[0].set_xticklabels(bank_raw_target_perc.index, rotation=45)

                ax[1].set_title('Dados filtrados', fontweight="bold")
                ax[1].set_xlabel('y')
                ax[1].set_ylabel('Porcentagem')
                ax[1].set_xticklabels(bank_target_perc.index, rotation=45)

                st.pyplot(fig)
            else:
                st.warning('Nenhum dado disponível após os filtros.')
        else:
            st.error('Dados não carregados ou DataFrame vazio. Verifique o arquivo de entrada.')

if __name__ == '__main__':
    main()
