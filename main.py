import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_NAME = "leads.db"


def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            interesse TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def inserir_lead(nome, email, telefone, interesse, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (nome, email, telefone, interesse, status)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, email, telefone, interesse, status))
    conn.commit()
    conn.close()

def obter_leads():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads")
    leads = cursor.fetchall()
    conn.close()
    return leads

def atualizar_lead(id_, nome, email, telefone, interesse, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads SET nome=?, email=?, telefone=?, interesse=?, status=?
        WHERE id=?
    """, (nome, email, telefone, interesse, status, id_))
    conn.commit()
    conn.close()

def deletar_lead(id_):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leads WHERE id=?", (id_,))
    conn.commit()
    conn.close()


def carregar_leads():
    for i in tree.get_children():
        tree.delete(i)
    for lead in obter_leads():
        tree.insert("", "end", values=lead)

def limpar_formulario():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_interesse.delete(0, tk.END)
    status_var.set("Em andamento")
    global lead_id_selecionado
    lead_id_selecionado = None

def adicionar_ou_atualizar():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    interesse = entry_interesse.get()
    status = status_var.get()

    if not nome or not email:
        messagebox.showwarning("Aviso", "Nome e email são obrigatórios!")
        return

    if lead_id_selecionado:
        atualizar_lead(lead_id_selecionado, nome, email, telefone, interesse, status)
    else:
        inserir_lead(nome, email, telefone, interesse, status)

    limpar_formulario()
    carregar_leads()

def ao_clicar_na_tabela(event):
    selecionado = tree.focus()
    if not selecionado:
        return

    valores = tree.item(selecionado, "values")
    global lead_id_selecionado
    lead_id_selecionado = valores[0]

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, valores[1])
    entry_email.delete(0, tk.END)
    entry_email.insert(0, valores[2])
    entry_telefone.delete(0, tk.END)
    entry_telefone.insert(0, valores[3])
    entry_interesse.delete(0, tk.END)
    entry_interesse.insert(0, valores[4])
    status_var.set(valores[5])

def excluir():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showinfo("Aviso", "Selecione um lead para excluir.")
        return

    valores = tree.item(selecionado, "values")
    confirm = messagebox.askyesno("Confirmar", f"Deseja excluir o lead '{valores[1]}'?")
    if confirm:
        deletar_lead(valores[0])
        limpar_formulario()
        carregar_leads()


janela = tk.Tk()
janela.title("Cadastro de Lead")
janela.geometry("800x600")

lead_id_selecionado = None
criar_tabela()

tk.Label(janela, text="Nome").pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()

tk.Label(janela, text="Email").pack()
entry_email = tk.Entry(janela)
entry_email.pack()

tk.Label(janela, text="Telefone").pack()
entry_telefone = tk.Entry(janela)
entry_telefone.pack()

tk.Label(janela, text="Interesse").pack()
entry_interesse = tk.Entry(janela)
entry_interesse.pack()

tk.Label(janela, text="Status").pack()
status_var = tk.StringVar(value="Escolha o Status")
status_menu = tk.OptionMenu(janela, status_var, "Em andamento", "Convertido", "Perdido")
status_menu.pack()

btn_adicionar = tk.Button(janela, text="Adicionar / Atualizar", command=adicionar_ou_atualizar)
btn_adicionar.pack(pady=5)

btn_excluir = tk.Button(janela, text="Excluir", command=excluir)
btn_excluir.pack(pady=5)

# Tabela de leads
tree = ttk.Treeview(janela, columns=("ID", "Nome", "Email", "Telefone", "Interesse", "Status"), show="headings")
for col in ("ID", "Nome", "Email", "Telefone", "Interesse", "Status"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=10, fill="both", expand=True)
tree.bind("<Double-1>", ao_clicar_na_tabela)

carregar_leads()

janela.mainloop()
