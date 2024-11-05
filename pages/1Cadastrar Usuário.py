import streamlit as st
from owlready2 import *

cols = st.columns([1,3,4])
cols[0].image("amazing_video.webp", width=100)
cols[1].title("Cadastrar Usuário")
st.markdown("---")

# Carregar a ontologia
onto = st.session_state.onto

# Função para obter todos os themeName distintos
def get_distinct_theme_names():
    return list(set([theme.themeName[0] if isinstance(theme.themeName, list) else theme.themeName 
                     for theme in onto.Tema.instances()]))

# Função para obter todos os intérpretes
def get_all_interpreters():
    return [interpreter.personName[0] if isinstance(interpreter.personName, list) else interpreter.personName 
            for interpreter in onto.Interprete.instances()]

# Função para adicionar um novo usuário
def add_user(name, age, email, whatsapp, preferred_genres, preferred_interpreters):
    with onto:

        user_count = len(list(onto.Usuario.instances()))
        user_id = f"usuario{user_count + 1}"

        new_user = onto.Usuario(user_id)
        new_user.userName.append(name)
        new_user.age.append(age)
        new_user.email.append(email)
        new_user.whatsapp.append(whatsapp)
        for genre in preferred_genres:
            theme = next((t for t in onto.Tema.instances() 
                          if t.themeName[0] == genre), None)
            if theme:
                new_user.prefersGenre.append(theme)
        for interpreter in preferred_interpreters:
            interp = next((i for i in onto.Interprete.instances() 
                           if i.personName[0] == interpreter), None)
            if interp:
                new_user.prefersInterpreter.append(interp)
    onto.save('ontologia_filmes.rdf')

# Layout em duas colunas
col1, col2 = st.columns(2)

with col1:
    user_name = st.text_input("Nome do usuário")
    user_age = st.number_input("Idade", min_value=0, max_value=120)
    user_email = st.text_input("E-mail")

with col2:
    user_whatsapp = st.text_input("WhatsApp")
    user_genres = st.multiselect("Gêneros preferidos", get_distinct_theme_names())
    user_interpreters = st.multiselect("Atores/Atrizes preferidos", get_all_interpreters())

# Centralizar o botão
_, col, _ = st.columns([1,2,1])

with col:
    if st.button("Adicionar Usuário", use_container_width=True):
        if user_name and user_age and user_email and user_whatsapp and user_genres and user_interpreters:
            add_user(user_name, user_age, user_email, user_whatsapp, user_genres, user_interpreters)
            st.success("Usuário adicionado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios (ID, Nome, Idade e E-mail).")

# Exibir usuários cadastrados
st.markdown("---")
st.subheader("Usuários Cadastrados")

users = onto.Usuario.instances()
if users:
    for user in users:
        with st.expander(f"Usuário: {user.userName[0]} (ID: {user.name})"):
            st.write(f"Idade: {user.age[0]}")
            st.write(f"E-mail: {user.email[0]}")
            st.write(f"WhatsApp: {user.whatsapp[0] if user.whatsapp else 'Não informado'}")
            st.write(f"Gêneros preferidos: {', '.join([g.themeName[0] for g in user.prefersGenre]) if user.prefersGenre else 'Nenhum'}")
            st.write(f"Intérpretes preferidos: {', '.join([i.personName[0] for i in user.prefersInterpreter]) if user.prefersInterpreter else 'Nenhum'}")
else:
    st.write("Nenhum usuário cadastrado ainda.")