import streamlit as st
from owlready2 import *

cols = st.columns([1,3,4])
cols[0].image("amazing_video.webp", width=100)
cols[1].title("Cadastrar Filme")
st.markdown("---")

# Funções auxiliares para obter listas de entidades existentes
def get_existing_interpreters():
    return [(i.name, i.personName[0]) for i in st.session_state.onto.Interprete.instances()]

def get_existing_directors():
    return [(d.name, d.personName[0]) for d in st.session_state.onto.Diretor.instances()]

def get_existing_themes():
    return [(t.name, t.themeName[0]) for t in st.session_state.onto.Tema.instances()]

# Função para adicionar um novo filme
def add_movie(title, portuguese_title, year, release_year, directors, interpreters, genres, nationality, original_language):
    with st.session_state.onto:

        movie_count = len(list(st.session_state.onto.Filme.instances()))
        movie_id = f"filme{movie_count + 1}"

        new_movie = st.session_state.onto.Filme(movie_id)
        new_movie.originalTitle.append(title)
        new_movie.portugueseTitle.append(portuguese_title)
        new_movie.productionYear.append(year)
        new_movie.releaseYear.append(release_year)
        new_movie.nationality.append(nationality)
        new_movie.originalLanguage.append(original_language)

        # Adicionar diretores
        for director in directors:
            director_instance = st.session_state.onto.Diretor(director)
            new_movie.hasDirector.append(director_instance)

        # Adicionar intérpretes
        for interpreter in interpreters:
            interpreter_instance = st.session_state.onto.Interprete(interpreter)
            new_movie.hasInterpreter.append(interpreter_instance)

        # Adicionar gêneros
        for genre in genres:
            genre_instance = st.session_state.onto.Tema(genre)
            new_movie.hasGenre.append(genre_instance)

    st.session_state.onto.save('ontologia_filmes.rdf')

# Layout em duas colunas
col1, col2 = st.columns(2)

with col1:
    movie_title = st.text_input("Título original do filme")
    movie_portuguese_title = st.text_input("Título em português do filme")
    movie_year = st.number_input("Ano de produção", min_value=1800, max_value=2024)
    movie_release_year = st.number_input("Ano de lançamento", min_value=1800, max_value=2024)
    movie_original_language = st.text_input("Idioma original")

with col2:
    movie_nationality = st.text_input("Nacionalidade")

    existing_directors = get_existing_directors()
    movie_directors = st.multiselect("Diretores", options=existing_directors, format_func=lambda x: x[1])

    existing_interpreters = get_existing_interpreters()
    movie_interpreters = st.multiselect("Atores/Atrizes", options=existing_interpreters, format_func=lambda x: x[1])

    existing_themes = get_existing_themes()
    movie_genres = st.multiselect("Gêneros", options=existing_themes, format_func=lambda x: x[1])




if st.button("Adicionar Filme"):
    if movie_title and movie_portuguese_title and movie_year and movie_release_year and movie_directors and movie_interpreters and movie_genres and movie_nationality and movie_original_language:
        add_movie(
            movie_title,
            movie_portuguese_title, 
            movie_year, 
            movie_release_year, 
            [d[0] for d in movie_directors], 
            [i[0] for i in movie_interpreters], 
            [g[0] for g in movie_genres], 
            movie_nationality, 
            movie_original_language
        )
        st.success("Filme adicionado com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos.")

# Exibir filmes cadastrados
st.markdown("---")
st.subheader("Filmes Cadastrados")

movies = st.session_state.onto.Filme.instances()
if movies:
    for movie in movies:
        with st.expander(f"Filme: {movie.originalTitle[0]} (ID: {movie.name})"):
            st.write(f"Título em português: {movie.portugueseTitle[0]}")
            st.write(f"Ano de produção: {movie.productionYear[0]}")
            st.write(f"Ano de lançamento: {movie.releaseYear[0]}")
            st.write(f"Diretores: {', '.join([d.personName[0] for d in movie.hasDirector]) if movie.hasDirector else 'Não informado'}")
            st.write(f"Intérpretes: {', '.join([i.personName[0] for i in movie.hasInterpreter]) if movie.hasInterpreter else 'Nenhum'}")
            st.write(f"Gêneros: {', '.join([g.themeName[0] for g in movie.hasGenre]) if movie.hasGenre else 'Nenhum'}")
            st.write(f"Nacionalidade: {movie.nationality[0]}")
            st.write(f"Idioma original: {movie.originalLanguage[0]}")
else:
    st.write("Nenhum filme cadastrado ainda.")