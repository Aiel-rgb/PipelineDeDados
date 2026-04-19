from modules import ingestao, limpeza, anomalias, relatorio
from pathlib import Path

BASE = Path(__file__).parent
RAW = BASE / "Arquivos"
SAIDA = BASE / "outputs/relatorio_auditoria.xlsx"

# 1. Ingestão
df_lanc = ingestao.ler_lancamentos(RAW / "lancamentos_contabeis.xlsx")
df_conf = ingestao.ler_conformidade(RAW / "relatorio_conformidade.xlsx")
df_erp = ingestao.ler_erp(RAW / "exportacao_erp.csv")

# 2. Limpeza
df_lanc = limpeza.limpar_lancamentos(df_lanc)
df_conf = limpeza.limpar_conformidade(df_conf)
df_erp = limpeza.limpar_erp(df_erp)

# 3. Anomalias 
alertas_lanc = anomalias.detectar_anomalias_lancamentos(df_lanc)
alertas_conf = anomalias.detectar_anomalias_conformidade(df_conf)
alertas_erp = anomalias.detectar_anomalias_erp(df_erp)

# 4. Relatório
SAIDA.parent.mkdir(parents=True, exist_ok=True)
relatorio.gerar_relatorio(alertas_lanc, alertas_conf, alertas_erp, SAIDA)