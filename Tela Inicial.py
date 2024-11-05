import streamlit as st
from owlready2 import *

# Carregando a ontologia
onto = get_ontology("ontologia_filmes.rdf").load()

st.set_page_config(page_title="Sistema de Recomendação de Filmes", page_icon="amazing_video.webp", layout="wide")

st.image("amazing_video.webp", width=250)

st.title("Amazing Video")
st.write("Bem-vindo ao Sistema de Recomendação de Filmes")
st.write("Use o menu à esquerda para navegar :D")

# Criando uma sessão de estado para armazenar a ontologia
if 'onto' not in st.session_state:
    st.session_state.onto = onto