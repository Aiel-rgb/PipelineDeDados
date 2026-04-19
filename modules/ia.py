import os 
from groq import Groq 
from dotenv import load_dotenv 
import pandas as pd

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

def comentar_anomalias(df_alertas):
    tabela = df_alertas.to_string(index=False)
    resposta = cliente.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Você é um auditor interno. Analise as anomalias abaixo e explique cada uma em linguagem simples para um gestor:\n\n{tabela}"
            }
        ]
    )

    return resposta.choices[0].message.content

def resumo_executivo(caminho_relatorio):
    conv = pd.read_excel(caminho_relatorio)
    tabela = conv.to_string(index=False)
    resposta = cliente.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Você como auiditor interno, analise bem esse relatorio de conformidades e explique cada uma em lingaugem simples para um gestor: \n\n {tabela}"
            }
        ]
    )
    return resposta.choices[0].message.content
