import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 🔐 pega do Streamlit Secrets
USER = st.secrets["USER_ADMIN"]
PASS = st.secrets["PASS_ADMIN"]

USERS = {
    USER: hash_password(PASS)
}

def check_login(username, password):
    return USERS.get(username) == hash_password(password)

def login():
    st.title("🔐 Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")