from datetime import datetime
import tkinter as tk
from models.visita_model import VisitaModel
from models.promotor_model import PromotorModel


class VisitaController:
    def __init__(self, tab_view, db, on_visita_alterada=None):
        self.view = tab_view
        self.model = VisitaModel(db)
        self.prom_model = PromotorModel(db)
        self.on_visita_alterada = on_visita_alterada

        self.id_em_edicao = None
        self.roteiro_atual_id = None
        self.mapa_promotores = {}
        self.mapa_lojas_roteiro = {}

        # Vincula eventos da View
        self.view.btn_carregar_roteiro.configure(command=self.carregar_roteiro_do_dia)
        self.view.combo_loja.configure(command=lambda _: self.carregar_industrias_da_loja())
        self.view.configurar_comando_status(self.alternar_status_visita)
        self.view.btn_salvar.configure(command=self.salvar)
        self.view.btn_cancelar.configure(command=self.cancelar_edicao)

        self.view.btn_filtrar_tabela.configure(command=self.atualizar_tabela)
        self.view.btn_limpar_filtro_tabela.configure(command=self.limpar_filtros_tabela)

        # Carga inicial
        self.recarregar_opcoes()
        self.atualizar_tabela()

    @staticmethod
    def _br_para_iso(data_br):
        try:
            return datetime.strptime(data_br.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None

    @staticmethod
    def _iso_para_br(data_iso):
        try:
            return datetime.strptime(data_iso.strip(), "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            return data_iso

    def recarregar_opcoes(self):
        """Atualiza os combos de promotores ao abrir ou alternar para a aba Visitas."""
        promotores = self.prom_model.buscar_todos()
        self.mapa_promotores.clear()
        nomes = []

        for p in promotores:
            p_id = p['id'] if isinstance(p, dict) or hasattr(p, 'keys') else p[0]
            nome = p['nome'] if isinstance(p, dict) or hasattr(p, 'keys') else p[1]
            self.mapa_promotores[nome] = p_id
            nomes.append(nome)

        self.view.atualizar_combos_promotores(nomes)

    def carregar_roteiro_do_dia(self):
        """Carrega exclusivamente as lojas pendentes do roteiro do promotor na data informada."""
        if self.id_em_edicao is not None:
            return

        promotor_nome = self.view.combo_promotor.get().strip()
        data_br = self.view.entrada_data.get().strip()

        if not promotor_nome or promotor_nome not in self.mapa_promotores:
            self.view.mostrar_mensagem("Erro", "Selecione um promotor válido.", "erro")
            return

        data_iso = self._br_para_iso(data_br)
        if not data_iso:
            self.view.mostrar_mensagem("Erro", "Informe uma data válida no formato DD/MM/AAAA.", "erro")
            return

        promotor_id = self.mapa_promotores[promotor_nome]
        roteiro_id, lojas_pendentes = self.model.buscar_roteiro_e_lojas_pendentes(promotor_id, data_iso)

        self.roteiro_atual_id = roteiro_id
        self.mapa_lojas_roteiro.clear()

        if roteiro_id is None:
            self.view.atualizar_combo_lojas([])
            self.view.exibir_mensagem_industrias(
                "Nenhum roteiro cadastrado para este promotor nesta data. Crie o roteiro antes de registrar visitas."
            )
            self.view.mostrar_mensagem(
                "Roteiro Não Encontrado",
                f"Não existe roteiro cadastrado para '{promotor_nome}' no dia {data_br}.\n\n"
                "Não é permitido registrar visitas avulsas. Cadastre o roteiro na aba 'Roteiro' primeiro.",
                "erro"
            )
            return

        if not lojas_pendentes:
            self.view.atualizar_combo_lojas([])
            self.view.exibir_mensagem_industrias(
                "Todas as lojas deste roteiro já tiveram visita registrada nesta data."
            )
            self.view.mostrar_mensagem(
                "Roteiro Concluído",
                f"Todas as lojas agendadas para '{promotor_nome}' em {data_br} já foram registradas."
            )
            return

        nomes_lojas = []
        for loja_id, nome, cidade in lojas_pendentes:
            rotulo = f"{nome} — {cidade}" if cidade else nome
            self.mapa_lojas_roteiro[rotulo] = loja_id
            nomes_lojas.append(rotulo)

        self.view.atualizar_combo_lojas(nomes_lojas)
        self.carregar_industrias_da_loja()

    def carregar_industrias_da_loja(self):
        promotor_nome = self.view.combo_promotor.get().strip()
        loja_rotulo = self.view.combo_loja.get().strip()

        if not promotor_nome or promotor_nome not in self.mapa_promotores:
            return
        if not loja_rotulo or loja_rotulo not in self.mapa_lojas_roteiro:
            self.view.exibir_mensagem_industrias("Selecione uma loja do roteiro acima.")
            return

        promotor_id = self.mapa_promotores[promotor_nome]
        loja_id = self.mapa_lojas_roteiro[loja_rotulo]

        if self.view.var_status.get() == "Não Feita":
            self.view.exibir_mensagem_industrias(
                "Visita marcada como 'Não Feita' — auditoria de estoque desabilitada. Informe o motivo acima."
            )
            return

        industrias = self.model.buscar_industrias_auditaveis(loja_id, promotor_id)
        if not industrias:
            self.view.exibir_mensagem_industrias(
                "Nenhuma indústria em comum entre este promotor e esta loja."
            )
            return

        itens_formatados = [
            {"industria_id": ind_id, "nome": ind_nome, "estoque": "tem", "obs": ""}
            for ind_id, ind_nome in industrias
        ]
        self.view.desenhar_industrias(itens_formatados)

    def alternar_status_visita(self):
        status_atual = self.view.var_status.get()
        if status_atual == "Não Feita":
            self.view.lbl_obs_geral.configure(text="Motivo (Obrigatório):")
            self.view.exibir_mensagem_industrias(
                "Visita marcada como 'Não Feita' — auditoria de estoque desabilitada. Informe o motivo acima."
            )
        else:
            self.view.lbl_obs_geral.configure(text="Observação (Opcional):")
            if self.id_em_edicao:
                self._recarregar_industrias_edicao()
            else:
                self.carregar_industrias_da_loja()

    def _recarregar_industrias_edicao(self):
        visita = self.model.buscar_por_id(self.id_em_edicao)
        if not visita:
            return
        _, _, promotor_id, _, loja_id, _, _, _, _, _ = visita

        salvos = {
            ind_id: {"estoque": est, "obs": obs or ""}
            for ind_id, _, est, obs in self.model.buscar_itens_visita(self.id_em_edicao)
        }
        auditaveis = self.model.buscar_industrias_auditaveis(loja_id, promotor_id)

        if not auditaveis and not salvos:
            self.view.exibir_mensagem_industrias(
                "Nenhuma indústria em comum entre este promotor e esta loja."
            )
            return

        itens_formatados = []
        ids_processados = set()
        for ind_id, ind_nome in auditaveis:
            dados = salvos.get(ind_id, {"estoque": "tem", "obs": ""})
            itens_formatados.append({
                "industria_id": ind_id,
                "nome": ind_nome,
                "estoque": dados["estoque"],
                "obs": dados["obs"],
            })
            ids_processados.add(ind_id)

        for ind_id, ind_nome, est, obs in self.model.buscar_itens_visita(self.id_em_edicao):
            if ind_id not in ids_processados:
                itens_formatados.append({
                    "industria_id": ind_id,
                    "nome": ind_nome,
                    "estoque": est,
                    "obs": obs or "",
                })

        self.view.desenhar_industrias(itens_formatados)

    def salvar(self):
        promotor_nome = self.view.combo_promotor.get().strip()
        data_br = self.view.entrada_data.get().strip()
        loja_rotulo = self.view.combo_loja.get().strip()
        status_ui = self.view.var_status.get()
        status_db = "feita" if status_ui == "Feita" else "nao_feita"
        obs_geral = self.view.entrada_obs_geral.get().strip()

        if not promotor_nome or promotor_nome not in self.mapa_promotores:
            self.view.mostrar_mensagem("Erro", "Selecione um promotor válido.", "erro")
            return

        data_iso = self._br_para_iso(data_br)
        if not data_iso:
            self.view.mostrar_mensagem("Erro", "Informe uma data válida no formato DD/MM/AAAA.", "erro")
            return

        if status_db == "nao_feita" and not obs_geral:
            self.view.mostrar_mensagem(
                "Erro",
                "Para visitas marcadas como 'Não Feita', informe o motivo na Observação Geral.",
                "erro"
            )
            return

        itens_industrias = self.view.obter_itens_industrias() if status_db == "feita" else []

        if self.id_em_edicao:
            self.model.atualizar(self.id_em_edicao, status_db, obs_geral, itens_industrias)
            self.view.mostrar_mensagem("Sucesso", "Visita atualizada com sucesso!")
            self.cancelar_edicao()
            self.atualizar_tabela()
            if self.on_visita_alterada:
                self.on_visita_alterada()
            return

        if not self.roteiro_atual_id or loja_rotulo not in self.mapa_lojas_roteiro:
            self.view.mostrar_mensagem(
                "Erro",
                "Carregue o roteiro do dia e selecione uma loja agendada antes de salvar.",
                "erro"
            )
            return

        promotor_id = self.mapa_promotores[promotor_nome]
        loja_id = self.mapa_lojas_roteiro[loja_rotulo]

        if self.model.loja_ja_registrada_na_data(loja_id, promotor_id, data_iso):
            self.view.mostrar_mensagem(
                "Erro",
                "Esta loja já possui visita registrada nesta data.",
                "erro"
            )
            self.carregar_roteiro_do_dia()
            return

        self.model.salvar(
            roteiro_id=self.roteiro_atual_id,
            promotor_id=promotor_id,
            loja_id=loja_id,
            data_iso=data_iso,
            status=status_db,
            obs_geral=obs_geral,
            itens_industrias=itens_industrias
        )

        self.view.mostrar_mensagem("Sucesso", f"Visita em '{loja_rotulo}' registrada com sucesso!")
        self.view.entrada_obs_geral.delete(0, "end")
        self.view.var_status.set("Feita")
        self.view.lbl_obs_geral.configure(text="Observação Geral (Opcional):")

        self.carregar_roteiro_do_dia()
        self.atualizar_tabela()
        if self.on_visita_alterada:
            self.on_visita_alterada()

    def preparar_edicao(self, visita_id):
        visita = self.model.buscar_por_id(visita_id)
        if not visita:
            self.view.mostrar_mensagem("Erro", "Visita não encontrada.", "erro")
            return

        v_id, roteiro_id, promotor_id, promotor_nome, loja_id, loja_nome, loja_cidade, data_iso, status, obs_geral = visita
        data_br = self._iso_para_br(data_iso)
        loja_rotulo = f"{loja_nome} — {loja_cidade}" if loja_cidade else loja_nome
        status_ui = "Feita" if status == "feita" else "Não Feita"

        self.id_em_edicao = v_id
        self.roteiro_atual_id = roteiro_id
        self.mapa_lojas_roteiro = {loja_rotulo: loja_id}

        self.view.entrar_modo_edicao(promotor_nome, data_br, loja_rotulo, status_ui, obs_geral or "")
        self.alternar_status_visita()

    def cancelar_edicao(self):
        self.id_em_edicao = None
        self.roteiro_atual_id = None
        self.mapa_lojas_roteiro.clear()
        self.view.entrar_modo_criacao()

    def excluir(self, visita_id, loja_nome, data_br):
        if not tk.messagebox.askyesno(
            "Confirmar",
            f"Deseja realmente excluir o registro de visita na loja '{loja_nome}' do dia {data_br}?"
        ):
            return

        self.model.deletar(visita_id)

        if self.id_em_edicao == visita_id:
            self.cancelar_edicao()

        self.view.mostrar_mensagem("Sucesso", "Registro de visita removido com sucesso!")
        self.atualizar_tabela()
        if self.on_visita_alterada:
            self.on_visita_alterada()

    def atualizar_tabela(self):
        filtro_promotor = self.view.combo_filtro_promotor.get().strip()
        filtro_data_br = self.view.entrada_filtro_data.get().strip()

        promotor_id = None
        if filtro_promotor and filtro_promotor != "Todos":
            promotor_id = self.mapa_promotores.get(filtro_promotor)

        data_iso = None
        if filtro_data_br:
            data_iso = self._br_para_iso(filtro_data_br)
            if not data_iso:
                self.view.mostrar_mensagem(
                    "Erro",
                    "Informe uma data válida (DD/MM/AAAA) no filtro da tabela.",
                    "erro"
                )
                return

        self.view.limpar_tabela()
        visitas = self.model.buscar_todas(promotor_id=promotor_id, data_iso=data_iso)

        for v in visitas:
            v_id, promotor_nome, v_data_iso, loja_nome, loja_cidade, status, obs_geral, resumo_ind = v
            data_br = self._iso_para_br(v_data_iso)
            loja_exibicao = f"{loja_nome} ({loja_cidade})" if loja_cidade else loja_nome

            if status == "feita":
                detalhe = resumo_ind
                if obs_geral:
                    detalhe += f"\nObs: {obs_geral}"
            else:
                detalhe = f"Motivo: {obs_geral}" if obs_geral else "Não realizada"

            self.view.adicionar_linha(
                promotor_nome=promotor_nome,
                data_br=data_br,
                loja_nome=loja_exibicao,
                status=status,
                detalhe=detalhe,
                cmd_editar=lambda vid=v_id: self.preparar_edicao(vid),
                cmd_excluir=lambda vid=v_id, l=loja_nome, d=data_br: self.excluir(vid, l, d)
            )

    def limpar_filtros_tabela(self):
        self.view.combo_filtro_promotor.set("Todos")
        self.view.entrada_filtro_data.delete(0, "end")
        self.atualizar_tabela()