import streamlit as st
import pandas as pd
from modules import ingestao, limpeza, anomalias
from pathlib import Path

BASE = Path(__file__).parent.parent 
RAW = BASE / "Arquivos"

def carregar_css(caminho):
    with open(caminho) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_css(BASE / "assets/style.css")

df_lanc = ingestao.ler_lancamentos(RAW / "lancamentos_contabeis.xlsx")
df_conf = ingestao.ler_conformidade(RAW / "relatorio_conformidade.xlsx")
df_erp = ingestao.ler_erp(RAW / "exportacao_erp.csv")

df_lanc = limpeza.limpar_lancamentos(df_lanc)
df_conf = limpeza.limpar_conformidade(df_conf)
df_erp = limpeza.limpar_erp(df_erp)

alertas_lanc = anomalias.detectar_anomalias_lancamentos(df_lanc)
alertas_conf = anomalias.detectar_anomalias_conformidade(df_conf)
alertas_erp = anomalias.detectar_anomalias_erp(df_erp)

st.title("🔍 Auditoria Interna")
fonte = st.selectbox("Selecione a fonte:", ["Lançamentos", "Conformidade", "ERP"])

if fonte == "Lançamentos":
    df_atual = df_lanc
    alertas_atual = alertas_lanc
elif fonte == "Conformidade":
    df_atual = df_conf
    alertas_atual = alertas_conf
else:
    df_atual = df_erp
    alertas_atual = alertas_erp

col1, col2 = st.columns([1.5,1])

with col1:
    st.subheader("Anomalias por tipo")
    st.bar_chart(alertas_atual["tipo_anomalia"].value_counts(), color="#1A6EBD")

with col2:
    st.subheader("Métricas")
    st.metric("Total de registros", len(df_atual))
    st.metric("Anomalias detectadas", len(alertas_atual))
    st.metric("% com anomalia", f"{round(len(alertas_atual)/len(df_atual)*100, 1)}%")

st.divider()
col3, col4 = st.columns([1.5,1])

with col3:
    st.markdown("**Sobre o pipeline**")
    st.markdown("Pipeline de auditoria interna que detecta automaticamente inconsistências em lançamentos contábeis, relatórios de conformidade e exportações de ERP.")

with col4:
    st.selectbox("Visualizar tabela:", ["Dados brutos", "Apenas anomalias"], key="tabela")
    if st.session_state.tabela == "Dados brutos":
        st.dataframe(df_atual.head(5), use_container_width=True)
    else:
        st.dataframe(alertas_atual.head(5), use_container_width=True)







