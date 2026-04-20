import streamlit as st 
from modules import ingestao, limpeza, anomalias
from pathlib import Path
from modules.utils import carregar_css

BASE = Path(__file__).parent.parent
RAW = BASE / "Arquivos"

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

st.title("📊 Dados")

aba1, aba2, aba3 = st.tabs(["Lançamentos", "Conformidade", "ERP"])

with aba1:
    df_lanc["Data"] = df_lanc["Data"].dt.strftime("%d/%m/%Y")
    st.metric("Total de registros", len(df_lanc))
    st.dataframe(df_lanc, use_container_width=True)


with aba2:
    st.metric("Total de registros", len(df_conf))
    st.dataframe(df_conf, use_container_width=True)

with aba3:
    st.metric("Total de registros", len(df_erp))
    st.dataframe(df_erp, use_container_width=True)