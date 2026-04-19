import pandas as pd

def detectar_anomalias_lancamentos(df):
    alertas = []
    #Duplicatas
    dup = df[df.duplicated(subset=["Centro_Custo","Conta_Contabil","Valor_BRL","Aprovado_Por"], keep=False)].copy()
    if not dup.empty:
        dup["tipo_anomalia"] = "DUPLICATA"
        dup["detalhe"] = "Lançamento duplicado"
        alertas.append(dup[["ID_Lancamento", "tipo_anomalia", "detalhe"]])

    #Sem aprovador
    sem_ap = df[df["Aprovado_Por"] == "SEM_APROVADOR"].copy()
    if not sem_ap.empty:
        sem_ap["tipo_anomalia"] = "SEM_APROVADOR"
        sem_ap["detalhe"] = "Lançamento sem aprovador"
        alertas.append(sem_ap[["ID_Lancamento","tipo_anomalia","detalhe"]])
    
    #Valor negativo
    val_neg = df[df["Valor_BRL"] < 0].copy()
    if not val_neg.empty:
        val_neg["tipo_anomalia"] = "VALOR_NEGATIVO"
        val_neg["detalhe"] = "Valor está negativo"
        alertas.append(val_neg[["ID_Lancamento", "tipo_anomalia", "detalhe"]])

    #Valor atípico
    val_atp = df[df["Valor_BRL"] > 500000].copy()
    if not val_atp.empty:
        val_atp["tipo_anomalia"] = "VALOR_ATÍPICO"
        val_atp["detalhe"] = "Valor está maior q o esperado"
        alertas.append(val_atp[["ID_Lancamento", "tipo_anomalia", "detalhe"]])

    return pd.concat(alertas, ignore_index=True) if alertas else pd.DataFrame()

def detectar_anomalias_conformidade(df):
    alertas = []

    #NÃO CONFORME
    n_conf = df[df["Status_Controle"] == "NÃO CONFORME"].copy()
    if not n_conf.empty:
        n_conf["tipo_anomalia"] = "NÃO_CONFORME"
        n_conf["detalhe"] = "Status não está conforme o planejado"
        alertas.append(n_conf[["ID_Controle", "tipo_anomalia", "detalhe"]])
    
    #SEM DADOS
    sem_dados = df[df["Ultima_Execucao"] == "SEM_DADOS"].copy()
    if not sem_dados.empty:
        sem_dados["tipo_anomalia"] = "SEM_DADOS"
        sem_dados["detalhe"] = "Status não está conforme o planejado"
        alertas.append(sem_dados[["ID_Controle","tipo_anomalia","detalhe"]])
    
    return pd.concat(alertas, ignore_index=True) if alertas else pd.DataFrame()

def detectar_anomalias_erp(df):
    alertas =  []

    #CNPJ Invalido
    cnpj_inv = df[df["CNPJ_EMITENTE"] == "00.000.000/0001-00"].copy()
    if not cnpj_inv.empty:
        cnpj_inv["tipo_anomalia"] = "CNPJ_INVALIDO"
        cnpj_inv["detalhe"] = "CNPJ está invalido"
        alertas.append(cnpj_inv[["NF_NUM", "tipo_anomalia", "detalhe"]])
    
    #Valor negativo
    val_neg = df[df["VALOR_TOTAL"] < 0].copy()
    if not val_neg.empty:
        val_neg["tipo_anomalia"] = "VALOR_NEGATIVO"
        val_neg["detalhe"] = "O valor está negativo"
        alertas.append(val_neg[["NF_NUM", "tipo_anomalia", "detalhe"]])
    
    #Valor atípico
    val_atp = df[df["VALOR_TOTAL"] > 500000].copy()
    if not val_atp.empty:
        val_atp["tipo_anomalia"] = "VALOR_ATIPICO"
        val_atp["detalhe"] = "O valor está mais alto que o esperado"
        alertas.append(val_atp[["NF_NUM", "tipo_anomalia", "detalhe"]])
    
    #Duplicata
    dup = df[df.duplicated(subset=["CNPJ_EMITENTE", "VALOR_TOTAL"], keep=False)].copy()
    if not dup.empty:
        dup["tipo_anomalia"] = "DUPLICATA"
        dup["detalhe"] = "Mesmo CNPJ e valor"
        alertas.append(dup[["NF_NUM", "tipo_anomalia", "detalhe"]])
    
    return pd.concat(alertas, ignore_index=True) if alertas else pd.DataFrame()