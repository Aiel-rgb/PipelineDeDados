import pandas as pd


#Antes de lançar no git eu arrumar cada docstring
def ler_lancamentos(caminho):
    """
    Vai ler um arquivo excel e fazer reajustes em seus tipos para n haver erros nos bgl 
    """
    df = pd.read_excel(
        caminho,
        parse_dates=["Data"],
        dtype={
            "ID_Lancamento": str,
            "Centro_Custo": str,
            "Conta_Contabil": str,
            "Aprovado_Por": str
        }
    )
    df.columns = df.columns.str.strip()
    return df

def ler_conformidade(caminho):
    df = pd.read_excel(
        caminho,
        dtype={"ID_Controle":str}
    )
    df.columns = df.columns.str.strip()
    return df

def ler_erp(caminho):
    df = pd.read_csv(
        caminho,
        sep=';',
        encoding="utf-8",
        dtype={
            "NF_NUM":str,
            "CNPJ_EMITENTE": str,
            "CNPJ_DESTINATARIO": str
        }
    )
    df.columns = df.columns.str.strip()
    return df