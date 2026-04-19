import streamlit as st

st.set_page_config(
    page_title="Pipeline de Auditoria",
    page_icon="🔍",
    layout="wide"
)

paginas = {
    "home": st.Page("pages/1_home.py", title="Home", icon="🏠"),
    "anomalias": st.Page("pages/2_anomalias.py", title="Anomalias", icon="⚠️"),
    "dados": st.Page("pages/3_dados.py", title="Dados", icon="📊"),
    "ia": st.Page("pages/4_ia.py", title="Análise IA", icon="🤖"),
}

nav = st.navigation(list(paginas.values()))
nav.run()