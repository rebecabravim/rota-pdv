import tkinter as tk
from tkinter import ttk, messagebox

class TabIndustria:
    def __init__(self, parent_frame):

        LARGURA_ACOES = 10

        self.parent = parent_frame
        
        # --- Card Superior: Cadastro ---
        frame_form = ttk.LabelFrame(self.parent, text="Cadastro de Indústrias", padding=15)
        frame_form.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(frame_form, text="NOME DA INDÚSTRIA", font=("", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        frame_input = ttk.Frame(frame_form)
        frame_input.pack(fill=tk.X, pady=(0, 10))

        # Variável rastreável do Tkinter
        self.var_nome = tk.StringVar()
        self.var_nome.trace_add("write", lambda *args: self.forcar_maiuscula(self.var_nome, self.entrada_nome))
        
        # Entry recebe a textvariable
        self.entrada_nome = ttk.Entry(frame_input, textvariable=self.var_nome)
        self.entrada_nome.pack(fill=tk.X, expand=True)

        frame_botoes_form = ttk.Frame(frame_form)
        frame_botoes_form.pack(anchor=tk.W)

        self.btn_salvar = ttk.Button(frame_botoes_form, text="Salvar", width=15)
        self.btn_salvar.pack(side=tk.LEFT, padx=(0, 5))
        self.btn_cancelar = ttk.Button(frame_botoes_form, text="Cancelar Edição")

        # --- Card Inferior: Tabela Customizada ---
        frame_lista = ttk.LabelFrame(self.parent, text="Lista", padding=15)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cabeçalho da tabela
        header = ttk.Frame(frame_lista)
        header.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(header, text="NOME", font=("", 9, "bold")).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(header, text="AÇÕES", font=("", 9, "bold"), width=LARGURA_ACOES).pack(side=tk.RIGHT)

        ttk.Separator(frame_lista, orient='horizontal').pack(fill=tk.X, pady=5)

        # Configuração do Canvas Rolável para as linhas
        self.canvas = tk.Canvas(frame_lista, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def limpar_tabela(self):
        # Destroi todos os widgets (linhas) dentro do frame rolável
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def adicionar_industria(self, id_ind, nome, cmd_editar, cmd_excluir):

        LARGURA_ACOES = 10

        # Cria uma "linha" (Frame)
        linha = ttk.Frame(self.scrollable_frame)
        linha.pack(fill=tk.X, pady=2)

        # Colunas (Labels e Botões)
        ttk.Label(linha, text=nome).pack(side=tk.LEFT, fill=tk.X, expand=True)

        frame_acoes = ttk.Frame(linha, width=LARGURA_ACOES)
        frame_acoes.pack(side=tk.RIGHT)

        # Os botões NA LINHA e recebem os comandos específicos desta ID
        btn_editar = ttk.Button(frame_acoes, text="Editar", command=cmd_editar)
        btn_editar.pack(side=tk.LEFT, padx=2)

        btn_excluir = ttk.Button(frame_acoes, text="Excluir", command=cmd_excluir)
        btn_excluir.pack(side=tk.LEFT, padx=2)

        ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill=tk.X, pady=2)

    def forcar_maiuscula(self, variavel, widget):
        # Salva a posição do cursor para ele não pular para o final ao editar no meio do texto
        posicao = widget.index(tk.INSERT)
        variavel.set(variavel.get().upper())
        widget.icursor(posicao)
        
    def mostrar_mensagem(self, titulo, mensagem, tipo="info"):
        if tipo == "erro":
            messagebox.showerror(titulo, mensagem)
        else:
            messagebox.showinfo(titulo, mensagem)