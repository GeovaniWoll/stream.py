# Imports
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Função para carregar os dados
@st.cache
def load_data(data_file):
    if data_file.name.endswith('.csv'):
        bank = pd.read_csv(data_file)
    elif data_file.name.endswith('.xlsx'):
        bank = pd.read_excel(data_file)
    else:
        st.error('Formato de arquivo inválido. Por favor, carregue um arquivo CSV ou Excel.')
        return None
    return bank

# Função para filtrar os dados com base nas seleções feitas pelo usuário
def multiselect_filter(df, column, selected_values):
    if 'all' in selected_values:
        return df
    return df[df[column].isin(selected_values)]

# Função para converter DataFrame em Excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title='Telemarketing analysis',
        page_icon='telemarketing_icon.png',
        layout="wide",
        initial_sidebar_state='expanded'
    )

    # Título principal da aplicação
    st.write('# Telemarketing analysis')
    st.markdown("---")
    
    # Apresenta a imagem na barra lateral da aplicação
    image = Image.open("Bank-Branding.jpg")
    st.sidebar.image(image)

    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])

    # Verifica se há conteúdo carregado na aplicação
    if data_file_1 is not None:
        bank_raw = load_data(data_file_1)
        bank = bank_raw.copy()

        st.write('## Antes dos filtros')
        st.write(bank_raw.head())

        # PROFISSÕES
        jobs_list = bank.job.unique().tolist()
        jobs_list.append('all')
        jobs_selected =  st.multiselect("Profissão", jobs_list, ['all'])

        # ESTADO CIVIL
        marital_list = bank.marital.unique().tolist()
        marital_list.append('all')
        marital_selected =  st.multiselect("Estado civil", marital_list, ['all'])

        # DEFAULT?
        default_list = bank.default.unique().tolist()
        default_list.append('all')
        default_selected =  st.multiselect("Default", default_list, ['all'])

        # TEM FINANCIAMENTO IMOBILIÁRIO?
        housing_list = bank.housing.unique().tolist()
        housing_list.append('all')
        housing_selected =  st.multiselect("Tem financiamento imob?", housing_list, ['all'])

        # TEM EMPRÉSTIMO?
        loan_list = bank.loan.unique().tolist()
        loan_list.append('all')
        loan_selected =  st.multiselect("Tem empréstimo?", loan_list, ['all'])

        # MEIO DE CONTATO?
        contact_list = bank.contact.unique().tolist()
        contact_list.append('all')
        contact_selected =  st.multiselect("Meio de contato", contact_list, ['all'])

        # MÊS DO CONTATO
        month_list = bank.month.unique().tolist()
        month_list.append('all')
        month_selected =  st.multiselect("Mês do contato", month_list, ['all'])

        # DIA DA SEMANA
        day_of_week_list = bank.day_of_week.unique().tolist()
        day_of_week_list.append('all')
        day_of_week_selected =  st.multiselect("Dia da semana", day_of_week_list, ['all'])

        submit_button = st.form_submit_button(label='Aplicar')

        # Restante do código ...

        st.write('## Proporção de aceite')

        # Calcula a proporção de aceite para os dados brutos
        bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True) * 100
        bank_raw_target_perc = bank_raw_target_perc.sort_index()

        # Calcula a proporção de aceite para os dados filtrados
        if not bank.empty:
            bank_target_perc = bank['y'].value_counts(normalize=True) * 100
            bank_target_perc = bank_target_perc.sort_index()

        if not bank_raw_target_perc.empty:
            # Gráfico de barras para os dados brutos
            fig, ax = plt.subplots(1, 2, figsize=(10, 5))
            sns.barplot(x=bank_raw_target_perc.index, y='y', data=bank_raw_target_perc.to_frame(), ax=ax[0])
            ax[0].set_title('Dados brutos', fontweight="bold")
            ax[0].set_xlabel('y')
            ax[0].set_ylabel('Porcentagem')
            ax[0].set_xticklabels(bank_raw_target_perc.index, rotation=45)

        if not bank_target_perc.empty:
            # Gráfico de barras para os dados filtrados
            sns.barplot(x=bank_target_perc.index, y='y', data=bank_target_perc.to_frame(), ax=ax[1])
            ax[1].set_title('Dados filtrados', fontweight="bold")
            ax[1].set_xlabel('y')
            ax[1].set_ylabel('Porcentagem')
            ax[1].set_xticklabels(bank_target_perc.index, rotation=45)

            # Exibe os gráficos
            st.pyplot(fig)

if __name__ == '__main__':
    main()
