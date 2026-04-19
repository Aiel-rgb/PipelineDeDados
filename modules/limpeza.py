import pandas as pd

def limpar_lancamentos(df):
    for col in ["Status","Tipo","Moeda"]:
        df[col] = df[col].str.strip().str.upper()
    df["Aprovado_Por"] = df["Aprovado_Por"].fillna("SEM_APROVADOR")
    return df 

def limpar_conformidade(df):
    for col in ["Status_Controle", "Periodicidade"]:
        df[col] = df[col].str.strip().str.upper()
    for fill in ["Observacoes","Ultima_Execucao"]:
        df[fill] = df[fill].fillna("SEM_DADOS")
    return df
def limpar_erp(df):
    for col in ["FORMA_PGTO", "CATEGORIA"]:
        df[col] = df[col].str.strip().str.upper()
    df["OBSERVACAO"] = df["OBSERVACAO"].fillna("SEM_OBSERVACAO")

    #Resolver separação do csv
    for csv in ["VALOR_TOTAL", "VALOR_IMPOSTOS"]:
        df[csv] = df[csv].astype(str).str.replace(",",".").astype(float)
    return df