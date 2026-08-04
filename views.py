import tkinter as tk
from tkinter import ttk, messagebox

class LivroView:
    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller
        
        self.root.title("📚 Sistema Integrado de Biblioteca")
        self.root.geometry("800x600")
        self.root.minsize(650, 450) # Tamanho mínimo para não quebrar a tela
        
        # ================= ESTILIZAÇÃO E TEMAS =================
        self.style = ttk.Style()
        # 'clam' é um tema nativo do Tkinter muito mais limpo e moderno
        self.style.theme_use("clam") 
        
        # Configurando as fontes e cores base
        fonte_padrao = ("Segoe UI", 10)
        fonte_titulo = ("Segoe UI", 10, "bold")
        
        self.style.configure("TLabel", font=fonte_padrao, padding=5)
        self.style.configure("TButton", font=fonte_titulo, padding=6, background="#0052cc", foreground="white")
        self.style.map("TButton", background=[("active", "#0047b3")]) # Cor ao passar o mouse
        
        self.style.configure("Treeview.Heading", font=fonte_titulo, background="#e1e1e1")
        self.style.configure("Treeview", font=fonte_padrao, rowheight=25)
        
        # ================= SISTEMA DE ABAS =================
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.aba_livros = ttk.Frame(self.notebook)
        self.aba_busca = ttk.Frame(self.notebook)
        self.aba_usuarios = ttk.Frame(self.notebook)
        self.aba_emprestimos = ttk.Frame(self.notebook)
        self.aba_relatorios = ttk.Frame(self.notebook)
        
        self.notebook.add(self.aba_livros, text=" 📖 Cadastrar Livro ")
        self.notebook.add(self.aba_busca, text=" 🔍 Buscar Livros ")
        self.notebook.add(self.aba_usuarios, text=" 👤 Usuários ")
        self.notebook.add(self.aba_emprestimos, text=" 🔄 Empréstimos ")
        self.notebook.add(self.aba_relatorios, text=" 📊 Relatórios ")
        
        # Montando o conteúdo
        self._montar_aba_cadastro()
        self._montar_aba_busca()
        self._montar_aba_usuarios()
        self._montar_aba_emprestimos()
        self._montar_aba_relatorios()

        self.notebook.bind("<<NotebookTabChanged>>", self.atualizar_comboboxes)

    # ================= CONSTRUÇÃO DAS TELAS =================

    def _montar_aba_cadastro(self):
        # Responsividade: A coluna 1 vai esticar ao maximizar a tela
        self.aba_livros.columnconfigure(1, weight=1)

        ttk.Label(self.aba_livros, text="Título:").grid(row=0, column=0, padx=20, pady=(30,10), sticky="e")
        self.entry_titulo = ttk.Entry(self.aba_livros, font=("Segoe UI", 10))
        self.entry_titulo.grid(row=0, column=1, padx=(0, 30), pady=(30,10), sticky="ew") # sticky="ew" faz esticar

        ttk.Label(self.aba_livros, text="Autor:").grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.entry_autor = ttk.Entry(self.aba_livros, font=("Segoe UI", 10))
        self.entry_autor.grid(row=1, column=1, padx=(0, 30), pady=10, sticky="ew")

        ttk.Label(self.aba_livros, text="Ano de Publicação:").grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.entry_ano = ttk.Entry(self.aba_livros, font=("Segoe UI", 10))
        self.entry_ano.grid(row=2, column=1, padx=(0, 30), pady=10, sticky="w") # Fica à esquerda por ser número curto

        ttk.Label(self.aba_livros, text="Quantidade:").grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.entry_qtd = ttk.Entry(self.aba_livros, font=("Segoe UI", 10))
        self.entry_qtd.grid(row=3, column=1, padx=(0, 30), pady=10, sticky="w")

        ttk.Button(self.aba_livros, text="Salvar Livro", command=self.salvar_livro, cursor="hand2").grid(row=4, column=0, columnspan=2, pady=30)

    def _montar_aba_busca(self):
        frame_topo = ttk.Frame(self.aba_busca)
        frame_topo.pack(fill="x", padx=15, pady=15)
        
        ttk.Label(frame_topo, text="Buscar por Título/Autor:").pack(side="left")
        self.entry_busca = ttk.Entry(frame_topo, font=("Segoe UI", 10), width=40)
        self.entry_busca.pack(side="left", padx=10, fill="x", expand=True) # expand=True na busca
        ttk.Button(frame_topo, text="Buscar", command=self.buscar_livro, cursor="hand2").pack(side="left")

        self.tabela_busca = ttk.Treeview(self.aba_busca, columns=("ID", "Título", "Autor", "Ano", "Qtd Disp"), show="headings")
        for col in self.tabela_busca["columns"]:
            self.tabela_busca.heading(col, text=col)
            self.tabela_busca.column(col, width=100, anchor="center")
        self.tabela_busca.column("Título", width=250, anchor="w")
        self.tabela_busca.column("Autor", width=200, anchor="w")
        
        self.tabela_busca.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _montar_aba_usuarios(self):
        self.aba_usuarios.columnconfigure(1, weight=1)

        ttk.Label(self.aba_usuarios, text="Nome Completo:").grid(row=0, column=0, padx=20, pady=(30,10), sticky="e")
        self.entry_nome_user = ttk.Entry(self.aba_usuarios, font=("Segoe UI", 10))
        self.entry_nome_user.grid(row=0, column=1, padx=(0, 30), pady=(30,10), sticky="ew")

        ttk.Label(self.aba_usuarios, text="Identificação (CPF/Matrícula):").grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.entry_ident_user = ttk.Entry(self.aba_usuarios, font=("Segoe UI", 10))
        self.entry_ident_user.grid(row=1, column=1, padx=(0, 30), pady=10, sticky="w")

        ttk.Label(self.aba_usuarios, text="Contato (Email/Telefone):").grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.entry_contato_user = ttk.Entry(self.aba_usuarios, font=("Segoe UI", 10))
        self.entry_contato_user.grid(row=2, column=1, padx=(0, 30), pady=10, sticky="ew")

        ttk.Button(self.aba_usuarios, text="Salvar Usuário", command=self.salvar_usuario, cursor="hand2").grid(row=3, column=0, columnspan=2, pady=30)

    def _montar_aba_emprestimos(self):
        self.aba_emprestimos.columnconfigure(1, weight=1)

        ttk.Label(self.aba_emprestimos, text="Selecione o Livro:").grid(row=0, column=0, padx=20, pady=(40, 15), sticky="e")
        self.combo_livro = ttk.Combobox(self.aba_emprestimos, font=("Segoe UI", 10), state="readonly")
        self.combo_livro.grid(row=0, column=1, padx=(0, 30), pady=(40, 15), sticky="ew")

        ttk.Label(self.aba_emprestimos, text="Selecione o Usuário:").grid(row=1, column=0, padx=20, pady=15, sticky="e")
        self.combo_usuario = ttk.Combobox(self.aba_emprestimos, font=("Segoe UI", 10), state="readonly")
        self.combo_usuario.grid(row=1, column=1, padx=(0, 30), pady=15, sticky="ew")

        frame_botoes = ttk.Frame(self.aba_emprestimos)
        frame_botoes.grid(row=2, column=0, columnspan=2, pady=40)
        
        ttk.Button(frame_botoes, text="Registrar Empréstimo", command=self.emprestar, cursor="hand2").pack(side="left", padx=15)
        # O botão de devolução ganha uma cor diferente usando um estilo específico
        self.style.configure("Devolver.TButton", background="#28a745", foreground="white")
        self.style.map("Devolver.TButton", background=[("active", "#218838")])
        ttk.Button(frame_botoes, text="Registrar Devolução", command=self.devolver, style="Devolver.TButton", cursor="hand2").pack(side="left", padx=15)

    def _montar_aba_relatorios(self):
        frame_botoes = ttk.Frame(self.aba_relatorios)
        frame_botoes.pack(fill="x", padx=15, pady=15)

        ttk.Button(frame_botoes, text="📋 Livros Disponíveis", command=self.relatorio_disponiveis, cursor="hand2").pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="📋 Livros Emprestados", command=self.relatorio_emprestados, cursor="hand2").pack(side="left", padx=5)

        self.tabela_relatorio = ttk.Treeview(self.aba_relatorios, show="headings")
        self.tabela_relatorio.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # ================= EVENTOS DOS BOTÕES =================

    def salvar_livro(self):
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        ano = self.entry_ano.get().strip()
        qtd = self.entry_qtd.get().strip()

        if self.controller:
            status, msg = self.controller.adicionar_livro(titulo, autor, ano, qtd)
            if status:
                messagebox.showinfo("Sucesso", msg)
                for entry in (self.entry_titulo, self.entry_autor, self.entry_ano, self.entry_qtd):
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", msg)

    def buscar_livro(self):
        for item in self.tabela_busca.get_children():
            self.tabela_busca.delete(item)
        if self.controller:
            resultados = self.controller.buscar_livros(self.entry_busca.get())
            for linha in resultados:
                self.tabela_busca.insert("", tk.END, values=linha)

    def salvar_usuario(self):
        nome = self.entry_nome_user.get().strip()
        ident = self.entry_ident_user.get().strip()
        contato = self.entry_contato_user.get().strip()

        if self.controller:
            status, msg = self.controller.adicionar_usuario(nome, ident, contato)
            if status:
                messagebox.showinfo("Sucesso", msg)
                for entry in (self.entry_nome_user, self.entry_ident_user, self.entry_contato_user):
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", msg)

    def atualizar_comboboxes(self, event=None):
        aba_selecionada = self.notebook.index(self.notebook.select())
        if aba_selecionada == 3 and self.controller:
            self.combo_livro['values'] = self.controller.obter_lista_livros()
            self.combo_usuario['values'] = self.controller.obter_lista_usuarios()

    def emprestar(self):
        selecao_livro = self.combo_livro.get()
        selecao_usuario = self.combo_usuario.get()

        if not selecao_livro or not selecao_usuario:
            messagebox.showwarning("Aviso", "Selecione o livro e o usuário nas listas!")
            return

        id_livro = selecao_livro.split(" - ")[0]
        id_usuario = selecao_usuario.split(" - ")[0]

        if self.controller:
            status, msg = self.controller.registrar_emprestimo(id_livro, id_usuario)
            if status:
                messagebox.showinfo("Sucesso", msg)
                self.combo_livro.set('')
                self.combo_usuario.set('')
            else:
                messagebox.showerror("Erro", msg)

    def devolver(self):
        selecao_livro = self.combo_livro.get()
        selecao_usuario = self.combo_usuario.get()

        if not selecao_livro or not selecao_usuario:
            messagebox.showwarning("Aviso", "Selecione o livro e o usuário nas listas!")
            return

        id_livro = selecao_livro.split(" - ")[0]
        id_usuario = selecao_usuario.split(" - ")[0]

        if self.controller:
            status, msg = self.controller.registrar_devolucao(id_livro, id_usuario)
            if status:
                messagebox.showinfo("Sucesso", msg)
                self.combo_livro.set('')
                self.combo_usuario.set('')
            else:
                messagebox.showerror("Erro", msg)

    def configurar_colunas_relatorio(self, colunas):
        self.tabela_relatorio["columns"] = colunas
        for col in colunas:
            self.tabela_relatorio.heading(col, text=col)
            self.tabela_relatorio.column(col, width=120, anchor="center")
        self.tabela_relatorio.column(colunas[1], width=300, anchor="w") 
        
        for item in self.tabela_relatorio.get_children():
            self.tabela_relatorio.delete(item)

    def relatorio_disponiveis(self):
        if self.controller:
            status, dados = self.controller.gerar_relatorio_disponiveis()
            if status:
                self.configurar_colunas_relatorio(("ID", "Título", "Autor", "Qtd Disponível"))
                for linha in dados:
                    self.tabela_relatorio.insert("", tk.END, values=linha)

    def relatorio_emprestados(self):
        if self.controller:
            status, dados = self.controller.gerar_relatorio_emprestados()
            if status:
                self.configurar_colunas_relatorio(("ID Empréstimo", "Título do Livro", "Usuário", "Data"))
                for linha in dados:
                    self.tabela_relatorio.insert("", tk.END, values=linha)