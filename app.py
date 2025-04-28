import streamlit as st
import requests

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Clipping Futebol Brasil", layout="wide", page_icon="⚽")

st.title("⚽ Clipping de Notícias de Futebol - Brasil")

# API DE NOTÍCIAS (NewsAPI)
API_KEY = "d6aff0a3bfa3488099cbf265deef0656"  # <<<< Substitua aqui pela sua chave da NewsAPI

def buscar_noticias(query):
    url = f"https://newsapi.org/v2/everything?q={query}&language=pt&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error("Erro ao buscar notícias.")
        return []

# LISTA DE CLUBES
clubes = ['Botafogo', 'Flamengo', 'Palmeiras', 'São Paulo', 'Corinthians', 'Grêmio', 'Fluminense', 'Athletico-PR']

# FILTROS
st.sidebar.title("Filtros")
clube_selecionado = st.sidebar.selectbox("Selecione o Clube", ["Todos"] + clubes)
termo_busca = st.sidebar.text_input("Busca por palavra-chave")
quantidade_noticias = st.sidebar.slider("Quantas notícias mostrar?", 5, 50, 10)

# MONTAGEM DA QUERY
if clube_selecionado != "Todos":
    consulta = f"futebol {clube_selecionado}"
else:
    consulta = "futebol Brasil"

# Buscar notícias
noticias = buscar_noticias(consulta)

# Filtro adicional por texto
if termo_busca:
    noticias = [n for n in noticias if termo_busca.lower() in (n['title'] or '').lower()]

# Mostrar notícias
st.subheader(f"Exibindo {min(quantidade_noticias, len(noticias))} notícias")

for noticia in noticias[:quantidade_noticias]:
    with st.container():
        st.markdown("---")
        cols = st.columns([1, 3])
        if noticia.get('urlToImage'):
            cols[0].image(noticia['urlToImage'], use_column_width=True)
        cols[1].subheader(noticia['title'])
        if noticia.get('description'):
            cols[1].write(noticia['description'])
        cols[1].markdown(f"[Leia mais aqui]({noticia['url']})", unsafe_allow_html=True)