import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from views.utils import WrappableLabel
from views.styles import Cores  

class TabPromotor:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        self.MIN_LARGURA_NOME = 360
        self.MIN_LARGURA_SETOR = 360
        self.MIN_LARGURA_INDUSTRIA = 360
        self.MIN_LARGURA_ACOES = 180
        self.WRAP = 230
        self.PADDING_ACOES = 20

        # --- Cadastro ---
        frame_form = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_form.pack(fill="x", padx=5, pady=(5, 10))

        ctk.CTkLabel(
            frame_form,
            text="Cadastro de Promotores",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=Cores.AZUL_ESCURO,
        ).pack(anchor="w", padx=10, pady=(5, 0))

        frame_inputs = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_inputs.pack(fill="x", padx=10, pady=(0, 5))

        ctk.CTkLabel(
            frame_inputs, text="Nome:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=0, sticky="w", padx=2)
        
        self.var_nome = tk.StringVar()
        self.var_nome.trace_add(
            "write",
            lambda *args: self.forcar_maiuscula(self.var_nome, self.entrada_nome),
        )

        # INPUT NOME
        self.entrada_nome = ctk.CTkEntry(
            frame_inputs,
            width=220,
            height=30,
            textvariable=self.var_nome,
            fg_color=Cores.BRANCO,
            border_color=Cores.CINZA_BORDA,
            border_width=1,
            corner_radius=5,
            text_color=Cores.TEXTO_ESCURO,
        )
        self.entrada_nome.grid(row=1, column=0, padx=(0, 10), sticky="w")

        ctk.CTkLabel(
            frame_inputs,
            text="Setor (Opcional):",
            text_color=Cores.PRETO,
            font=ctk.CTkFont(size=11),
        ).grid(row=0, column=1, sticky="w", padx=2)
        
        self.var_setor = tk.StringVar()
        self.var_setor.trace_add(
            "write",
            lambda *args: self.forcar_maiuscula(self.var_setor, self.entrada_setor),
        )

        # INPUT SETOR
        self.entrada_setor = ctk.CTkEntry(
            frame_inputs,
            width=400,
            height=30,
            textvariable=self.var_setor,
            fg_color=Cores.BRANCO,
            border_color=Cores.CINZA_BORDA,
            border_width=1,
            corner_radius=5,
            text_color=Cores.TEXTO_ESCURO,
        )
        self.entrada_setor.grid(row=1, column=1, sticky="w")

        # CHECKBOXES INDÚSTRIAS
        ctk.CTkLabel(
            frame_form,
            text="Indústrias abastecidas:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Cores.AZUL_ESCURO,
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.frame_checks = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        self.frame_checks.pack(fill="x", padx=10, pady=(0, 10))
        self.check_vars = {}

        # BOTÕES AÇÕES
        frame_botoes = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_botoes.pack(anchor="w", padx=10, pady=(0, 10))

        self.btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            width=90,
            height=28,
            corner_radius=5,
            fg_color=Cores.AZUL_MEDIO,
            hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.BRANCO,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.btn_salvar.pack(side="left", padx=(0, 10))

        self.btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar Edição",
            width=105,
            height=28,
            corner_radius=5,
            fg_color=Cores.AZUL_CLARO,
            hover_color=Cores.AZUL_HOVER_CLARO,
            text_color=Cores.AZUL_ESCURO,
            font=ctk.CTkFont(size=11, weight="bold"),
        )

        # --- Lista ---
        frame_lista = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_lista.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        ctk.CTkLabel(
            frame_lista,
            text="Lista de Promotores",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=Cores.AZUL_ESCURO,
        ).pack(anchor="w", padx=10, pady=(5, 2))

        self.header = ctk.CTkFrame(
            frame_lista, fg_color=Cores.AZUL_CLARO, corner_radius=4, height=26
        )
        self.header.pack(fill="x", padx=10, pady=(0, 2))

        self.header.grid_columnconfigure(0, minsize=self.MIN_LARGURA_NOME, weight=0)
        self.header.grid_columnconfigure(1, minsize=self.MIN_LARGURA_SETOR, weight=0)
        self.header.grid_columnconfigure(2, minsize=self.MIN_LARGURA_INDUSTRIA, weight=1)
        self.header.grid_columnconfigure(3, minsize=self.MIN_LARGURA_ACOES, weight=0)

        ctk.CTkLabel(
            self.header,
            text="NOME",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Cores.AZUL_ESCURO,
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        ctk.CTkLabel(
            self.header,
            text="SETOR",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Cores.AZUL_ESCURO,
        ).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ctk.CTkLabel(
            self.header,
            text="INDÚSTRIAS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Cores.AZUL_ESCURO,
        ).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        ctk.CTkLabel(
            self.header,
            text="AÇÕES",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Cores.AZUL_ESCURO,
        ).grid(row=0, column=3, sticky="e", padx=self.PADDING_ACOES, pady=2)

        self.scrollable_frame = ctk.CTkScrollableFrame(
            frame_lista,
            fg_color=Cores.TRANSPARENTE,
            scrollbar_button_color=Cores.CINZA_SCROLL,
            scrollbar_button_hover_color=Cores.AZUL_CLARO,
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def limpar_tabela(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def adicionar_linha(self, id_prom, nome, setor, inds_str, cmd_editar, cmd_excluir):

        linha = ctk.CTkFrame(self.scrollable_frame, fg_color=Cores.TRANSPARENTE)
        linha.pack(fill="x", pady=1)

        linha.grid_columnconfigure(0, minsize=self.MIN_LARGURA_NOME, weight=0)
        linha.grid_columnconfigure(1, minsize=self.MIN_LARGURA_SETOR, weight=0)
        linha.grid_columnconfigure(2, minsize=self.MIN_LARGURA_INDUSTRIA, weight=1)
        linha.grid_columnconfigure(3, minsize=self.MIN_LARGURA_ACOES, weight=0)

        # NOME
        ctk.CTkLabel(
            linha,
            text=nome,
            text_color=Cores.PRETO,
            anchor="w",
            wraplength=self.WRAP,
            justify="left",
            font=ctk.CTkFont(size=12),
        ).grid(row=0, column=0, sticky="nw", padx=5)

        # SETOR
        ctk.CTkLabel(
            linha,
            text=setor,
            text_color=Cores.PRETO,
            anchor="w",
            justify="left",
            wraplength=self.WRAP,
            font=ctk.CTkFont(size=12),
        ).grid(row=0, column=1, sticky="nw", padx=5)


        # LÓGICA PARA QUEBRA DE LINHA EM INDÚSTRIAS
        frame_industria = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        frame_industria.grid(row=0, column=2, sticky="nsew", padx=5, pady=2)

        lbl_industria = WrappableLabel(
            master=frame_industria,
            text=inds_str,
            text_color=Cores.PRETO,
            fg_color=Cores.BRANCO, 
            anchor="w",
            justify="left",
        )
        lbl_industria.pack(fill="both", expand=True)

        # AÇÕES: Botões Editar e Excluir
        frame_acoes = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        frame_acoes.grid(
            row=0, column=3, sticky="e", padx=2
        )  

        ctk.CTkButton(
            frame_acoes,
            text="Editar",
            command=cmd_editar,
            width=50,
            height=24,
            fg_color=Cores.AZUL_MEDIO,
            hover_color=Cores.AZUL_ESCURO,
            font=ctk.CTkFont(weight="bold", size=11),
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            frame_acoes,
            text="Excluir",
            command=cmd_excluir,
            width=50,
            height=24,
            fg_color=Cores.VERMELHO,
            hover_color=Cores.VERMELHO_ESCURO,
            font=ctk.CTkFont(weight="bold", size=11),
        ).pack(side="left", padx=2)

        ctk.CTkFrame(self.scrollable_frame, fg_color=Cores.CINZA_LINHA, height=1).pack(
            fill="x", pady=1
        )

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

            chk = ctk.CTkCheckBox(
                self.frame_checks,
                text=nome,
                variable=var,
                checkbox_width=18,
                checkbox_height=18,
                border_width=2,
                fg_color=Cores.AZUL_MEDIO,
                hover_color=Cores.AZUL_ESCURO,
                border_color=Cores.CINZA_SCROLL,
                text_color=Cores.PRETO,
                font=ctk.CTkFont(size=11),
            )
            chk.grid(row=row, column=col, padx=(0, 15), pady=2, sticky="w")

            col += 1
            if col > 5:
                col = 0
                row += 1

    def forcar_maiuscula(self, variavel, widget):
        posicao = widget.index(tk.INSERT)
        variavel.set(variavel.get().upper())
        widget.icursor(posicao)

    def mostrar_mensagem(self, titulo, mensagem, tipo="info"):
        if tipo == "erro":
            messagebox.showerror(titulo, mensagem)
        else:
            messagebox.showinfo(titulo, mensagem)