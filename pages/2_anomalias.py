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

st.title("Anomalias Detectadas")

def colorir_anomalia(row):
    cores = {
        "DUPLICATA": "background-color: #FFE5E5",
        "VALOR_NEGATIVO": "background-color: #FFF3E0",
        "VALOR_ATÍPICO": "background-color: #FFF3E0",
        "SEM_APROVADOR": "background-color: #FFF9E0",
        "NÃO_CONFORME": "background-color: #FFE5E5",
        "SEM_DADOS": "background-color: #FFF9E0",
        "CNPJ_INVALIDO": "background-color: #FFE5E5",
    }
    cor = cores.get(row["tipo_anomalia"], "")
    return [cor] * len(row)

aba1, aba2, aba3 = st.tabs(["Lançamentos", "Conformidade", "ERP"])

with aba1:
    st.metric("Total de alertas", len(alertas_lanc))
    st.dataframe(
    alertas_lanc.style.apply(colorir_anomalia, axis=1),
    use_container_width=True
)

with aba2:
    st.metric("Total de alertas", len(alertas_conf))
    st.dataframe(
    alertas_conf.style.apply(colorir_anomalia, axis=1),
    use_container_width=True
)

with aba3:
    st.metric("Total de alertas", len(alertas_erp))
    st.dataframe(
    alertas_erp.style.apply(colorir_anomalia, axis=1),
    use_container_width=True
)
