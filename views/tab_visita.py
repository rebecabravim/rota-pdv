from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from views.utils import WrappableLabel
from views.styles import Cores


class TabVisita:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.controles_industrias = {}

        # Larguras fixas sincronizadas entre Cabeçalho e Linhas da Tabela Inferior
        self.LARGURA_PROMOTOR = 190
        self.LARGURA_DATA = 100
        self.LARGURA_LOJA = 230
        self.LARGURA_STATUS = 110
        self.LARGURA_ACOES = 120
        self.PADDING_ACOES = 20

        # =====================================================================
        # CARD SUPERIOR: REGISTRAR VISITA / EDITANDO VISITA (TUDO EM 1 LINHA)
        # =====================================================================
        frame_form = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_form.pack(fill="x", padx=5, pady=(5, 6))

        self.lbl_titulo_form = ctk.CTkLabel(
            frame_form,
            text="Registrar Visita",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=Cores.AZUL_ESCURO
        )
        self.lbl_titulo_form.pack(anchor="w", padx=10, pady=(4, 2))

        # Linha única: Promotor | Data | Carregar | Loja | Status | Obs | Salvar
        frame_linha1 = ctk.CTkFrame(frame_form, fg_color=Cores.TRANSPARENTE)
        frame_linha1.pack(fill="x", padx=10, pady=(0, 4))
        frame_linha1.grid_columnconfigure(5, weight=1)

        # 0. PROMOTOR
        ctk.CTkLabel(
            frame_linha1, text="Promotor:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=0, sticky="w", padx=2)
        self.combo_promotor = ctk.CTkComboBox(
            frame_linha1, width=155, height=30, values=[], state="readonly",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            button_color=Cores.AZUL_MEDIO, button_hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.TEXTO_ESCURO, dropdown_fg_color=Cores.BRANCO,
            dropdown_text_color=Cores.TEXTO_ESCURO
        )
        self.combo_promotor.grid(row=1, column=0, padx=(0, 6), sticky="w")

        # 1. DATA
        ctk.CTkLabel(
            frame_linha1, text="Data:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=1, sticky="w", padx=2)
        self.entrada_data = ctk.CTkEntry(
            frame_linha1, width=95, height=30, placeholder_text="DD/MM/AAAA",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entrada_data.bind("<KeyRelease>", lambda e: self._aplicar_mascara_data(self.entrada_data))
        self.entrada_data.grid(row=1, column=1, padx=(0, 6), sticky="w")

        # 2. BOTÃO CARREGAR ROTEIRO
        self.btn_carregar_roteiro = ctk.CTkButton(
            frame_linha1, text="Carregar Roteiro", width=105, height=30, corner_radius=5,
            fg_color=Cores.AZUL_MEDIO, hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_carregar_roteiro.grid(row=1, column=2, padx=(0, 8), sticky="w")

        # 3. LOJA AGENDADA NO ROTEIRO
        ctk.CTkLabel(
            frame_linha1, text="Loja Agendada no Roteiro:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=3, sticky="w", padx=2)
        self.combo_loja = ctk.CTkComboBox(
            frame_linha1, width=195, height=30, values=[], state="disabled",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            button_color=Cores.AZUL_MEDIO, button_hover_color=Cores.AZUL_ESCURO,
            text_color=Cores.TEXTO_ESCURO, dropdown_fg_color=Cores.BRANCO,
            dropdown_text_color=Cores.TEXTO_ESCURO
        )
        self.combo_loja.grid(row=1, column=3, padx=(0, 10), sticky="w")

        # 4. STATUS DA VISITA (Bolinhas sem fundo cinza)
        ctk.CTkLabel(
            frame_linha1, text="Status da Visita:", text_color=Cores.PRETO, font=ctk.CTkFont(size=11)
        ).grid(row=0, column=4, sticky="w", padx=2)

        frame_radios_status = ctk.CTkFrame(frame_linha1, fg_color=Cores.TRANSPARENTE)
        frame_radios_status.grid(row=1, column=4, sticky="w", padx=(0, 10))

        self.var_status = tk.StringVar(value="Feita")

        self.radio_feita = ctk.CTkRadioButton(
            frame_radios_status,
            text="Feita",
            variable=self.var_status,
            value="Feita",
            width=55,
            radiobutton_width=15,
            radiobutton_height=15,
            border_width_checked=5,
            fg_color=Cores.AZUL_MEDIO,
            hover_color=Cores.AZUL_ESCURO,
            border_color=Cores.CINZA_BORDA,
            text_color=Cores.PRETO,
            font=ctk.CTkFont(size=11)
        )
        self.radio_feita.pack(side="left", padx=(0, 6))

        self.radio_nao_feita = ctk.CTkRadioButton(
            frame_radios_status,
            text="Não Feita",
            variable=self.var_status,
            value="Não Feita",
            width=75,
            radiobutton_width=15,
            radiobutton_height=15,
            border_width_checked=5,
            fg_color=Cores.AZUL_MEDIO,
            hover_color=Cores.AZUL_ESCURO,
            border_color=Cores.CINZA_BORDA,
            text_color=Cores.PRETO,
            font=ctk.CTkFont(size=11)
        )
        self.radio_nao_feita.pack(side="left")

        # 5. OBSERVAÇÃO GERAL (Compacta na mesma linha)
        self.lbl_obs_geral = ctk.CTkLabel(
            frame_linha1,
            text="Observação (Opcional):",
            text_color=Cores.PRETO,
            font=ctk.CTkFont(size=11)
        )
        self.lbl_obs_geral.grid(row=0, column=5, sticky="w", padx=2)

        self.entrada_obs_geral = ctk.CTkEntry(
            frame_linha1, width=130, height=30,
            placeholder_text="Obs. ou motivo...",
            fg_color=Cores.BRANCO, border_color=Cores.CINZA_BORDA, border_width=1,
            corner_radius=5, text_color=Cores.TEXTO_ESCURO
        )
        self.entrada_obs_geral.grid(row=1, column=5, sticky="ew", padx=(0, 8))

        # 6. BOTÕES SALVAR / CANCELAR EDIÇÃO
        frame_botoes = ctk.CTkFrame(frame_linha1, fg_color=Cores.TRANSPARENTE)
        frame_botoes.grid(row=1, column=6, sticky="e")

        self.btn_salvar = ctk.CTkButton(
            frame_botoes, text="Salvar Visita", width=95, height=30, corner_radius=5,
            fg_color="#2E7D32", hover_color="#1B5E20",
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_salvar.pack(side="left")

        self.btn_cancelar = ctk.CTkButton(
            frame_botoes, text="Cancelar", width=75, height=30, corner_radius=5,
            fg_color=Cores.VERMELHO, hover_color=Cores.VERMELHO_ESCURO,
            text_color=Cores.BRANCO, font=ctk.CTkFont(size=11, weight="bold")
        )
        # Inicia oculto (exibido apenas no Modo Edição)

        # Seção de Auditoria por Indústria (altura compacta para ampliar a tabela abaixo)
        ctk.CTkLabel(
            frame_form,
            text="Auditoria de Estoque por Indústria:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Cores.AZUL_ESCURO
        ).pack(anchor="w", padx=10, pady=(2, 2))

        self.scroll_industrias = ctk.CTkScrollableFrame(
            frame_form, height=95, fg_color=Cores.TRANSPARENTE, corner_radius=5,
            scrollbar_button_color=Cores.CINZA_SCROLL, scrollbar_button_hover_color=Cores.AZUL_CLARO
        )
        self.scroll_industrias.pack(fill="x", padx=10, pady=(0, 6))

        self.exibir_mensagem_industrias(
            "Selecione o promotor e a data e clique em 'Carregar Roteiro'."
        )

        # =====================================================================
        # CARD INFERIOR: VISITAS REGISTRADAS (COM MAIOR ALTURA)
        # =====================================================================
        frame_lista = ctk.CTkFrame(self.parent, fg_color=Cores.BRANCO, corner_radius=6)
        frame_lista.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        topo_lista = ctk.CTkFrame(frame_lista, fg_color=Cores.TRANSPARENTE)
        topo_lista.pack(fill="x", padx=10, pady=(5, 4))

        ctk.CTkLabel(
            topo_lista, text="Visitas Registradas",
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

        self.header.grid_columnconfigure(0, minsize=self.LARGURA_PROMOTOR, weight=0)
        self.header.grid_columnconfigure(1, minsize=self.LARGURA_DATA, weight=0)
        self.header.grid_columnconfigure(2, minsize=self.LARGURA_LOJA, weight=0)
        self.header.grid_columnconfigure(3, minsize=self.LARGURA_STATUS, weight=0)
        self.header.grid_columnconfigure(4, weight=1)
        self.header.grid_columnconfigure(5, minsize=self.LARGURA_ACOES, weight=0)

        ctk.CTkLabel(self.header, text="PROMOTOR", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="DATA", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="LOJA", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="STATUS", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=3, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="ESTOQUE / OBSERVAÇÃO", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=4, sticky="w", padx=5, pady=2)
        ctk.CTkLabel(self.header, text="AÇÕES", font=ctk.CTkFont(size=11, weight="bold"), text_color=Cores.AZUL_ESCURO).grid(row=0, column=5, sticky="e", padx=self.PADDING_ACOES, pady=2)

        self.scrollable_frame = ctk.CTkScrollableFrame(
            frame_lista, fg_color=Cores.TRANSPARENTE,
            scrollbar_button_color=Cores.CINZA_SCROLL, scrollbar_button_hover_color=Cores.AZUL_CLARO
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def configurar_comando_status(self, cmd):
        self.radio_feita.configure(command=cmd)
        self.radio_nao_feita.configure(command=cmd)

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
        self.lbl_titulo_form.configure(text="Registrar Visita", text_color=Cores.AZUL_ESCURO)
        self.combo_promotor.configure(state="readonly")
        self.entrada_data.configure(state="normal")
        self.btn_carregar_roteiro.configure(state="normal")

        self.combo_loja.configure(values=[], state="disabled")
        self.combo_loja.set("")

        self.var_status.set("Feita")
        self.lbl_obs_geral.configure(text="Observação (Opcional):")
        self.entrada_obs_geral.delete(0, "end")

        self.btn_salvar.configure(text="Salvar Visita")
        self.btn_cancelar.pack_forget()
        self.exibir_mensagem_industrias(
            "Selecione o promotor e a data e clique em 'Carregar Roteiro'."
        )

    def entrar_modo_edicao(self, promotor_nome, data_br, loja_rotulo, status_ui, obs_geral):
        self.lbl_titulo_form.configure(
            text=f"Editando Visita — {promotor_nome} • {loja_rotulo} ({data_br})",
            text_color=Cores.AZUL_MEDIO
        )
        self.combo_promotor.set(promotor_nome)
        self.combo_promotor.configure(state="disabled")

        self.entrada_data.configure(state="normal")
        self.entrada_data.delete(0, "end")
        self.entrada_data.insert(0, data_br)
        self.entrada_data.configure(state="disabled")

        self.btn_carregar_roteiro.configure(state="disabled")

        self.combo_loja.configure(values=[loja_rotulo], state="normal")
        self.combo_loja.set(loja_rotulo)
        self.combo_loja.configure(state="disabled")

        self.var_status.set(status_ui)
        self.entrada_obs_geral.delete(0, "end")
        self.entrada_obs_geral.insert(0, obs_geral)

        self.btn_salvar.configure(text="Salvar Alterações")
        self.btn_cancelar.pack(side="left", padx=(6, 0))

    def atualizar_combos_promotores(self, nomes):
        self.combo_promotor.configure(values=nomes)
        if nomes and self.combo_promotor.get() not in nomes:
            self.combo_promotor.set(nomes[0])

        opcoes_filtro = ["Todos"] + nomes
        self.combo_filtro_promotor.configure(values=opcoes_filtro)
        if self.combo_filtro_promotor.get() not in opcoes_filtro:
            self.combo_filtro_promotor.set("Todos")

    def atualizar_combo_lojas(self, nomes_lojas):
        if nomes_lojas:
            self.combo_loja.configure(values=nomes_lojas, state="readonly")
            self.combo_loja.set(nomes_lojas[0])
        else:
            self.combo_loja.configure(values=[], state="normal")
            self.combo_loja.set("")
            self.combo_loja.configure(state="disabled")

    # --- Renderização da Auditoria de Indústrias ---
    def exibir_mensagem_industrias(self, mensagem):
        for widget in self.scroll_industrias.winfo_children():
            widget.destroy()
        self.controles_industrias.clear()

        ctk.CTkLabel(
            self.scroll_industrias,
            text=mensagem,
            text_color=Cores.TEXTO_ESCURO,
            font=ctk.CTkFont(size=11)
        ).pack(pady=14)

    def desenhar_industrias(self, itens):
        for widget in self.scroll_industrias.winfo_children():
            widget.destroy()
        self.controles_industrias.clear()

        for item in itens:
            ind_id = item["industria_id"]
            linha = ctk.CTkFrame(
                self.scroll_industrias,
                fg_color=Cores.BRANCO,
                border_width=1,
                border_color=Cores.CINZA_BORDA,
                corner_radius=5
            )
            linha.pack(fill="x", padx=2, pady=2)
            linha.grid_columnconfigure(0, minsize=180, weight=0)
            linha.grid_columnconfigure(1, minsize=250, weight=0)
            linha.grid_columnconfigure(2, weight=1)

            ctk.CTkLabel(
                linha,
                text=item["nome"],
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=Cores.AZUL_ESCURO,
                anchor="w"
            ).grid(row=0, column=0, sticky="w", padx=(10, 8), pady=5)

            var_estoque = tk.StringVar(value=item.get("estoque", "tem"))
            frame_radios = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
            frame_radios.grid(row=0, column=1, sticky="w", padx=4, pady=3)

            opcoes = [("Com estoque", "tem"), ("Sem estoque", "nao"), ("N/A", "na")]
            for texto_op, valor_op in opcoes:
                ctk.CTkRadioButton(
                    frame_radios,
                    text=texto_op,
                    variable=var_estoque,
                    value=valor_op,
                    radiobutton_width=16,
                    radiobutton_height=16,
                    border_width_checked=5,
                    fg_color=Cores.AZUL_MEDIO,
                    hover_color=Cores.AZUL_ESCURO,
                    border_color=Cores.CINZA_BORDA,
                    text_color=Cores.PRETO,
                    font=ctk.CTkFont(size=11)
                ).pack(side="left", padx=(0, 8))

            entrada_obs = ctk.CTkEntry(
                linha,
                height=26,
                placeholder_text="Obs. da indústria (opcional)",
                fg_color=Cores.BRANCO,
                border_color=Cores.CINZA_BORDA,
                border_width=1,
                corner_radius=4,
                text_color=Cores.TEXTO_ESCURO,
                font=ctk.CTkFont(size=11)
            )
            if item.get("obs"):
                entrada_obs.insert(0, item["obs"])
            entrada_obs.grid(row=0, column=2, sticky="ew", padx=(4, 10), pady=3)

            self.controles_industrias[ind_id] = {
                "var_estoque": var_estoque,
                "entrada_obs": entrada_obs,
            }

    def obter_itens_industrias(self):
        itens = []
        for ind_id, ctrls in self.controles_industrias.items():
            itens.append({
                "industria_id": ind_id,
                "estoque": ctrls["var_estoque"].get(),
                "obs": ctrls["entrada_obs"].get().strip(),
            })
        return itens

    # --- Métodos da Tabela Inferior ---
    def limpar_tabela(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def adicionar_linha(self, promotor_nome, data_br, loja_nome, status, detalhe, cmd_editar, cmd_excluir):
        linha = ctk.CTkFrame(self.scrollable_frame, fg_color=Cores.TRANSPARENTE)
        linha.pack(fill="x", pady=1)

        linha.grid_columnconfigure(0, minsize=self.LARGURA_PROMOTOR, weight=0)
        linha.grid_columnconfigure(1, minsize=self.LARGURA_DATA, weight=0)
        linha.grid_columnconfigure(2, minsize=self.LARGURA_LOJA, weight=0)
        linha.grid_columnconfigure(3, minsize=self.LARGURA_STATUS, weight=0)
        linha.grid_columnconfigure(4, weight=1)
        linha.grid_columnconfigure(5, minsize=self.LARGURA_ACOES, weight=0)

        ctk.CTkLabel(linha, text=promotor_nome, text_color=Cores.PRETO, anchor="w", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="nw", padx=5, pady=4)
        ctk.CTkLabel(linha, text=data_br, text_color=Cores.PRETO, anchor="w", font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="nw", padx=5, pady=4)

        f_loja = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        f_loja.grid(row=0, column=2, sticky="nsew", padx=5, pady=2)
        WrappableLabel(master=f_loja, text=loja_nome, text_color=Cores.PRETO, fg_color=Cores.BRANCO, anchor="w", justify="left").pack(fill="both", expand=True)

        # Badge de Status
        f_status = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        f_status.grid(row=0, column=3, sticky="nw", padx=5, pady=4)
        if status == "feita":
            ctk.CTkLabel(
                f_status, text="Feita", fg_color="#E8F5E9", text_color="#2E7D32",
                corner_radius=4, padx=8, pady=1, font=ctk.CTkFont(size=11, weight="bold")
            ).pack(anchor="w")
        else:
            ctk.CTkLabel(
                f_status, text="Não Feita", fg_color="#FFEBEE", text_color="#C62828",
                corner_radius=4, padx=8, pady=1, font=ctk.CTkFont(size=11, weight="bold")
            ).pack(anchor="w")

        f_detalhe = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        f_detalhe.grid(row=0, column=4, sticky="nsew", padx=5, pady=2)
        WrappableLabel(master=f_detalhe, text=detalhe, text_color=Cores.PRETO, fg_color=Cores.BRANCO, anchor="w", justify="left").pack(fill="both", expand=True)

        frame_acoes = ctk.CTkFrame(linha, fg_color=Cores.TRANSPARENTE)
        frame_acoes.grid(row=0, column=5, sticky="ne", padx=5, pady=3)

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