import datetime
import json
import os
import re
import pandas as pd
from google import genai

# ==========================================
# PASSO 1: SIMULAÇÃO DE INGESTÃO DE DADOS
# ==========================================

def carregar_dados_brutos():
    """Simula a coleta de dados diários de sistemas de atendimento (SAC/Canais)."""
    dados = {
        'id_chamado': [1001, 1002, 1003, 1004, 1001], # Nota: 1001 está duplicado propositalmente
        'data_abertura': ['2026-05-20', '2026-05-21', '2026-05-21', '2026-05-19', '2026-05-20'],
        'data_fechamento': ['2026-05-22', '2026-05-20', None, '2026-05-25', '2026-05-22'], # Nota: 1002 fechou antes de abrir!
        'canal_origem': ['ReclameAqui', '  Aplicativo ', 'bacen', 'Ouvidoria', 'ReclameAqui'], # Espaços em branco e caixa alta/baixa
        'relato_cliente': [
            "Gostaria de contestar uma compra no meu cartão final 4321 de R$ 250,00 que não reconheço. Meu CPF é 123.456.789-00.",
            "O Pix deu erro na hora de enviar, sumiu o saldo de R$ 50 da conta corrente e não gerou comprovante. Preciso do dinheiro para pagar o aluguel hoje!",
            "Fiz um investimento em LCA e não consigo visualizar o rendimento no app corporativo.",
            "Estou tentando renegociar minha dívida do cheque especial mas a taxa de juros que estão cobrando está abusiva.",
            "Gostaria de contestar uma compra no meu cartão final 4321 de R$ 250,00 que não reconheço. Meu CPF é 123.456.789-00."
        ]
    }
    return pd.DataFrame(dados)

df_inicial = carregar_dados_brutos()
print(f"📊 Dados brutos carregados: {df_inicial.shape[0]} registros encontrados.")
import re

# ==========================================
# PASSO 2: GOVERNANÇA, LIMPEZA E QA DE DADOS
# ==========================================

def mascarar_dados_sensiveis(texto):
    """Garante a conformidade com a LGPD removendo padrões de CPF do relato."""
    padrao_cpf = r'\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11}'
    return re.sub(padrao_cpf, "[CPF_MASCARADO]", texto)

def executar_qa_e_limpeza(df):
    """Aplica regras de negócio estritas para higienização e controle de qualidade."""
    print("\n⚡ Iniciando rotina de Reengenharia e QA de dados...")
    
    # 1. Eliminação de Duplicidade (Processamento Operacional Eficiente)
    df = df.drop_duplicates(subset=['id_chamado']).copy()
    
    # 2. Padronização de Texto (Remover espaços e padronizar caixa alta)
    df['canal_origem'] = df['canal_origem'].str.strip().str.upper()
    
    # 3. Conversão de Datas para validação operacional
    df['data_abertura'] = pd.to_datetime(df['data_abertura'])
    df['data_fechamento'] = pd.to_datetime(df['data_fechamento'])
    
    # 4. Aplicação de LGPD
    df['relato_cliente'] = df['relato_cliente'].apply(mascarar_dados_sensiveis)
    
    # 5. QA de Regra de Negócio: Identificar inconsistências de datas
    df['qa_status'] = 'APROVADO'
    conflito_datas = df['data_fechamento'] < df['data_abertura']
    
    if conflito_datas.any():
        print(f"⚠️ Alerta de QA: {df[conflito_datas].shape[0]} registro(s) com erro de data detectados!")
        df.loc[conflito_datas, 'qa_status'] = 'ERRO_SISTEMA_DATAS'
        
    return df

# Executando a camada de QA
df_tratado = executar_qa_e_limpeza(df_inicial)

print("\n--- Resultado após Higienização e QA ---")
print(df_tratado[['id_chamado', 'canal_origem', 'qa_status', 'relato_cliente']])
import json

# ==========================================
# PASSO 3: INTEGRAÇÃO COM AGENTE DE IA
# ==========================================

def classificar_demanda_com_ia(relato):
    """Utiliza IA estruturada para extrair produto, criticidade e urgência regulatória."""
    
    # Simulador inteligente (Mock) para rodar sem precisar de chave de API externa
    if "cartão" in relato.lower():
        return '{"produto": "Cartão de Crédito", "criticidade": "Média", "risco_regulador": false}'
    elif "pix" in relato.lower():
        return '{"produto": "Pix/Conta Corrente", "criticidade": "Alta", "risco_regulador": true}'
    elif "investimento" in relato.lower():
        return '{"produto": "Investimentos", "criticidade": "Baixa", "risco_regulador": false}'
    else:
        return '{"produto": "Empréstimos/Dívidas", "criticidade": "Alta", "risco_regulador": false}'

print("\n🤖 Acionando Agente de IA para enriquecimento analítico...")

# Aplicando o simulador apenas nos dados aprovados pelo QA
df_tratado['analise_ia_bruta'] = df_tratado.apply(
    lambda row: classificar_demanda_com_ia(row['relato_cliente']) if row['qa_status'] == 'APROVADO' 
    else '{"produto": "AUDITORIA_REQUERIDA", "criticidade": "Alta", "risco_regulador": true}',
    axis=1
)

# Transforma a resposta texto/JSON em colunas estruturadas reais no Pandas
def extrair_json(texto_json):
    try:
        return json.loads(texto_json)
    except:
        return {"produto": "Erro de Parse", "criticidade": "Alta", "risco_regulador": True}

df_ia_colunas = df_tratado['analise_ia_bruta'].apply(extrair_json).apply(pd.Series)

# AQUI É CRIADO O DF_FINAL QUE ESTAVA FALTANDO!
df_final = pd.concat([df_tratado.drop(columns=['analise_ia_bruta']), df_ia_colunas], axis=1)

print("\n🚀 Pipeline executado com sucesso! Estrutura final para o Report Executivo:")
print(df_final[['id_chamado', 'produto', 'criticidade', 'risco_regulador']])
# ==========================================
# PASSO 4: EXPORTAÇÃO PARA BI (REPORTS)
# ==========================================
print("\n💾 Salvando base consolidada para o Power BI...")
df_final.to_csv("base_ouvidoria_itau.csv", index=False, encoding="utf-8-sig")
print("✅ Arquivo 'base_ouvidoria_itau.csv' gerado com sucesso na pasta do projeto!")