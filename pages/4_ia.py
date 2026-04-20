import streamlit as st
from modules import ingestao, limpeza, anomalias, relatorio
from modules.ia import comentar_anomalias, resumo_executivo
from pathlib import Path
from modules.utils import carregar_css


BASE = Path(__file__).parent.parent
RAW = BASE / "Arquivos"
SAIDA = BASE / "outputs/relatorio_auditoria.xlsx"

carregar_css(BASE / "assets/style.css")

df_lanc = ingestao.ler_lancamentos(RAW / "lancamentos_contabeis.xlsx")
df_conf = ingestao.ler_conformidade(RAW / "relatorio_conformidade.xlsx")
df_erp  = ingestao.ler_erp(RAW / "exportacao_erp.csv")

df_lanc = limpeza.limpar_lancamentos(df_lanc)
df_conf = limpeza.limpar_conformidade(df_conf)
df_erp  = limpeza.limpar_erp(df_erp)

alertas_lanc = anomalias.detectar_anomalias_lancamentos(df_lanc)
alertas_conf = anomalias.detectar_anomalias_conformidade(df_conf)
alertas_erp  = anomalias.detectar_anomalias_erp(df_erp)

SAIDA.parent.mkdir(parents=True, exist_ok=True)
relatorio.gerar_relatorio(alertas_lanc, alertas_conf, alertas_erp, SAIDA)

st.title("ARIA")

st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.aria-welcome {
    animation: fadeIn 1.5s ease-in-out;
    background: linear-gradient(135deg, #E8F4FD, #FFFFFF);
    border-left: 4px solid #1A6EBD;
    border-radius: 10px;
    padding: 20px 25px;
    margin-bottom: 25px;
    color: #1A1A2E;
    font-size: 16px;
    line-height: 1.7;
}
.aria-welcome strong {
    color: #1A6EBD;
    font-size: 18px;
}
</style>

<div class="aria-welcome">
    <strong>Olá, seja bem-vindo. Sou a ARIA</strong> — Auditoria e Risco com Inteligência Artificial.<br><br>
    Estou aqui para analisar os dados do pipeline, identificar anomalias e responder suas dúvidas 
    sobre auditoria interna, contabilidade e compliance.<br><br>
    Use os botões abaixo para uma análise rápida ou digite sua pergunta diretamente no chat.
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

col1, col2 = st.columns(2)

with col1:
    if st.button("📋 Analisar anomalias"):
        resposta = comentar_anomalias(alertas_lanc)
        st.session_state.messages.append({"role":"assistant", "content": resposta})
        st.rerun()

with col2:
    if st.button("📄 Resumo executivo"):
        resposta = resumo_executivo(SAIDA)
        st.session_state.messages.append({"role":"assistant", "content": resposta})
        st.rerun()

if prompt := st.chat_input("Pergunte ao auditor IA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    resposta = comentar_anomalias(alertas_lanc)
    st.session_state.messages.append({"role": "assistant", "content":resposta})
    st.rerun()