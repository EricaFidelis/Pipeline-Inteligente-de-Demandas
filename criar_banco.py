import sqlite3

# 1. Conecta ao arquivo de banco de dados (se não existir, ele cria na hora)
conexao = sqlite3.connect("sistema_atendimento.db")
cursor = conexao.cursor()

# 2. Cria a tabela simulando o banco de dados da empresa
cursor.execute("""
CREATE TABLE IF NOT EXISTS chamados_brutos (
    id_chamado INTEGER,
    data_abertura TEXT,
    data_fechamento TEXT,
    canal_origem TEXT,
    relato_cliente TEXT
)
""")

# 3. Limpa dados antigos para não duplicar o teste
cursor.execute("DELETE FROM chamados_brutos")

# 4. Insere os dados brutos como se tivessem sido gravados pelo sistema da empresa
dados_para_inserir = [
    (1001, '2026-05-20', '2026-05-22', 'PlataformaWeb', 'Gostaria de contestar uma transação no meu cartão final 4321 de R$ 250,00 que não reconheço. Meu CPF é 123.456.789-00.'),
    (1002, '2026-05-21', '2026-05-20', '  Aplicativo ', 'O pagamento instantâneo deu erro na hora de enviar, retirou o saldo de R$ 50 da conta corrente e não gerou comprovante. Preciso do dinheiro hoje!'),
    (1003, '2026-05-21', None, 'PortalSuporte', 'Fiz uma aplicação financeira de renda fixa e não consigo visualizar o rendimento no painel corporativo.'),
    (1004, '2026-05-19', '2026-05-25', 'OuvidoriaGeral', 'Estou tentando renegociar meu contrato de crédito parcelado mas a taxa de juros aplicada está divergente do combinado.'),
    (1001, '2026-05-20', '2026-05-22', 'PlataformaWeb', 'Gostaria de contestar uma transação no meu cartão final 4321 de R$ 250,00 que não reconheço. Meu CPF é 123.456.789-00.')
]

cursor.executemany("INSERT INTO chamados_brutos VALUES (?, ?, ?, ?, ?)", dados_para_inserir)

# 5. Salva e fecha a conexão
conexao.commit()
conexao.close()

print("💾 Banco de dados 'sistema_atendimento.db' criado com sucesso com tabelas SQL!")