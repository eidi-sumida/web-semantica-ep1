import streamlit as st
from owlready2 import *
import os

# Carregando a ontologia
onto_path.append(".")
onto = get_ontology("amazingVideo.rdf")
onto.load()

# Função para adicionar um novo usuário
def add_user(name, age, email, whatsapp, preferred_genres, preferred_actors):
    with onto:
        new_user = onto.User(name)
        new_user.userAge = [age]
        new_user.userEmail = [email]
        new_user.userWhatsApp = [whatsapp]
        for genre in preferred_genres:
            new_user.userPreferredGenre.append(onto[genre])
        for actor in preferred_actors:
            new_user.userPreferredActor.append(onto[actor])
    onto.save()

# Função para adicionar um novo filme
def add_movie(title, original_title, release_year, director, actors, genres, nationality, language):
    with onto:
        new_movie = onto.Movie(title)
        new_movie.hasTitle = [title]
        new_movie.hasOriginalTitle = [original_title]
        new_movie.hasReleaseYear = [release_year]
        new_movie.hasDirector = [onto[director]]
        for actor in actors:
            new_movie.hasActor.append(onto[actor])
        for genre in genres:
            new_movie.hasGenre.append(onto[genre])
        new_movie.hasNationality = [nationality]
        new_movie.hasOriginalLanguage = [language]
    onto.save()

# Função para recomendar filmes
def recommend_movies(user):
    recommended = []
    user_genres = set(user.userPreferredGenre)
    user_actors = set(user.userPreferredActor)
    
    for movie in onto.Movie.instances():
        movie_genres = set(movie.hasGenre)
        movie_actors = set(movie.hasActor)
        
        genre_match = len(user_genres.intersection(movie_genres))
        actor_match = len(user_actors.intersection(movie_actors))
        
        if genre_match > 0 or actor_match > 0:
            score = genre_match + actor_match
            recommended.append((movie, score))
    
    return sorted(recommended, key=lambda x: x[1], reverse=True)

# Interface Streamlit
st.title("Amazing Video - Sistema de Recomendação de Filmes")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Usuário", "Cadastrar Filme", "Recomendações", "Listar Filmes"])

if menu == "Cadastrar Usuário":
    st.header("Cadastro de Usuário")
    name = st.text_input("Nome")
    age = st.number_input("Idade", min_value=0, max_value=120)
    email = st.text_input("E-mail")
    whatsapp = st.text_input("WhatsApp")
    preferred_genres = st.multiselect("Gêneros Preferidos", [g.name for g in onto.Genre.instances()])
    preferred_actors = st.multiselect("Atores Preferidos", [a.name for a in onto.Actor.instances()])
    
    if st.button("Cadastrar"):
        add_user(name, age, email, whatsapp, preferred_genres, preferred_actors)
        st.success("Usuário cadastrado com sucesso!")

elif menu == "Cadastrar Filme":
    st.header("Cadastro de Filme")
    title = st.text_input("Título")
    original_title = st.text_input("Título Original")
    release_year = st.number_input("Ano de Lançamento", min_value=1800, max_value=2100)
    director = st.selectbox("Diretor", [d.name for d in onto.Director.instances()])
    actors = st.multiselect("Atores", [a.name for a in onto.Actor.instances()])
    genres = st.multiselect("Gêneros", [g.name for g in onto.Genre.instances()])
    nationality = st.text_input("Nacionalidade")
    language = st.text_input("Idioma Original")
    
    if st.button("Cadastrar"):
        add_movie(title, original_title, release_year, director, actors, genres, nationality, language)
        st.success("Filme cadastrado com sucesso!")

elif menu == "Recomendações":
    st.header("Recomendações de Filmes")
    user = st.selectbox("Selecione um usuário", [u.name for u in onto.User.instances()])
    
    if st.button("Recomendar"):
        recommendations = recommend_movies(onto[user])
        for movie, score in recommendations:
            st.write(f"{movie.hasTitle[0]} (Score: {score})")

elif menu == "Listar Filmes":
    st.header("Listagem de Filmes")
    filter_type = st.selectbox("Filtrar por", ["Ator", "Gênero", "Nacionalidade"])
    
    if filter_type == "Ator":
        actor = st.selectbox("Selecione um ator", [a.name for a in onto.Actor.instances()])
        movies = [m for m in onto.Movie.instances() if onto[actor] in m.hasActor]
    elif filter_type == "Gênero":
        genre = st.selectbox("Selecione um gênero", [g.name for g in onto.Genre.instances()])
        movies = [m for m in onto.Movie.instances() if onto[genre] in m.hasGenre]
    else:
        nationality = st.text_input("Digite a nacionalidade")
        movies = [m for m in onto.Movie.instances() if nationality in m.hasNationality]
    
    for movie in movies:
        st.write(f"{movie.hasTitle[0]} ({movie.hasReleaseYear[0]})")