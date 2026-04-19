import streamlit as st
from modules import ingestao, limpeza, anomalias, relatorio
from modules.ia import comentar_anomalias, resumo_executivo
from pathlib import Path

BASE = Path(__file__).parent.parent
RAW = BASE / "Arquivos"
SAIDA = BASE / "outputs/relatorio_auditoria.xlsx"

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

st.title("🤖 Análise IA")

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