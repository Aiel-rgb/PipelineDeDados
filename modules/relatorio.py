import pandas as pd

def gerar_relatorio(alertas_lanc, alertas_conf, alertas_erp, caminho_saida):
    alertas_lanc["origem"] = "lancamentos"
    alertas_conf["origem"] = "conformidade"
    alertas_erp["origem"] = "erp"
    
    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
        alertas_lanc.to_excel(writer, sheet_name = "Lancamentos", index=False)
        alertas_conf.to_excel(writer, sheet_name = "Conformidade", index=False)
        alertas_erp.to_excel(writer, sheet_name = "ERP", index = False)

        consolidado = pd.concat([alertas_lanc, alertas_conf, alertas_erp], ignore_index=True)
        consolidado.to_excel(writer, sheet_name="Consolidado", index=False)