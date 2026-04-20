import streamlit as st

def carregar_css(caminho):
    with open(caminho) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)