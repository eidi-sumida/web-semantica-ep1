import streamlit as st
from owlready2 import *

st.title("Registro de Avaliação")

onto = st.session_state.onto

users = list(onto.Usuario.instances())
selected_user = st.selectbox("Selecione Usuário:", 
                             [u.userName[0] if isinstance(u.userName, list) else u.userName for u in users])

movies = list(onto.Filme.instances())
selected_movie = st.selectbox("Selecione Filme:", 
                              [m.originalTitle[0] if isinstance(m.originalTitle, list) else m.originalTitle for m in movies])

rating = st.selectbox("Avaliação (1-5):", [1,2,3,4,5])

if st.button("Registrar Avaliação"):

    user = next(u for u in users if (u.userName[0] if isinstance(u.userName, list) else u.userName) == selected_user)
    movie = next(m for m in movies if (m.originalTitle[0] if isinstance(m.originalTitle, list) else m.originalTitle) == selected_movie)
    
    existing_rating = next((r for r in user.hasRating if r.ratesMovie[0] == movie), None)
    
    if existing_rating:
        st.error("Este usuário já avaliou este filme. Não é possível adicionar outra avaliação.")
    
    else:
        rating_count = len(list(st.session_state.onto.Avaliacao.instances()))
        rating_id = f"avaliacao{rating_count + 1}"
        
        new_rating = onto.Avaliacao(rating_id)
        new_rating.ratesMovie = [movie]
        new_rating.ratingValue = [rating]
        
        user.hasRating.append(new_rating)
        
        st.session_state.onto.save('ontologia_filmes.rdf')
        st.success("Avaliação feita com sucesso!")

st.markdown("---")
st.write(f"Avaliação de {selected_user}")

user = next(u for u in users if (u.userName[0] if isinstance(u.userName, list) else u.userName) == selected_user)

if hasattr(user, 'hasRating'):
    for rating in user.hasRating:
        movie = rating.ratesMovie[0]
        text = f"""
Filme: {movie.originalTitle[0] if isinstance(movie.originalTitle, list) else movie.originalTitle}
Avaliação: {rating.ratingValue[0] if isinstance(rating.ratingValue, list) else rating.ratingValue}
"""
        st.text(text)
else:
    st.write("Este usuário não possui avaliação ainda.")