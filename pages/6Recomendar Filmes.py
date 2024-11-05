import streamlit as st
from owlready2 import *
from collections import defaultdict

onto = st.session_state.onto

st.title("Recomendação de Filmes")
st.markdown("---")

def get_all_users():
    return list(onto.Usuario.instances())

def get_user_ratings(user):
    return {rating.ratesMovie[0]: rating.ratingValue[0] for rating in user.hasRating} if hasattr(user, 'hasRating') else {}

def get_user_preferred_genres(user):
    return list(user.prefersGenre) if hasattr(user, 'prefersGenre') else []

def get_user_preferred_interpreters(user):
    return list(user.prefersInterpreter) if hasattr(user, 'prefersInterpreter') else []

def get_average_rating(movie):
    ratings = [rating.ratingValue[0] for rating in onto.Avaliacao.instances() if rating.ratesMovie[0] == movie]
    return sum(ratings) / len(ratings) if ratings else 0

def recommend_movies(user):
    user_ratings = get_user_ratings(user)
    preferred_genres = get_user_preferred_genres(user)
    preferred_interpreters = get_user_preferred_interpreters(user)
    
    all_movies = list(onto.Filme.instances())
    recommended_movies = []
    
    # Calcular a média das avaliações do usuário
    user_avg_rating = sum(user_ratings.values()) / len(user_ratings) if user_ratings else 0
    for movie in all_movies:
        if movie not in user_ratings:
            score = 0
            print(movie)
            # Pontuação baseada em gêneros preferidos
            genre_score = sum(2 for genre in movie.hasGenre if genre in preferred_genres)
            print(preferred_genres)
            print(genre_score)
            score += genre_score
            
            # Pontuação baseada em intérpretes preferidos
            interpreter_score = sum(2 for interpreter in movie.hasInterpreter if interpreter in preferred_interpreters)
            print(preferred_interpreters)
            print(interpreter_score)
            score += interpreter_score
            
            # Pontuação baseada na avaliação média do filme
            avg_rating = get_average_rating(movie)
            # print(avg_rating)
            if avg_rating > user_avg_rating:
                score += (avg_rating - user_avg_rating) * 2
            
            # Pontuação baseada em similaridade com filmes bem avaliados pelo usuário
            for rated_movie, rating in user_ratings.items():
                if rating > user_avg_rating:
                    common_genres = set(movie.hasGenre) & set(rated_movie.hasGenre)
                    common_interpreters = set(movie.hasInterpreter) & set(rated_movie.hasInterpreter)
                    similarity_score = len(common_genres) + len(common_interpreters)
                    print(similarity_score * (rating - user_avg_rating))
                    score += similarity_score * (rating - user_avg_rating)
            
            if score > 0:
                recommended_movies.append((movie, score))
    
    recommended_movies.sort(key=lambda x: x[1], reverse=True)
    return recommended_movies[:10]

users = get_all_users()
user_names = [u.userName[0] if isinstance(u.userName, list) else u.userName for u in users]

selected_user_name = st.selectbox("Escolha um usuário:", user_names)
selected_user = next(user for user in users if (user.userName[0] if isinstance(user.userName, list) else user.userName) == selected_user_name)

if st.button("Recomendar Filmes"):
    recommended_movies = recommend_movies(selected_user)
    
    st.markdown("---")
    st.write("Filmes Recomendados:")
    if recommended_movies:
        for i, (movie, score) in enumerate(recommended_movies):
            title = movie.originalTitle[0] if isinstance(movie.originalTitle, list) else movie.originalTitle
            year = movie.releaseYear[0] if isinstance(movie.releaseYear, list) else movie.releaseYear
            avg_rating = get_average_rating(movie)
            st.text(f"{i+1} - {title} ({year}) - Pontuação: {score} - Avaliação média: {avg_rating:.2f}")
    else:
        st.text("Não há recomendações disponíveis para este usuário.")

# import streamlit as st
# from owlready2 import *

# onto = st.session_state.onto

# st.title("Recomendação de Filmes")
# st.markdown("---")

# def get_all_users():
#     return list(onto.Usuario.instances())

# def get_user_ratings(user):
#     return [rating.ratesMovie[0] for rating in user.hasRating] if hasattr(user, 'hasRating') else []

# def get_user_preferred_genres(user):
#     return list(user.prefersGenre) if hasattr(user, 'prefersGenre') else []

# def get_user_preferred_interpreters(user):
#     return list(user.prefersInterpreter) if hasattr(user, 'prefersInterpreter') else []

# def recommend_movies(user):
#     rated_movies = get_user_ratings(user)
#     preferred_genres = get_user_preferred_genres(user)
#     preferred_interpreters = get_user_preferred_interpreters(user)
    
#     all_movies = list(onto.Filme.instances())
#     recommended_movies = []
    
#     for movie in all_movies:
#         if movie not in rated_movies:
#             score = 0
#             if any(genre in movie.hasGenre for genre in preferred_genres):
#                 score += 1
#             if any(interpreter in movie.hasInterpreter for interpreter in preferred_interpreters):
#                 score += 1
#             if score > 0:
#                 recommended_movies.append((movie, score))
    
#     recommended_movies.sort(key=lambda x: x[1], reverse=True)
#     return [movie for movie, _ in recommended_movies[:5]]  

# users = get_all_users()
# user_names = [u.userName[0] if isinstance(u.userName, list) else u.userName for u in users]

# selected_user_name = st.selectbox("Escolha um usuário:", user_names)
# selected_user = next(user for user in users if (user.userName[0] if isinstance(user.userName, list) else user.userName) == selected_user_name)

# if st.button("Recomendar Filmes"):
#     recommended_movies = recommend_movies(selected_user)
    
#     st.markdown("---")
#     st.write("Filmes Recomendados:")
#     if recommended_movies:
#         for i, movie in enumerate(recommended_movies):
#             title = movie.originalTitle[0] if isinstance(movie.originalTitle, list) else movie.originalTitle
#             year = movie.releaseYear[0] if isinstance(movie.releaseYear, list) else movie.releaseYear
#             st.text(f"{i+1} - {title} ({year})")
#     else:
#         st.text("Não há recomendações disponíveis para este usuário.")
    