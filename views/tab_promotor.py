import tkinter as tk
from tkinter import ttk, messagebox

class TabPromotor:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        # --- Cadastro ---
        frame_form = ttk.LabelFrame(self.parent, text="Cadastro de Promotores", padding=15)
        frame_form.pack(fill=tk.X, padx=10, pady=10)

        # Campos de texto
        frame_inputs = ttk.Frame(frame_form)
        frame_inputs.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame_inputs, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.entrada_nome = ttk.Entry(frame_inputs, width=30)
        self.entrada_nome.grid(row=1, column=0, padx=5, sticky=tk.W)

        ttk.Label(frame_inputs, text="Setor (Opcional):").grid(row=0, column=1, sticky=tk.W, padx=5)
        self.entrada_setor = ttk.Entry(frame_inputs, width=30)
        self.entrada_setor.grid(row=1, column=1, padx=5, sticky=tk.W)

        # Checkboxes Dinâmicos
        ttk.Label(frame_form, text="Indústrias que este promotor abastece:", font=("", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.frame_checks = ttk.Frame(frame_form)
        self.frame_checks.pack(fill=tk.X, pady=(0, 10))
        self.check_vars = {} # Dicionário para guardar as variáveis dos checkboxes

        # Botões
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.pack(anchor=tk.W)

        self.btn_salvar = ttk.Button(frame_botoes, text="Salvar", width=15)
        self.btn_salvar.pack(side=tk.LEFT, padx=(0, 5))
        self.btn_cancelar = ttk.Button(frame_botoes, text="Cancelar Edição")

        # --- Lista Customizada ---
        frame_lista = ttk.LabelFrame(self.parent, text="Lista", padding=15)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        header = ttk.Frame(frame_lista)
        header.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(header, text="NOME", font=("", 9, "bold"), width=20).pack(side=tk.LEFT)
        ttk.Label(header, text="SETOR", font=("", 9, "bold"), width=15).pack(side=tk.LEFT)
        ttk.Label(header, text="INDÚSTRIAS", font=("", 9, "bold")).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(header, text="AÇÕES", font=("", 9, "bold"), width=15).pack(side=tk.RIGHT)

        ttk.Separator(frame_lista, orient='horizontal').pack(fill=tk.X, pady=5)

        self.canvas = tk.Canvas(frame_lista, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def limpar_tabela(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def adicionar_linha(self, id_prom, nome, setor, inds_str, cmd_editar, cmd_excluir):
        linha = ttk.Frame(self.scrollable_frame)
        linha.pack(fill=tk.X, pady=2)

        ttk.Label(linha, text=nome, width=20).pack(side=tk.LEFT)
        ttk.Label(linha, text=setor, width=15).pack(side=tk.LEFT)
        ttk.Label(linha, text=inds_str).pack(side=tk.LEFT, fill=tk.X, expand=True)

        frame_acoes = ttk.Frame(linha, width=15)
        frame_acoes.pack(side=tk.RIGHT)

        ttk.Button(frame_acoes, text="Editar", command=cmd_editar).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_acoes, text="Excluir", command=cmd_excluir).pack(side=tk.LEFT, padx=2)

        ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill=tk.X, pady=2)

    def desenhar_checkboxes_industrias(self, industrias, selecionadas=None):
        selecionadas = selecionadas or []
        for widget in self.frame_checks.winfo_children():
            widget.destroy()
        
        self.check_vars.clear()
        
        col = 0
        row = 0
        for ind in industrias:
            ind_id, nome = ind
            var = tk.BooleanVar(value=(ind_id in selecionadas))
            self.check_vars[ind_id] = var
            chk = ttk.Checkbutton(self.frame_checks, text=nome, variable=var)
            chk.grid(row=row, column=col, padx=5, pady=2, sticky=tk.W)
            
            col += 1
            if col > 4: # Quebra de linha nos checkboxes
                col = 0
                row += 1

    def mostrar_mensagem(self, titulo, mensagem, tipo="info"):
        if tipo == "erro":
            messagebox.showerror(titulo, mensagem)
        else:
            messagebox.showinfo(titulo, mensagem)