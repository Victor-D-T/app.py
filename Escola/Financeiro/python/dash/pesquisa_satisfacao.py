import pandas as pd
import streamlit as st
import plotly.express as px
import os 
# Carregar os dados
@st.cache_data

def carregar_dados():
    print(os.getcwd(), 'Escola', 'Financeiro', 'python', 'dash')
    xlsx = pd.ExcelFile(os.path.join(os.getcwd(), 'Escola', 'Financeiro', 'python', 'dash', "pesquisa.xlsx"))
    df_list = []
    for unidade in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=unidade)
        df['Unidade'] = unidade
        df_list.append(df)
    df_total = pd.concat(df_list, ignore_index=True)

    colunas_relevantes = [
        'TURMA',
        'DATA DA LIGAÇÃO',
        'Esta com acesso a agenda?',
        'Recebeu o plano de estudo?',
        'Ciência dos diferenciais da unidade? Ex. Ballet, Karatê... , ',
        'Usa transporte? Está satisfeito?',
        'Elogios',
        'Reclamação',
        'Unidade'
    ]

    df = df_total[colunas_relevantes].copy()
    df.columns = [
        'Turma', 'Data', 'Acesso_agenda', 'Plano_estudos',
        'Conhece_diferenciais', 'Satisfacao_transporte',
        'Elogios', 'Reclamacoes', 'Unidade']
    return df

# Função para criar gráficos

def gerar_grafico(df, coluna, titulo):
    df_temp = df[coluna].value_counts(dropna=False).reset_index()
    df_temp.columns = ['Resposta', 'Quantidade']
    fig = px.bar(df_temp, x='Resposta', y='Quantidade', text='Quantidade',
                 title=titulo, labels={'Resposta': 'Resposta', 'Quantidade': 'Quantidade'})
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title='Quantidade de Respostas', xaxis_title='Resposta')
    return fig

# App Streamlit
st.set_page_config(page_title="Dashboard de Satisfação", layout="wide")
st.title("Dashboard de Satisfação dos Responsáveis")

# Carregar dados
df = carregar_dados()

# Filtros
unidades = df['Unidade'].dropna().unique()
unidade_selecionada = st.sidebar.multiselect("Filtrar por unidade:", unidades, default=list(unidades))

df_filtrado = df[df['Unidade'].isin(unidade_selecionada)]

# Layout dos gráficos
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(gerar_grafico(df_filtrado, 'Acesso_agenda', 'Acesso à Agenda'), use_container_width=True)
    st.plotly_chart(gerar_grafico(df_filtrado, 'Conhece_diferenciais', 'Conhecimento dos Diferenciais'), use_container_width=True)

with col2:
    st.plotly_chart(gerar_grafico(df_filtrado, 'Plano_estudos', 'Recebimento do Plano de Estudos'), use_container_width=True)
    st.plotly_chart(gerar_grafico(df_filtrado, 'Satisfacao_transporte', 'Satisfação com o Transporte'), use_container_width=True)

# Elogios e Reclamações
st.subheader("Elogios")
st.write(df_filtrado['Elogios'].dropna().unique())

st.subheader("Reclamações")
st.write(df_filtrado['Reclamacoes'].dropna().unique())
