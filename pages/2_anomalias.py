import streamlit as st 
from modules import ingestao, limpeza, anomalias
from pathlib import Path

BASE = Path(__file__).parent.parent
RAW = BASE / "Arquivos"

df_lanc = ingestao.ler_lancamentos(RAW / "lancamentos_contabeis.xlsx")
df_conf = ingestao.ler_conformidade(RAW / "relatorio_conformidade.xlsx")
df_erp = ingestao.ler_erp(RAW / "exportacao_erp.csv")

df_lanc = limpeza.limpar_lancamentos(df_lanc)
df_conf = limpeza.limpar_conformidade(df_conf)
df_erp = limpeza.limpar_erp(df_erp)

alertas_lanc = anomalias.detectar_anomalias_lancamentos(df_lanc)
alertas_conf = anomalias.detectar_anomalias_conformidade(df_conf)
alertas_erp = anomalias.detectar_anomalias_erp(df_erp)

st.title("Anomalias Detectadas")

aba1, aba2, aba3 = st.tabs(["Lançamentos", "Conformidade", "ERP"])

with aba1:
    st.metric("Total de alertas", len(alertas_lanc))
    st.dataframe(alertas_lanc, use_container_width=True)

with aba2:
    st.metric("Total de alertas", len(alertas_conf))
    st.dataframe(alertas_conf, use_container_width=True)

with aba3:
    st.metric("Total de alertas", len(alertas_erp))
    st.dataframe(alertas_erp, use_container_width=True)
