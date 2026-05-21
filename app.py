import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import json
import re
import sqlite3

# Variável global para controlar os dados na memória para exportação e filtros
df_processado_global = None

# ==========================================
# MOTOR LOGÍSTICO (CONEXÃO COM O BANCO SQL)
# ==========================================
def carregar_dados_brutos():
    try:
        conexao = sqlite3.connect("sistema_atendimento.db")
        query_sql = "SELECT id_chamado, data_abertura, data_fechamento, canal_origem, relato_cliente FROM chamados_brutos"
        df_banco = pd.read_sql(query_sql, conexao)
        conexao.close()
        return df_banco
    except Exception as e:
        messagebox.showerror("Erro de Banco", f"Certifique-se de rodar o 'criar_banco.py' primeiro!\nErro: {str(e)}")
        return pd.DataFrame()

def mascarar_dados_sensiveis(texto):
    padrao_cpf = r'\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11}'
    return re.sub(padrao_cpf, "[DADO_MASCARADO]", texto)

def ejecutar_qa_e_limpeza(df):
    df = df.drop_duplicates(subset=['id_chamado']).copy()
    df['canal_origem'] = df['canal_origem'].str.strip().str.upper()
    df['data_abertura'] = pd.to_datetime(df['data_abertura'])
    df['data_fechamento'] = pd.to_datetime(df['data_fechamento'])
    df['relato_cliente'] = df['relato_cliente'].apply(mascarar_dados_sensiveis)
    df['qa_status'] = 'APROVADO'
    conflito_datas = df['data_fechamento'] < df['data_abertura']
    if conflito_datas.any():
        df.loc[conflito_datas, 'qa_status'] = 'ERRO_CRONOLOGIA'
    return df

def classificar_demanda_com_ia(relato):
    if "cartão" in relato.lower():
        return '{"produto": "Meios de Pagamento", "criticidade": "Média", "risco_regulatorio": false}'
    elif "pagamento instantâneo" in relato.lower() or "saldo" in relato.lower():
        return '{"produto": "Conta Corrente", "criticidade": "Alta", "risco_regulatorio": true}'
    elif "aplicação" in relato.lower() or "renda fixa" in relato.lower():
        return '{"produto": "Investimentos", "criticidade": "Baixa", "risco_regulatorio": false}'
    else:
        return '{"produto": "Crédito e Financiamentos", "criticidade": "Alta", "risco_regulatorio": false}'

# ==========================================
# FUNÇÕES DE CONTROLE DA TELA PRINCIPAL
# ==========================================
def disparar_automacao():
    global df_processado_global
    df_inicial = carregar_dados_brutos()
    if df_inicial.empty: 
        return
    
    df_tratado = ejecutar_qa_e_limpeza(df_inicial)
    df_tratado['analise_ia_bruta'] = df_tratado.apply(
        lambda row: classificar_demanda_com_ia(row['relato_cliente']) if row['qa_status'] == 'APROVADO' 
        else '{"produto": "AUDITORIA_REQUERIDA", "criticidade": "Alta", "risco_regulatorio": true}', axis=1
    )
    
    df_ia_colunas = df_tratado['analise_ia_bruta'].apply(lambda x: json.loads(x)).apply(pd.Series)
    df_final = pd.concat([df_tratado.drop(columns=['analise_ia_bruta']), df_ia_colunas], axis=1)
    
    df_processado_global = df_final.copy()
    
    # Atualiza as opções do Filtro Dropdown dinamicamente
    canais_disponiveis = ["TODOS"] + list(df_final['canal_origem'].unique())
    combo_filtro['values'] = canais_disponiveis
    combo_filtro.current(0)
    
    atualizar_tela_com_dados(df_final)
    btn_exportar.config(state="normal")
    
    # Mensagem de sucesso limpa e sem termos técnicos redundantes
    messagebox.showinfo("Sucesso", "Dados lidos do Banco SQL com sucesso!")

def atualizar_tela_com_dados(df):
    # Atualiza métricas numéricas no topo
    lbl_total.config(text=f"Total Demandas Únicas: {len(df)}")
    lbl_qa.config(text=f"Erros detectados pelo QA: {len(df[df['qa_status'] != 'APROVADO'])}")
    lbl_risco.config(text=f"Demandas Críticas (Risco Regulatório): {len(df[df['risco_regulatorio'] == True])}")
    
    # Limpa e redesenha a tabela visual
    for item in tabela.get_children(): 
        tabela.delete(item)
        
    for _, row in df.iterrows():
        tabela.insert("", "end", values=(row['id_chamado'], row['canal_origem'], row['qa_status'], row['produto'], row['criticidade']))

def aplicar_filtro(event):
    global df_processado_global
    if df_processado_global is None: 
        return
    
    canal_selecionado = combo_filtro.get()
    if canal_selecionado == "TODOS":
        atualizar_tela_com_dados(df_processado_global)
    else:
        df_filtrado = df_processado_global[df_processado_global['canal_origem'] == canal_selecionado]
        atualizar_tela_com_dados(df_filtrado)

def exportar_excel():
    global df_processado_global
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
    if caminho_arquivo:
        df_processado_global.to_excel(caminho_arquivo, index=False)
        messagebox.showinfo("Salvo!", "Planilha exportada com sucesso!")

# ==========================================
# TELA DE LOGIN INICIAL (RECURSO DE SEGURANÇA)
# ==========================================
def verificar_login():
    usuario = entry_user.get()
    senha = entry_password.get()
    
    if usuario == "admin" and senha == "1234":
        janela_login.destroy()  
        abrir_painel_principal()  
    else:
        messagebox.showerror("Acesso Negado", "Usuário ou Senha incorretos!")

janela_login = tk.Tk()
janela_login.title("Autenticação Requerida")
janela_login.geometry("350x220")
janela_login.configure(bg="#2c3e50")
janela_login.eval('tk::PlaceWindow . center')

tk.Label(janela_login, text="🔐 LOGIN CORPORATIVO", font=("Arial", 12, "bold"), fg="white", bg="#2c3e50").pack(pady=15)
tk.Label(janela_login, text="Usuário:", fg="white", bg="#2c3e50").pack()
entry_user = tk.Entry(janela_login, width=25)
entry_user.insert(0, "admin")  
entry_user.pack(pady=5)

tk.Label(janela_login, text="Senha:", fg="white", bg="#2c3e50").pack()
entry_password = tk.Entry(janela_login, show="*", width=25)
entry_password.insert(0, "1234")  
entry_password.pack(pady=5)

tk.Button(janela_login, text="Entrar no Sistema", command=verificar_login, bg="#107c41", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

# ==========================================
# PAINEL CENTRAL (INTERFACE PRINCIPAL)
# ==========================================
def abrir_painel_principal():
    global lbl_total, lbl_qa, lbl_risco, tabela, btn_exportar, combo_filtro
    
    root = tk.Tk()
    root.title("Customer Ops Analytics - Painel Operacional Corporativo")
    root.geometry("880x550") 
    root.configure(bg="#f4f6f9")

    tk.Label(root, text="Pipeline Inteligente de Operações e Demandas", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=10)

    frame_botoes = tk.Frame(root, bg="#f4f6f9")
    frame_botoes.pack(pady=5)

    btn_executar = tk.Button(frame_botoes, text="🚀 EXECUTAR", font=("Arial", 11, "bold"), bg="#107c41", fg="white", padx=20, pady=5, command=disparar_automacao)
    btn_executar.grid(row=0, column=0, padx=10)

    btn_exportar = tk.Button(frame_botoes, text="💾 EXPORTAR PLANILHA", font=("Arial", 11, "bold"), bg="#2b579a", fg="white", padx=15, pady=5, command=exportar_excel, state="disabled")
    btn_exportar.grid(row=0, column=1, padx=10)

    tk.Label(frame_botoes, text="Filtrar por Canal:", font=("Arial", 10, "bold"), bg="#f4f6f9").grid(row=0, column=2, padx=10)
    combo_filtro = ttk.Combobox(frame_botoes, state="readonly", width=18)
    combo_filtro.grid(row=0, column=3, padx=5)
    combo_filtro.bind("<<ComboboxSelected>>", aplicar_filtro)

    frame_metricas = tk.LabelFrame(root, text=" Relatório Executivo Operacional ", font=("Arial", 10, "bold"), bg="#f4f6f9", padx=10, pady=5)
    frame_metricas.pack(fill="x", padx=20, pady=5)

    lbl_total = tk.Label(frame_metricas, text="Total Demandas Únicas: -", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#34495e")
    lbl_total.pack(anchor="w")

    lbl_qa = tk.Label(frame_metricas, text="Erros detectados pelo QA: -", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#c0392b")
    lbl_qa.pack(anchor="w")

    lbl_risco = tk.Label(frame_metricas, text="Demandas Críticas (Risco Regulatório): -", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#d35400")
    lbl_risco.pack(anchor="w")

    frame_tabela = tk.LabelFrame(root, text=" Visualização de Dados Estruturados (Saída de Produção) ", font=("Arial", 10, "bold"), bg="#f4f6f9", padx=10, pady=5)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=5)

    colunas = ('ID Chamado', 'Canal Origem', 'Status QA', 'Categoria Produto', 'Criticidade')
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show='headings', height=10)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130, anchor="center")
    tabela.pack(fill="both", expand=True)

    root.mainloop()

janela_login.mainloop()