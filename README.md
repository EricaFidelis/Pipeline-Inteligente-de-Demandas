📈 Customer Ops Analytics - Pipeline Inteligente de Demandas
Bem-vindo(a) ao Customer Ops Analytics! Este é um sistema inteligente de engenharia e análise de dados desenvolvido para resolver um problema crítico em grandes empresas: a bagunça, os erros e os riscos de segurança no recebimento de reclamações de clientes.

O sistema funciona como uma "Fábrica Automática" que se conecta a um banco de dados relacional, limpa as informações de forma segura, audita a qualidade dos dados, classifica tudo por inteligência lógica e entrega um painel de controle (Dashboard) pronto para os diretores tomarem decisões.

🛠️ O que usamos para construir esse projeto? (Tecnologias)
Para garantir que o projeto rodasse rápido, fosse leve e não dependesse de instalações complexas no computador da empresa, usamos as ferramentas mais consolidadas do mercado de dados:

Python (Linguagem Principal): O cérebro do projeto, responsável por ditar as regras de como os dados andam pelo sistema.

SQLite (Banco de Dados): Um banco de dados relacional real que armazena os chamados e as reclamações brutas da empresa através de tabelas SQL.

Pandas (Manipulação de Dados): A biblioteca de mercado mais poderosa para ler, limpar, remover duplicados e estruturar tabelas de dados na memória.

Tkinter (Interface Gráfica): Ferramenta nativa do Python usada para construir toda a parte visual do aplicativo (botões, tabelas, caixa de login e filtros).

JSON & Regex (Segurança e Extração): Usados para ler as respostas da IA e criar filtros que localizam e escondem CPFs automaticamente.

🏗️ Como a "Fábrica de Dados" funciona por dentro?
O sistema é dividido em 4 etapas automatizadas que acontecem em menos de um segundo assim que o usuário interage com a tela:

1. Governança e Segurança de Acesso (Login)
Nenhum dado sensível de cliente pode ficar exposto. Por isso, o sistema possui uma tela de autenticação restrita. O operador precisa digitar as credenciais corporativas (admin / 1234) para que o painel principal seja liberado.

2. Ingestão de Dados (SQL)
Ao clicar no botão verde "🚀 EXECUTAR", o script faz um comando SELECT invisível diretamente no banco de dados SQLite (sistema_atendimento.db), trazendo todas as reclamações brutas registradas pelos clientes.

3. Esteira de Limpeza e Qualidade (O Coração do Código)
Aqui, o código Pandas executa três tarefas de uma vez só:

Mascaramento LGPD: Se o cliente escreveu o CPF dele no meio do texto da reclamação, o robô apaga os números e escreve [DADO_MASCARADO], protegendo a empresa contra multas da Lei Geral de Proteção de Dados.

Filtro de Qualidade (Status QA): O robô analisa se a data de fechamento do chamado é menor que a data de abertura. Se for, ele carimba como ERRO_CRONOLOGIA para sinalizar bugs no sistema de origem. Se estiver tudo certo, carimba como APROVADO.

Categorização por Inteligência Lógica: O código lê as palavras-chave da reclamação (como "cartão", "saldo", "aplicação") e deduz sozinho qual é o produto (Meios de Pagamento, Conta Corrente, Investimentos) e o nível de criticidade daquele problema.

4. Visualização e Entrega de Valor (Dashboard)
Os dados limpos são jogados na tela em uma tabela organizada. O painel calcula instantaneamente os indicadores vitais para os chefes: total de chamados, quantos erros de sistema foram travados pelo QA e quantas demandas são críticas.

Filtro Dinâmico: É possível selecionar um canal de atendimento específico (como APLICATIVO) e a tabela se atualiza sozinha na hora.

Exportação (Excel): Com um clique no botão azul, o usuário salva um relatório limpo no formato .xlsx na sua máquina local para enviar por e-mail ou alimentar apresentações executivas.

🚀 Como Executar o Projeto
Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina e a biblioteca Pandas. Caso não tenha o Pandas, instale pelo terminal usando:

Bash
pip install pandas openpyxl
Passo a Passo
Crie o banco de dados inicial: Execute o arquivo criar_banco.py no seu VS Code para que a tabela SQL e os chamados simulados sejam gerados.

Inicie o aplicativo: Execute o arquivo app.py.

Faça o Login: Use o usuário admin e a senha 1234.

Rode o Pipeline: Clique no botão verde "🚀 EXECUTAR" para ver a mágica acontecer!

💡 Por que este projeto se destaca em uma entrevista?
Este projeto vai muito além de um "código que funciona". Ele foi desenhado seguindo as melhores práticas do mercado corporativo porque resolve três dores reais de qualquer grande corporação:

Garante a Qualidade dos Dados (Data Quality): Através do motor de Status QA, ele evita que relatórios gerenciais fiquem errados devido a bugs de sistemas de terceiros.

Cumpre Leis Federais (Compliance): O mascaramento automático de CPF garante conformidade imediata com as diretrizes da LGPD.

Gera Eficiência Operacional: Transforma horas de leitura manual de textos em uma triagem automatizada com visualização clara e exportável para tomada de decisão em segundos.
