from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from views.utils import WrappableLabel
from views.styles import Cores


class TabRoteiro:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.total_cards_exibidos = 0

        # Larguras fixas sincronizadas entre Cabeçalho e Linhas da Tabela Inferior
        self.LARGURA_PROMOTOR = 260
        self.LARGURA_DATA = 115
        self.LARGURA_LOJAS = 100
        self.LARGURA_FEITAS = 100
        self.LARGURA_NAO_FEITAS = 110
        self.LARGURA_ACOES = 130
        self.PADDING_ACOES = 20

        # =====================================================================
        # CARD SUPERIOR: NOVO ROTEIRO / EDITANDO ROTEIRO
        # =====================================================================
        frame_form = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_form.pack(fill="both", expand=True, padx=5, pady=(5, 10))

        self.lbl_titulo_form = ctk.CTkLabel(
            frame_form,
            text="Novo Roteiro",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=Cores.AZUL_ESCURO
        )
        self.lbl_titulo_form.pack(anchor="w", padx=10, pady=(5, 2))

        # Linha de Inputs: Promotor, Data, Filtro de Estoque
        frame_inputs = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_inputs.pack(fill="x", padx=10, pady=(0, 5))

        # PROMOTOR
        ctk.CTkLabel(
            frame_inputs, text="Promotor:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=0, sticky="w", padx=2)
        self.combo_promotor = ctk.CTkComboBox(
            frame_inputs, width=240, height=30, values=[], state="readonly",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            button_color=Cores.AZUL_MEDIO, button_hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.TEXTO_ESCURO, dropdown_fg_color=Cores.BRANCO,
            dropdown_text_color=Cores.TEXTO_ESCURO
        )
        self.combo_promotor.grid(row=1, column=0, padx=(0, 10), sticky="w")

        # DATA
        ctk.CTkLabel(
            frame_inputs, text="Data (DD/MM/AAAA):", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=1, sticky="w", padx=2)
        self.entrada_data = ctk.CTkEntry(
            frame_inputs, width=140, height=30, placeholder_text="DD/MM/AAAA",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entrada_data.bind("<KeyRelease>", lambda e: self._aplicar_mascara_data(self.entrada_data))
        self.entrada_data.grid(row=1, column=1, padx=(0, 10), sticky="w")

        # FILTRO DE ESTOQUE
        ctk.CTkLabel(
            frame_inputs, text="Filtro (Estoque):", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=2, sticky="w", padx=2)
        self.combo_estoque = ctk.CTkComboBox(
            frame_inputs, width=270, height=30, state="readonly",
            values=[
                "Todas as lojas",
                "Somente com estoque",
                "Somente sem estoque (inclui sem info)"
            ],
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            button_color=Cores.AZUL_MEDIO, button_hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.TEXTO_ESCURO, dropdown_fg_color=Cores.BRANCO,
            dropdown_text_color=Cores.TEXTO_ESCURO
        )
        self.combo_estoque.set("Todas as lojas")
        self.combo_estoque.grid(row=1, column=2, sticky="w")

        # Botões de Ação do Formulário
        frame_botoes = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_botoes.pack(anchor="w", padx=10, pady=(4, 6))

        self.btn_carregar = ctk.CTkButton(
            frame_botoes, text="Carregar Lojas", width=110, height=28, corner_radius=5,
            fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_carregar.pack(side="left", padx=(0, 8))

        self.btn_salvar = ctk.CTkButton(
            frame_botoes, text="Salvar Roteiro", width=115, height=28, corner_radius=5,
            fg_color="#2E7D32", hover_color="#1B5E20",
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_salvar.pack(side="left", padx=(0, 8))

        self.btn_limpar = ctk.CTkButton(
            frame_botoes, text="Limpar Seleção", width=110, height=28, corner_radius=5,
            fg_color=Cores.AZUL_CLARO, hover_color=Cores.AZUL_HOVER_CLARO,
            text_color=Cores.AZUL_ESCURO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_limpar.pack(side="left", padx=(0, 8))

        self.btn_cancelar = ctk.CTkButton(
            frame_botoes, text="Cancelar Edição", width=115, height=28, corner_radius=5,
            fg_color=Cores.VERMELHO, hover_color=Cores.VERMELHO_ESCURO,
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        # Inicia oculto (exibido apenas no Modo Edição)

        # Barra de Resumo
        self.frame_resumo = ctk.CTkFrame(frame_form, fg_color="#E8F5E9", corner_radius=5)
        self.lbl_resumo = ctk.CTkLabel(
            self.frame_resumo, text="", text_color="#1B5E20",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.lbl_resumo.pack(anchor="w", padx=10, pady=4)

        # Lista Rolável de Lojas da Carteira
        self.scroll_lojas = ctk.CTkScrollableFrame(
            frame_form, fg_color="#F8FAFC", corner_radius=5,
            scrollbar_button_color=Cores.CINZA_SCROLL, scrollbar_button_hover_color=Cores.AZUL_CLARO
        )
        self.scroll_lojas.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        self.exibir_mensagem_vazia_lojas(
            "Para criar novo Roteiro, selecione o promotor e a data e clique em 'Carregar Lojas'."
        )

        # =====================================================================
        # CARD INFERIOR: ROTEIROS GERADOS
        # =====================================================================
        frame_lista = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_lista.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Título + Barra de Filtro Isolada da Tabela
        topo_lista = ctk.CTkFrame(frame_lista, fg_color=Cores.TRANSPARENTE)
        topo_lista.pack(fill="x", padx=10, pady=(5, 4))

        ctk.CTkLabel(
            topo_lista, text="Roteiros Gerados",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=Cores.AZUL_ESCURO
        ).pack(side="left")

        frame_filtros = ctk.CTkFrame(topo_lista, fg_color=Cores.TRANSPARENTE)
        frame_filtros.pack(side="right")

        ctk.CTkLabel(
            frame_filtros, text="Promotor:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(0, 4))

        self.combo_filtro_promotor = ctk.CTkComboBox(
            frame_filtros, width=170, height=26, values=["Todos"], state="readonly",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            button_color=Cores.AZUL_MEDIO, button_hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.TEXTO_ESCURO, dropdown_fg_color=Cores.BRANCO,
            dropdown_text_color=Cores.TEXTO_ESCURO
        )
        self.combo_filtro_promotor.set("Todos")
        self.combo_filtro_promotor.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            frame_filtros, text="Data:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(0, 4))

        self.entrada_filtro_data = ctk.CTkEntry(
            frame_filtros, width=105, height=26, placeholder_text="DD/MM/AAAA",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_filtro_data.bind(
            "<KeyRelease>", lambda e: self._aplicar_mascara_data(self.entrada_filtro_data)
        )
        self.entrada_filtro_data.pack(side="left", padx=(0, 8))

        self.btn_filtrar_tabela = ctk.CTkButton(
            frame_filtros, text="Filtrar", width=65, height=26, corner_radius=5,
            fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_filtrar_tabela.pack(side="left", padx=(0, 4))

        self.btn_limpar_filtro_tabela = ctk.CTkButton(
            frame_filtros, text="Limpar", width=65, height=26, corner_radius=5,
            fg_color=Cores.AZUL_CLARO, hover_color=Cores.AZUL_HOVER_CLARO,
            text_color=Cores.AZUL_ESCURO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_limpar_filtro_tabela.pack(side="left")

        # Cabeçalho Sincronizado da Tabela
        self.header = ctk.CTkFrame(frame_lista, fg_color=Cores.AZUL_CLARO, corner_radius=4, height=26)
        self.header.pack(fill="x", padx=10, pady=(0, 2))

        self.header.grid_columnconfigure(0, minsize=self.LARGURA_PROMOTOR, weight=1)
        self.header.grid_columnconfigure(1, minsize=self.LARGURA_DATA, weight=0)
        self.header.grid_columnconfigure(2, minsize=self.LARGURA_LOJAS, weight=0)
        self.header.grid_columnconfigure(3, minsize=self.LARGURA_FEITAS, weight=0)
        self.header.grid_columnconfigure(4, minsize=self.LARGURA_NAO_FEITAS, weight=0)
        self.header.grid_columnconfigure(5, minsize=self.LARGURA_ACOES, weight=0)

        # GAMBIARRA PRA ALINHAR TABELA, NAO TIRAR
        debug_col2 = ctk.CTkFrame(self.header, fg_color=Cores.TRANSPARENTE, height=20, width=self.LARGURA_ACOES) # Se usar CustomTkinter, use ctk.CTkFrame(..., fg_color="red")
        debug_col2.grid(row=0, column=5, sticky="nsew")

        ctk.CTkLabel(self.header, text="PROMOTOR", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="DATA", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="LOJAS", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="FEITAS", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=3, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="NÃO FEITAS", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=4, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="AÇÕES", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=5, sticky="e", padx=self.PADDING_ACOES, pady=2)

        self.scrollable_frame = ctk.CTkScrollableFrame(
            frame_lista, fg_color=Cores.TRANSPARENTE,
            scrollbar_button_color=Cores.CINZA_SCROLL, scrollbar_button_hover_color=Cores.AZUL_CLARO
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    # --- Máscara de Data ---
    @staticmethod
    def _aplicar_mascara_data(entry):
        texto = "".join(ch for ch in entry.get() if ch.isdigit())[:8]
        novo = ""
        if len(texto) > 0:
            novo += texto[:2]
        if len(texto) >= 3:
            novo += "/" + texto[2:4]
        if len(texto) >= 5:
            novo += "/" + texto[4:8]
        if entry.get() != novo:
            entry.delete(0, "end")
            entry.insert(0, novo)

    # --- Controle de Estados (Criação vs. Edição) ---
    def entrar_modo_criacao(self):
        self.lbl_titulo_form.configure(text="Novo Roteiro", text_color=Cores.AZUL_ESCURO)
        self.combo_promotor.configure(state="readonly")
        self.entrada_data.configure(state="normal")
        self.btn_salvar.configure(text="Salvar Roteiro")
        self.btn_cancelar.pack_forget()
        self.exibir_mensagem_vazia_lojas(
            "Selecione o promotor e a data e clique em 'Carregar Lojas'."
        )

    def entrar_modo_edicao(self, promotor_nome, data_br):
        self.lbl_titulo_form.configure(
            text=f"Editando Roteiro — {promotor_nome} ({data_br})",
            text_color=Cores.AZUL_MEDIO
        )
        self.combo_promotor.set(promotor_nome)
        self.combo_promotor.configure(state="disabled")

        self.entrada_data.configure(state="normal")
        self.entrada_data.delete(0, "end")
        self.entrada_data.insert(0, data_br)
        self.entrada_data.configure(state="disabled")

        self.btn_salvar.configure(text="Salvar Alterações")
        self.btn_cancelar.pack(side="left", padx=(0, 8))

    def atualizar_combos_promotores(self, nomes):
        self.combo_promotor.configure(values=nomes)
        if nomes and self.combo_promotor.get() not in nomes:
            self.combo_promotor.set(nomes[0])

        opcoes_filtro = ["Todos"] + nomes
        self.combo_filtro_promotor.configure(values=opcoes_filtro)
        if self.combo_filtro_promotor.get() not in opcoes_filtro:
            self.combo_filtro_promotor.set("Todos")

    def atualizar_resumo(self, texto):
        if texto:
            self.lbl_resumo.configure(text=texto)
            if not self.frame_resumo.winfo_ismapped():
                self.scroll_lojas.pack_forget()
                self.frame_resumo.pack(fill="x", padx=10, pady=(0, 4))
                self.scroll_lojas.pack(fill="both", expand=True, padx=10, pady=(2, 8))
        else:
            self.frame_resumo.pack_forget()

    def exibir_mensagem_vazia_lojas(self, mensagem):
        for widget in self.scroll_lojas.winfo_children():
            widget.destroy()
        self.total_cards_exibidos = 0
        self.atualizar_resumo("")
        ctk.CTkLabel(
            self.scroll_lojas, text=mensagem,
            text_color=Cores.TEXTO_ESCURO, font=ctk.CTkFont(size=11)
        ).pack(pady=18)

    def desenhar_cards_lojas(self, lojas, selecionadas_ids, travadas_ids, texto_resumo, cmd_toggle):
        for widget in self.scroll_lojas.winfo_children():
            widget.destroy()

        self.total_cards_exibidos = len(lojas)
        self.atualizar_resumo(texto_resumo)

        if not lojas:
            self.exibir_mensagem_vazia_lojas(
                "Nenhuma loja encontrada para os critérios selecionados."
            )
            return

        for loja in lojas:
            loja_id = loja["loja_id"]
            travada = loja_id in travadas_ids

            card = ctk.CTkFrame(
                self.scroll_lojas, fg_color=Cores.BRANCO,
                border_width=1, border_color=Cores.CINZA_BORDA, corner_radius=5
            )
            card.pack(fill="x", padx=4, pady=3)
            card.grid_columnconfigure(1, weight=1)

            var_chk = tk.BooleanVar(value=(loja_id in selecionadas_ids))
            chk = ctk.CTkCheckBox(
                card, text="", variable=var_chk, width=22,
                checkbox_width=18, checkbox_height=18, border_width=2,
                fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO,
                border_color=Cores.CINZA_BORDA,
                state="disabled" if travada else "normal",
                command=lambda lid=loja_id, v=var_chk: cmd_toggle(lid, v.get())
            )
            chk.grid(row=0, column=0, rowspan=2, padx=(10, 6), pady=8, sticky="nw")

            titulo = f"{loja['nome']} — {loja['cidade']}" if loja["cidade"] else loja["nome"]
            f_titulo = ctk.CTkFrame(card, fg_color=Cores.TRANSPARENTE)
            f_titulo.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(6, 2))
            lbl_titulo = WrappableLabel(
                master=f_titulo, text=titulo, text_color=Cores.PRETO,
                fg_color=Cores.BRANCO, anchor="w", justify="left",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            lbl_titulo.pack(fill="both", expand=True)

            linha_badges = ctk.CTkFrame(card, fg_color=Cores.TRANSPARENTE)
            linha_badges.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 6))

            if loja["critica"]:
                self._criar_badge(linha_badges, "Crítica", "#FFEBEE", "#C62828")
            else:
                self._criar_badge(linha_badges, "OK", "#E8F5E9", "#2E7D32")

            estoque = loja["resumo_estoque"]
            if estoque == "tem":
                self._criar_badge(linha_badges, "Com estoque", "#E8F5E9", "#2E7D32")
            elif estoque == "nao":
                self._criar_badge(linha_badges, "Sem estoque", "#FFF3E0", "#EF6C00")
            else:
                self._criar_badge(linha_badges, "Estoque: sem info", "#ECEFF1", "#455A64")

            if travada:
                self._criar_badge(linha_badges, "Já registrada", Cores.AZUL_CLARO, Cores.AZUL_ESCURO)

            dias_txt = (
                "Nunca visitada"
                if loja["dias_sem_visita"] is None
                else f"Dias sem visita: {loja['dias_sem_visita']} dia(s)"
            )
            ctk.CTkLabel(
                linha_badges,
                text=f"{dias_txt} • Intervalo: {loja['intervalo_dias']} dias",
                text_color=Cores.TEXTO_ESCURO,
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(6, 0))

    @staticmethod
    def _criar_badge(parent, texto, cor_fundo, cor_texto):
        ctk.CTkLabel(
            parent, text=texto, fg_color=cor_fundo, text_color=cor_texto,
            corner_radius=4, padx=7, pady=1,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(side="left", padx=(0, 5))

    # --- Métodos da Tabela Inferior ---
    def limpar_tabela(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def adicionar_linha(self, promotor_nome, data_br, total_lojas, feitas, nao_feitas, cmd_editar, cmd_excluir):
        linha = ctk.CTkFrame(self.scrollable_frame, fg_color=Cores.TRANSPARENTE)
        linha.pack(fill="x", pady=1)

        linha.grid_columnconfigure(0, minsize=self.LARGURA_PROMOTOR, weight=1)
        linha.grid_columnconfigure(1, minsize=self.LARGURA_DATA, weight=0)
        linha.grid_columnconfigure(2, minsize=self.LARGURA_LOJAS, weight=0)
        linha.grid_columnconfigure(3, minsize=self.LARGURA_FEITAS, weight=0)
        linha.grid_columnconfigure(4, minsize=self.LARGURA_NAO_FEITAS, weight=0)
        linha.grid_columnconfigure(5, minsize=self.LARGURA_ACOES, weight=0)

        ctk.CTkLabel(linha, text=promotor_nome, text_color=Cores.PRETO, anchor="w", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(linha, text=data_br, text_color=Cores.PRETO, anchor="w", font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(linha, text=total_lojas, text_color=Cores.PRETO, anchor="w", font=ctk.CTkFont(size=12)).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(linha, text=feitas, text_color="#2E7D32", anchor="w", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=3, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(linha, text=nao_feitas, text_color=Cores.VERMELHO, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=4, sticky="w", padx=5, pady=2)

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

    def mostrar_mensagem(self, titulo, mensagem, tipo="info"):
        if tipo == "erro":
            messagebox.showerror(titulo, mensagem)
        else:
            messagebox.showinfo(titulo, mensagem)