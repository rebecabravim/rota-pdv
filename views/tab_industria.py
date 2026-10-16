import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from views.utils import WrappableLabel
from views.styles import Cores

class TabIndustria:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        self.MIN_LARGURA_ACOES = 180
        self.PADDING_ACOES = 20

        # --- Card Superior: Cadastro ---
        frame_form = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_form.pack(fill="x", padx=5, pady=(5, 10))

        ctk.CTkLabel(
            frame_form, 
            text="Cadastro de Indústrias", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            text_color=Cores.AZUL_ESCURO
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.var_nome = tk.StringVar()
        self.var_nome.trace_add(
            "write", 
            lambda *args: self.forcar_maiuscula(self.var_nome, self.entrada_nome)
        )

        # INPUT MODERNO
        self.entrada_nome = ctk.CTkEntry(
            frame_form, 
            textvariable=self.var_nome, 
            fg_color=Cores.BRANCO, 
            border_color=Cores.CINZA_BORDA, 
            border_width=1, 
            corner_radius=5,
            text_color=Cores.TEXTO_ESCURO, 
            height=30
        )
        self.entrada_nome.pack(fill="x", padx=10, pady=(5, 10))

        frame_botoes = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_botoes.pack(anchor="w", padx=10, pady=(0, 10))

        # BOTÕES AÇÕES CADASTRO
        self.btn_salvar = ctk.CTkButton(
            frame_botoes, 
            text="Salvar", 
            width=90, 
            height=28, 
            corner_radius=5,
            fg_color=Cores.AZUL_MEDIO, 
            hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.BRANCO, 
            font=ctk.CTkFont(size=11, weight="bold")
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
            font=ctk.CTkFont(size=11, weight="bold")
        )

        # --- Lista
        frame_lista = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_lista.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        ctk.CTkLabel(
            frame_lista, 
            text="Lista de Indústrias", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            text_color=Cores.AZUL_ESCURO
        ).pack(anchor="w", padx=10, pady=(5, 2))

        header = ctk.CTkFrame(frame_lista, fg_color=Cores.AZUL_CLARO, corner_radius=4, height=26)
        header.pack(fill="x", padx=10, pady=(0, 2))
        
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, minsize=self.MIN_LARGURA_ACOES, weight=0)

        ctk.CTkLabel(
            header, text="NOME", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO
        ).grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        ctk.CTkLabel(
            header, text="AÇÕES", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO
        ).grid(row=0, column=1, sticky="e", padx=self.PADDING_ACOES, pady=2)

        self.scrollable_frame = ctk.CTkScrollableFrame(
            frame_lista, 
            fg_color=Cores.TRANSPARENTE, 
            scrollbar_button_color=Cores.CINZA_SCROLL, 
            scrollbar_button_hover_color=Cores.AZUL_CLARO
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def limpar_tabela(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def adicionar_industria(self, id_ind, nome, cmd_editar, cmd_excluir):
        linha = ctk.CTkFrame(self.scrollable_frame, fg_color=Cores.TRANSPARENTE)
        linha.pack(fill="x", pady=1)

        linha.grid_columnconfigure(0, weight=1)
        linha.grid_columnconfigure(1, minsize=self.MIN_LARGURA_ACOES, weight=0)

        # --- LÓGICA PARA QUEBRA DE LINHA NO NOME DA INDÚSTRIA ---
        frame_nome = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        frame_nome.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)

        lbl_nome = WrappableLabel(
            master=frame_nome,
            text=nome,
            text_color=Cores.PRETO,
            fg_color=Cores.BRANCO,
            anchor="w",
            justify="left"
        )
        lbl_nome.pack(fill="both", expand=True)
        # --------------------------------------------------------

        # AÇÕES: Botões Editar e Excluir
        frame_acoes = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        frame_acoes.grid(row=0, column=1, sticky="e", padx=5)

        ctk.CTkButton(
            frame_acoes, 
            text="Editar", 
            command=cmd_editar, 
            fg_color=Cores.AZUL_MEDIO, 
            hover_color=Cores.AZUL_ESCURO, 
            font=ctk.CTkFont(weight="bold", size=11), 
            width=50, 
            height=24
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            frame_acoes, 
            text="Excluir", 
            command=cmd_excluir, 
            fg_color=Cores.VERMELHO, 
            hover_color=Cores.VERMELHO_ESCURO, 
            font=ctk.CTkFont(weight="bold", size=11), 
            width=50, 
            height=24
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