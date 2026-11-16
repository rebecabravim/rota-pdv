import sqlite3
from datetime import datetime
import tkinter as tk
from models.roteiro_model import RoteiroModel
from models.promotor_model import PromotorModel


class RoteiroController:
    def __init__(self, tab_view, db):
        self.view = tab_view
        self.model = RoteiroModel(db)
        self.prom_model = PromotorModel(db)

        self.id_em_edicao = None
        self.mapa_promotores = {}
        self.lojas_valores_derivados_calculados = []
        self.lojas_selecionadas_ids = set()
        self.lojas_travadas_ids = set()

        # Vincula os comandos dos botões e filtros da View
        self.view.btn_carregar.configure(command=self.carregar_lojas)
        self.view.btn_salvar.configure(command=self.salvar)
        self.view.btn_limpar.configure(command=self.limpar_selecao)
        self.view.btn_cancelar.configure(command=self.cancelar_edicao)
        self.view.combo_estoque.configure(command=lambda _: self.aplicar_filtro_estoque())

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
        """Atualiza os combos de promotores ao abrir ou alternar para a aba Roteiro."""
        promotores = self.prom_model.buscar_todos()
        self.mapa_promotores.clear()
        nomes = []

        for p in promotores:
            p_id = p['id'] if isinstance(p, dict) or hasattr(p, 'keys') else p[0]
            nome = p['nome'] if isinstance(p, dict) or hasattr(p, 'keys') else p[1]
            self.mapa_promotores[nome] = p_id
            nomes.append(nome)

        self.view.atualizar_combos_promotores(nomes)

    def carregar_lojas(self):
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

        # No Modo Criação, bloqueia se já existir roteiro para o mesmo Promotor + Data
        if self.id_em_edicao is None:
            if self.model.existe_roteiro_na_data(promotor_id, data_iso):
                self.view.mostrar_mensagem(
                    "Roteiro Já Existente",
                    f"O promotor {promotor_nome} já possui um roteiro cadastrado para {data_br}.\n\n"
                    "Não é possível criar um novo roteiro para a mesma data e promotor.\n\n"
                    "Para alterar o roteiro existente, clique em 'Editar' na tabela de Roteiros Gerados abaixo.",
                    "erro"
                )
                self.lojas_valores_derivados_calculados = []
                self.lojas_selecionadas_ids.clear()
                self.lojas_travadas_ids.clear()
                self.view.exibir_mensagem_vazia_lojas(
                    "Já existe um roteiro nesta data. Utilize a tabela abaixo para editar ou escolha outra data."
                )
                return

            self.lojas_selecionadas_ids.clear()
            self.lojas_travadas_ids.clear()

        self.lojas_valores_derivados_calculados = self.model.buscar_lojas_valores_derivados_calculados(promotor_id, data_iso)
        self.aplicar_filtro_estoque()

    def aplicar_filtro_estoque(self):
        if not self.lojas_valores_derivados_calculados:
            return

        filtro = self.view.combo_estoque.get()
        filtradas = []

        for item in self.lojas_valores_derivados_calculados:
            estoque = item["resumo_estoque"]
            if filtro == "Somente com estoque" and estoque != "tem":
                continue
            if filtro == "Somente sem estoque (inclui sem info)" and estoque == "tem":
                continue
            filtradas.append(item)

        promotor_nome = self.view.combo_promotor.get().strip()
        data_br = self.view.entrada_data.get().strip()
        resumo = (
            f"Carregado: {promotor_nome} • {data_br} • "
            f"Lojas exibidas: {len(filtradas)} de {len(self.lojas_valores_derivados_calculados)} • "
            f"Selecionadas: {len(self.lojas_selecionadas_ids)}"
        )

        self.view.desenhar_cards_lojas(
            lojas=filtradas,
            selecionadas_ids=self.lojas_selecionadas_ids,
            travadas_ids=self.lojas_travadas_ids,
            texto_resumo=resumo,
            cmd_toggle=self.alternar_selecao_loja
        )

    def alternar_selecao_loja(self, loja_id, selecionada):
        if loja_id in self.lojas_travadas_ids:
            return

        if selecionada:
            self.lojas_selecionadas_ids.add(loja_id)
        else:
            self.lojas_selecionadas_ids.discard(loja_id)

        if self.lojas_valores_derivados_calculados:
            promotor_nome = self.view.combo_promotor.get().strip()
            data_br = self.view.entrada_data.get().strip()
            total_exibidas = self.view.total_cards_exibidos
            resumo = (
                f"Carregado: {promotor_nome} • {data_br} • "
                f"Lojas exibidas: {total_exibidas} de {len(self.lojas_valores_derivados_calculados)} • "
                f"Selecionadas: {len(self.lojas_selecionadas_ids)}"
            )
            self.view.atualizar_resumo(resumo)

    def limpar_selecao(self):
        self.lojas_selecionadas_ids = set(self.lojas_travadas_ids)
        self.aplicar_filtro_estoque()

    def salvar(self):
        promotor_nome = self.view.combo_promotor.get().strip()
        data_br = self.view.entrada_data.get().strip()

        if not promotor_nome or promotor_nome not in self.mapa_promotores:
            self.view.mostrar_mensagem("Erro", "Selecione um promotor válido.", "erro")
            return

        data_iso = self._br_para_iso(data_br)
        if not data_iso:
            self.view.mostrar_mensagem("Erro", "Informe uma data válida no formato DD/MM/AAAA.", "erro")
            return

        if not self.lojas_selecionadas_ids:
            self.view.mostrar_mensagem("Erro", "Selecione pelo menos uma loja para salvar o roteiro.", "erro")
            return

        promotor_id = self.mapa_promotores[promotor_nome]

        try:
            if self.id_em_edicao:
                self.model.atualizar(self.id_em_edicao, list(self.lojas_selecionadas_ids))
                self.view.mostrar_mensagem("Sucesso", f"Roteiro de '{promotor_nome}' ({data_br}) atualizado com sucesso!")
            else:
                if self.model.existe_roteiro_na_data(promotor_id, data_iso):
                    self.view.mostrar_mensagem(
                        "Erro",
                        f"Já existe um roteiro cadastrado para '{promotor_nome}' na data {data_br}.",
                        "erro"
                    )
                    return

                self.model.salvar(promotor_id, data_iso, list(self.lojas_selecionadas_ids))
                self.view.mostrar_mensagem("Sucesso", f"Roteiro de '{promotor_nome}' ({data_br}) criado com sucesso!")

            self.cancelar_edicao()
            self.atualizar_tabela()

        except sqlite3.IntegrityError:
            self.view.mostrar_mensagem(
                "Erro",
                "Não foi possível salvar: já existe um roteiro para este promotor nesta data.",
                "erro"
            )

    def preparar_edicao(self, roteiro_id):
        roteiro = self.model.buscar_por_id(roteiro_id)
        if not roteiro:
            self.view.mostrar_mensagem("Erro", "Roteiro não encontrado.", "erro")
            return

        r_id, promotor_id, promotor_nome, data_iso = roteiro
        data_br = self._iso_para_br(data_iso)

        self.id_em_edicao = r_id
        lojas_vinculadas = set(self.model.buscar_lojas_vinculadas(r_id))
        self.lojas_valores_derivados_calculados = self.model.buscar_lojas_valores_derivados_calculados(promotor_id, data_iso)

        ids_validos_promotor = {item["loja_id"] for item in self.lojas_valores_derivados_calculados}

        # Lojas que já tiveram visita baixada no dia ficam marcadas e travadas
        self.lojas_travadas_ids = {
            item["loja_id"] for item in self.lojas_valores_derivados_calculados if item["ja_registrada"]
        }
        self.lojas_selecionadas_ids = (lojas_vinculadas & ids_validos_promotor) | self.lojas_travadas_ids

        self.view.entrar_modo_edicao(promotor_nome, data_br)
        self.aplicar_filtro_estoque()

    def cancelar_edicao(self):
        self.id_em_edicao = None
        self.lojas_valores_derivados_calculados = []
        self.lojas_selecionadas_ids.clear()
        self.lojas_travadas_ids.clear()
        self.view.entrar_modo_criacao()

    def excluir(self, roteiro_id, promotor_nome, data_br):
        if not tk.messagebox.askyesno(
            "Confirmar",
            f"Deseja realmente excluir o roteiro de '{promotor_nome}' do dia {data_br}?"
        ):
            return

        self.model.deletar(roteiro_id)

        if self.id_em_edicao == roteiro_id:
            self.cancelar_edicao()

        self.view.mostrar_mensagem("Sucesso", "Roteiro removido com sucesso!")
        self.atualizar_tabela()

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
        roteiros = self.model.buscar_todos(promotor_id=promotor_id, data_iso=data_iso)

        for r in roteiros:
            r_id, _, promotor_nome, r_data_iso, total_lojas, feitas, nao_feitas = r
            data_br = self._iso_para_br(r_data_iso)

            self.view.adicionar_linha(
                promotor_nome=promotor_nome,
                data_br=data_br,
                total_lojas=str(total_lojas or 0),
                feitas=str(feitas or 0),
                nao_feitas=str(nao_feitas or 0),
                cmd_editar=lambda rid=r_id: self.preparar_edicao(rid),
                cmd_excluir=lambda rid=r_id, p=promotor_nome, d=data_br: self.excluir(rid, p, d)
            )

    def limpar_filtros_tabela(self):
        self.view.combo_filtro_promotor.set("Todos")
        self.view.entrada_filtro_data.delete(0, 'end')
        self.atualizar_tabela()