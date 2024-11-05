import streamlit as st
import pandas as pd
from owlready2 import *

cols = st.columns([1,3,4])
cols[0].image("amazing_video.webp", width=100)
cols[1].title("Listar Filmes")
st.markdown("---")

def get_movie_details(movie):
    directors = [director.personName[0] if isinstance(director.personName, list) else director.personName for director in movie.hasDirector]
    interpreters = [interpreter.personName[0] if isinstance(interpreter.personName, list) else interpreter.personName for interpreter in movie.hasInterpreter]
    genres = [genre.themeName[0] if isinstance(genre.themeName, list) else genre.themeName for genre in movie.hasGenre]
    ratings = [rating.ratingValue[0] if isinstance(rating.ratingValue, list) else rating.ratingValue 
               for rating in st.session_state.onto.Avaliacao.instances() 
               if rating.ratesMovie[0] == movie]
    
    avg_rating = f"{sum(ratings) / len(ratings):.1f}" if ratings else "-"

    return {
        "Título Original": movie.originalTitle[0] if isinstance(movie.originalTitle, list) else movie.originalTitle,
        "Título em Português": movie.portugueseTitle[0] if isinstance(movie.portugueseTitle, list) else movie.portugueseTitle,
        "Ano de Produção": movie.productionYear[0] if isinstance(movie.productionYear, list) else movie.productionYear,
        "Ano de Lançamento": movie.releaseYear[0] if isinstance(movie.releaseYear, list) else movie.releaseYear,
        "Diretor(es)": ", ".join(directors),
        "Intérpretes": ", ".join(interpreters),
        "Gêneros": ", ".join(genres),
        "Nacionalidade": movie.nationality[0] if isinstance(movie.nationality, list) else movie.nationality,
        "Idioma Original": movie.originalLanguage[0] if isinstance(movie.originalLanguage, list) else movie.originalLanguage,
        "Avaliação Média": avg_rating,
        "Número de Avaliações": len(ratings)
    }

# Exibir detalhes de um filme específico
if st.session_state.onto.Filme.instances():
    selected_movie = st.selectbox("Selecione um filme para ver mais detalhes:", 
                                  [movie.originalTitle[0] if isinstance(movie.originalTitle, list) else movie.originalTitle 
                                   for movie in st.session_state.onto.Filme.instances()])
    
    if selected_movie:
        movie = next(movie for movie in st.session_state.onto.Filme.instances() 
                     if (movie.originalTitle[0] if isinstance(movie.originalTitle, list) else movie.originalTitle) == selected_movie)
        
        cols = st.columns([1,1,1])
        movie_details = get_movie_details(movie)
        for key, value in movie_details.items():
            cols[0].write(f"**{key}:** {value}")
        
        cols[1].write("**Avaliações individuais:**")
        ratings = [rating for rating in st.session_state.onto.Avaliacao.instances() if rating.ratesMovie[0] == movie]
        for rating in ratings:
            user = next(user for user in st.session_state.onto.Usuario.instances() if rating in user.hasRating)
            user_name = user.userName[0] if isinstance(user.userName, list) else user.userName
            rating_value = rating.ratingValue[0] if isinstance(rating.ratingValue, list) else rating.ratingValue
            cols[1].write(f"- {user_name}: {rating_value} estrelas")
else:
    st.write("Nenhum filme encontrado na base de dados.")

st.markdown("---")

list_option = st.selectbox("Listar por:", ["Todos", "Ator/Atriz", "Gênero"])

if list_option == "Todos":
    movies = [get_movie_details(movie) for movie in st.session_state.onto.Filme.instances()]
    df = pd.DataFrame(movies)
    st.table(df)


elif list_option == "Ator/Atriz":

    interpreters = list(set([interpreter.personName[0] if isinstance(interpreter.personName, list) else interpreter.personName 
                             for movie in st.session_state.onto.Filme.instances() 
                             for interpreter in movie.hasInterpreter]))
    
    interpreters.sort()
    
    selected_actor = st.selectbox("Selecione um Ator/Atriz", interpreters)

    if selected_actor:
        movies = [get_movie_details(movie) for movie in st.session_state.onto.Filme.instances() 
                  if any(selected_actor.lower() in (interpreter.personName[0] if isinstance(interpreter.personName, list) else interpreter.personName).lower() 
                         for interpreter in movie.hasInterpreter)]
        if movies:
            df = pd.DataFrame(movies)
            st.table(df)
        else:
            st.write("Nenhum filme encontrado para este ator/atriz.")

elif list_option == "Gênero":
    genres = list(set([genre.themeName[0] if isinstance(genre.themeName, list) else genre.themeName 
                       for movie in st.session_state.onto.Filme.instances() 
                       for genre in movie.hasGenre]))
    genre = st.selectbox("Gênero", genres)
    movies = [get_movie_details(movie) for movie in st.session_state.onto.Filme.instances() 
              if any(genre.lower() == (g.themeName[0] if isinstance(g.themeName, list) else g.themeName).lower() for g in movie.hasGenre)]
    if movies:
        df = pd.DataFrame(movies)
        st.table(df)
    else:
        st.write("Nenhum filme encontrado para este gênero.")

