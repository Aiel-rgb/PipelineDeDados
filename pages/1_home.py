import streamlit as st
import pandas as pd
import plotly.express as px
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
    contagem = alertas_atual["tipo_anomalia"].value_counts().reset_index()
    contagem.columns = ["Tipo", "Quantidade"]

    fig = px.bar(
        contagem,
        x="Tipo",
        y="Quantidade",
        color="Tipo",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        text="Quantidade"
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1A1A2E"),
        hoverlabel=dict(bgcolor="#1A6EBD", font_color="white")
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

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







