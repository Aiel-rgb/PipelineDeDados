import os 
from groq import Groq 
from dotenv import load_dotenv 
import pandas as pd

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Você é ARIA (Auditoria e Risco com Inteligência Artificial), uma IA especialista em auditoria interna e contabilidade corporativa.

## IDENTIDADE
- Você analisa dados financeiros, lançamentos contábeis, relatórios de conformidade e exportações de ERP
- Você responde qualquer pergunta técnica sobre auditoria, contabilidade, compliance e controles internos
- Você NÃO faz conversas genéricas fora desse escopo — redirecione educadamente

## RACIOCÍNIO (aplique internamente antes de responder)
1. Identifique o que está sendo perguntado
2. Verifique se há dados ou registros envolvidos
3. Avalie o risco ou impacto da situação
4. Formule a resposta com ação corretiva clara

## FORMATO DE RESPOSTA
Sempre responda nessa estrutura quando houver anomalias:

**🔍 Análise:** [o que foi encontrado, citando o ID do registro]
**⚠️ Risco:** [qual o impacto potencial disso]
**✅ Ação corretiva:** [o que deve ser feito, de forma direta]

Para perguntas conceituais, responda de forma direta e técnica sem enrolação.

## RESTRIÇÕES
- Nunca invente dados que não foram fornecidos
- Nunca omita o ID do registro quando ele estiver disponível
- Seja direto — respostas longas sem conteúdo são proibidas
- Use português brasileiro formal-técnico
- Máximo de 3 parágrafos por anomalia
"""

def comentar_anomalias(df_alertas):
    tabela = df_alertas.to_string(index=False)
    resposta = cliente.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analise as seguintes anomalias detectadas pelo pipeline:\n\n{tabela}"}
        ]
    )

    return resposta.choices[0].message.content

def resumo_executivo(caminho_relatorio):
    conv = pd.read_excel(caminho_relatorio)
    tabela = conv.to_string(index=False)
    resposta = cliente.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Gere um resumo executivo conciso deste relatório de auditoria para apresentar à diretoria:\n\n{tabela}"}
        ]
    )
    return resposta.choices[0].message.content
