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

st.markdown("""
<h1>
    <i class="fa-solid fa-magnifying-glass" style="color:#1A6EBD"></i> ARGOS
</h1>
""", unsafe_allow_html=True)
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
    st.subheader("Distribuição de anomalias")
    fig_pizza = px.pie(
        contagem,
        values="Quantidade",
        names="Tipo",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig_pizza.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1A1A2E"),
        showlegend=True
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

with col4:
    st.subheader("Valores por lançamento")
    if fonte == "Lançamentos":
        fig_linha = px.line(
            df_atual,
            x="Data",
            y="Valor_BRL",
            markers=True,
            color_discrete_sequence=["#1A6EBD"]
        )
    elif fonte == "ERP":
        fig_linha = px.line(
            df_atual,
            x="EMISSAO",
            y="VALOR_TOTAL",
            markers=True,
            color_discrete_sequence=["#1A6EBD"]
        )
    else:
        fig_linha = px.line(
            df_atual.reset_index(),
            x="index",
            y=df_atual.select_dtypes("number").columns[0],
            markers=True,
            color_discrete_sequence=["#1A6EBD"]
        )
    fig_linha.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1A1A2E")
    )
    st.plotly_chart(fig_linha, use_container_width=True)






