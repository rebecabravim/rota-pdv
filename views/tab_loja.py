import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from views.utils import WrappableLabel
from views.styles import Cores 


class TabLoja:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        # --- Card Superior: Formulário de Cadastro ---
        frame_form = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_form.pack(fill="x", padx=5, pady=(5, 10))

        ctk.CTkLabel(
            frame_form, text="Cadastro de Lojas (PDV)", 
            font=ctk.CTkFont(size=13, weight="bold"), text_color=Cores.AZUL_ESCURO
        ).pack(anchor="w", padx=10, pady=(5, 0))

        # Linha 1 de Inputs: Nome, Cidade, Endereço, Intervalo
        frame_inputs = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_inputs.pack(fill="x", padx=10, pady=(0, 5))
        
        # NOME
        ctk.CTkLabel(frame_inputs, text="Nome da Loja:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w", padx=2)
        self.var_nome = tk.StringVar()
        self.var_nome.trace_add("write", lambda *args: self.forcar_maiuscula(self.var_nome, self.entrada_nome))
        self.entrada_nome = ctk.CTkEntry(
            frame_inputs, width=200, height=30, textvariable=self.var_nome, 
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1, corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_nome.grid(row=1, column=0, padx=(0, 8), sticky="w")

        # CIDADE
        ctk.CTkLabel(frame_inputs, text="Cidade:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)).grid(row=0, column=1, sticky="w", padx=2)
        self.var_cidade = tk.StringVar()
        self.var_cidade.trace_add("write", lambda *args: self.forcar_maiuscula(self.var_cidade, self.entrada_cidade))
        self.entrada_cidade = ctk.CTkEntry(
            frame_inputs, width=160, height=30, textvariable=self.var_cidade, 
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1, corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_cidade.grid(row=1, column=1, padx=(0, 8), sticky="w")

        # ENDEREÇO
        ctk.CTkLabel(frame_inputs, text="Endereço (Opcional):", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)).grid(row=0, column=2, sticky="w", padx=2)
        self.var_endereco = tk.StringVar()
        self.var_endereco.trace_add("write", lambda *args: self.forcar_maiuscula(self.var_endereco, self.entrada_endereco))
        self.entrada_endereco = ctk.CTkEntry(
            frame_inputs, width=220, height=30, textvariable=self.var_endereco, 
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1, corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_endereco.grid(row=1, column=2, padx=(0, 8), sticky="w")

        # INTERVALO (DIAS)
        ctk.CTkLabel(frame_inputs, text="Intervalo (dias):", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)).grid(row=0, column=3, sticky="w", padx=2)
        self.entrada_intervalo = ctk.CTkEntry(
            frame_inputs, width=90, height=30, 
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1, corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_intervalo.insert(0, "7")
        self.entrada_intervalo.grid(row=1, column=3, sticky="w")

        # Seção de Checkboxes: Promotores
        ctk.CTkLabel(frame_form, text="Promotores associados a esta loja:", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).pack(anchor="w", padx=10, pady=(5, 0))
        self.frame_prom_checks = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        self.frame_prom_checks.pack(fill="x", padx=10, pady=(0, 5))
        self.check_prom_vars = {}

        # Seção de Checkboxes: Indústrias
        ctk.CTkLabel(frame_form, text="Indústrias atendidas nesta loja:", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).pack(anchor="w", padx=10, pady=(5, 0))
        self.frame_ind_checks = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        self.frame_ind_checks.pack(fill="x", padx=10, pady=(0, 5))
        self.check_ind_vars = {}

        # Botões de Ação
        frame_botoes = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_botoes.pack(anchor="w", padx=10, pady=(5, 10))

        self.btn_salvar = ctk.CTkButton(
            frame_botoes, text="Salvar", width=90, height=28, corner_radius=5,
            fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO, 
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_salvar.pack(side="left", padx=(0, 10))
        
        self.btn_cancelar = ctk.CTkButton(
            frame_botoes, text="Cancelar Edição", width=105, height=28, corner_radius=5,
            fg_color=Cores.AZUL_CLARO, hover_color=Cores.AZUL_HOVER_CLARO, 
            text_color=Cores.AZUL_ESCURO, font=ctk.CTkFont(size=11, weight="bold")
        )
        # Oculto por padrão

        # --- Card Inferior: Tabela de Lojas ---
        frame_lista = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_lista.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        ctk.CTkLabel(frame_lista, text="Lista de Lojas", font=ctk.CTkFont(size=13, weight="bold"), text_color=Cores.AZUL_ESCURO).pack(anchor="w", padx=10, pady=(5, 2))

        header = ctk.CTkFrame(frame_lista, fg_color=Cores.AZUL_CLARO, corner_radius=4, height=26)
        header.pack(fill="x", padx=10, pady=(0, 2))

        # Estrutura Rígida de Colunas
        header.grid_columnconfigure(0, minsize=160, weight=0) # LOJA
        header.grid_columnconfigure(1, minsize=110, weight=0) # CIDADE
        header.grid_columnconfigure(2, minsize=80, weight=0)  # INTERVALO
        header.grid_columnconfigure(3, weight=1)              # PROMOTORES
        header.grid_columnconfigure(4, weight=1)              # INDÚSTRIAS
        header.grid_columnconfigure(5, minsize=120, weight=0) # AÇÕES

        ctk.CTkLabel(header, text="LOJA", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=0, sticky="w", padx=10, pady=2)
        ctk.CTkLabel(header, text="CIDADE", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=1, sticky="w", padx=10, pady=2)
        ctk.CTkLabel(header, text="INTERVALO", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=2, sticky="w", padx=10, pady=2)
        ctk.CTkLabel(header, text="PROMOTORES", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=3, sticky="w", padx=10, pady=2)
        ctk.CTkLabel(header, text="INDÚSTRIAS", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=4, sticky="w", padx=10, pady=2)
        ctk.CTkLabel(header, text="AÇÕES", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=5, sticky="e", padx=15, pady=2)

        self.scrollable_frame = ctk.CTkScrollableFrame(
            frame_lista, fg_color=Cores.TRANSPARENTE, 
            scrollbar_button_color=Cores.CINZA_SCROLL, scrollbar_button_hover_color=Cores.AZUL_CLARO
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def desenhar_checkboxes_promotores(self, promotores, selecionados=None):
        selecionados = selecionados or []
        for widget in self.frame_prom_checks.winfo_children():
            widget.destroy()
        
        self.check_prom_vars.clear()
        col, row = 0, 0
        for p in promotores:
            # Suporta dicionário/Row (p['id']) ou tupla (p[0])
            p_id = p['id'] if isinstance(p, dict) or hasattr(p, 'keys') else p[0]
            nome = p['nome'] if isinstance(p, dict) or hasattr(p, 'keys') else p[1]

            var = tk.BooleanVar(value=(p_id in selecionados))
            self.check_prom_vars[p_id] = var
            
            chk = ctk.CTkCheckBox(
                self.frame_prom_checks, text=nome, variable=var,
                checkbox_width=18, checkbox_height=18, border_width=2,
                fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO, 
                border_color=Cores.CINZA_BORDA, text_color=Cores.PRETO,
                font=ctk.CTkFont(size=11)
            )
            chk.grid(row=row, column=col, padx=(0, 15), pady=2, sticky="w")
            col += 1
            if col > 5:
                col = 0
                row += 1

    def desenhar_checkboxes_industrias(self, industrias, selecionadas=None):
        selecionadas = selecionadas or []
        for widget in self.frame_ind_checks.winfo_children():
            widget.destroy()
        
        self.check_ind_vars.clear()
        col, row = 0, 0
        for ind in industrias:
            # Suporta dicionário/Row (ind['id']) ou tupla (ind[0])
            ind_id = ind['id'] if isinstance(ind, dict) or hasattr(ind, 'keys') else ind[0]
            nome = ind['nome'] if isinstance(ind, dict) or hasattr(ind, 'keys') else ind[1]

            var = tk.BooleanVar(value=(ind_id in selecionadas))
            self.check_ind_vars[ind_id] = var
            
            chk = ctk.CTkCheckBox(
                self.frame_ind_checks, text=nome, variable=var,
                checkbox_width=18, checkbox_height=18, border_width=2,
                fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO, 
                border_color=Cores.CINZA_BORDA, text_color=Cores.PRETO,
                font=ctk.CTkFont(size=11)
            )
            chk.grid(row=row, column=col, padx=(0, 15), pady=2, sticky="w")
            col += 1
            if col > 5:
                col = 0
                row += 1

    def obter_promotores_selecionados(self):
        return [p_id for p_id, var in self.check_prom_vars.items() if var.get()]

    def obter_industrias_selecionadas(self):
        return [ind_id for ind_id, var in self.check_ind_vars.items() if var.get()]

    def limpar_tabela(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def adicionar_linha(self, id_loja, nome, cidade, endereco, intervalo, promotores_str, industrias_str, cmd_editar, cmd_excluir):
        linha = ctk.CTkFrame(self.scrollable_frame, fg_color=Cores.TRANSPARENTE)
        linha.pack(fill="x", pady=1)

        linha.grid_columnconfigure(0, minsize=160, weight=0)
        linha.grid_columnconfigure(1, minsize=110, weight=0)
        linha.grid_columnconfigure(2, minsize=80, weight=0)
        linha.grid_columnconfigure(3, weight=1)
        linha.grid_columnconfigure(4, weight=1)
        linha.grid_columnconfigure(5, minsize=120, weight=0)

        # LOJA (com Endereço em subtexto)
        texto_loja = f"{nome}\n({endereco})" if endereco and endereco != "—" else nome
        ctk.CTkLabel(linha, text=texto_loja, text_color=Cores.PRETO, anchor="w", wraplength=150, font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w", padx=10)
        
        # CIDADE E INTERVALO
        ctk.CTkLabel(linha, text=cidade, text_color=Cores.PRETO, anchor="w", font=ctk.CTkFont(size=11)).grid(row=0, column=1, sticky="w", padx=10)
        ctk.CTkLabel(linha, text=intervalo, text_color=Cores.PRETO, anchor="w", font=ctk.CTkFont(size=11)).grid(row=0, column=2, sticky="w", padx=10)

        # PROMOTORES E INDÚSTRIAS (Importado de views.utils)
        f_prom = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        f_prom.grid(row=0, column=3, sticky="nsew", padx=5)
        lbl_p = WrappableLabel(f_prom, text=promotores_str, text_color=Cores.TEXTO_ESCURO, font=ctk.CTkFont(size=11))
        lbl_p.pack(fill="both", expand=True)

        f_ind = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        f_ind.grid(row=0, column=4, sticky="nsew", padx=5)
        lbl_i = WrappableLabel(f_ind, text=industrias_str, text_color=Cores.TEXTO_ESCURO, font=ctk.CTkFont(size=11))
        lbl_i.pack(fill="both", expand=True)

        # AÇÕES
        frame_acoes = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        frame_acoes.grid(row=0, column=5, sticky="e", padx=5)

        ctk.CTkButton(
            frame_acoes, text="Editar", command=cmd_editar, width=50, height=24, 
            fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO, 
            font=ctk.CTkFont(weight="bold", size=11)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            frame_acoes, text="Excluir", command=cmd_excluir, width=50, height=24, 
            fg_color=Cores.VERMELHO, hover_color=Cores.VERMELHO_ESCURO, 
            font=ctk.CTkFont(weight="bold", size=11)
        ).pack(side="left", padx=2)

        ctk.CTkFrame(self.scrollable_frame, fg_color=Cores.CINZA_LINHA, height=1).pack(fill="x", pady=1)

    def forcar_maiuscula(self, variavel, widget):
        posicao = widget.index(tk.INSERT)
        variavel.set(variavel.get().upper())
        widget.icursor(posicao)

    def mostrar_mensagem(self, titulo, mensagem, tipo="info"):
        if tipo == "erro":
            messagebox.showerror(titulo, mensagem)
        else:
            messagebox.showinfo(titulo, mensagem)