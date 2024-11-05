import streamlit as st

st.title("Visualizar o arquivo RDF")

st.markdown("---")

with open('ontologia_filmes.rdf', "r", encoding="utf-8") as file:
    rdf_content = file.read()

# Exibe o conteúdo do arquivo
st.code(rdf_content, language="xml")
