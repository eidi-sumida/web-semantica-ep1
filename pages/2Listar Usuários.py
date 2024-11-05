import streamlit as st
import pandas as pd
from owlready2 import *

cols = st.columns([1,3,4])
cols[0].image("amazing_video.webp", width=100)
cols[1].title("Listar Usuários")
st.markdown("---")

# Função para obter informações dos usuários
def get_user_info(user):
    preferred_genres = [genre.themeName[0] for genre in user.prefersGenre]
    preferred_interpreters = [interpreter.personName[0] for interpreter in user.prefersInterpreter]
    
    return {
        "ID do usuário": user.name,
        "Nome de usuário": user.userName[0],
        "Idade": user.age[0],
        "Email": user.email[0],
        "WhatsApp": user.whatsapp[0],
        "Gêneros preferidos": ", ".join(preferred_genres),
        "Ator/Atriz preferidos": ", ".join(preferred_interpreters)
    }

# Carregar a ontologia
onto = st.session_state.onto

# Obter todos os usuários
users = list(onto.Usuario.instances())

if users:
    # Criar uma lista de dicionários com as informações dos usuários
    user_data = [get_user_info(user) for user in users]

    # Opção para exibir detalhes de um usuário específico
    selected_user = st.selectbox("Selecione um usuário para ver avaliações:", [user.userName[0] for user in users])
    
    if selected_user:
        user = next(user for user in users if user.userName[0] == selected_user)
        st.subheader(f"Avaliações do usuário: {selected_user}")
        
        for rating in user.hasRating:
            print(user.userName[0])
            print(rating)
            st.write(f"- {rating.ratesMovie[0].originalTitle[0]}: {rating.ratingValue[0]} estrelas")
            # st.write(f"- {rating.ratesMovie[0].originalTitle[0]}: {rating.ratingValue[0]} estrelas ({rating.name}, {user.name})")

    st.markdown("---")
    # Criar um DataFrame com as informações dos usuários
    df = pd.DataFrame(user_data)
    
    # Exibir o DataFrame
    st.write(df)


else:
    st.write("Nenhum usuário encontrado na base de dados.")