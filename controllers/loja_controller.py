from models.loja_model import LojaModel
from models.industria_model import IndustriaModel
from models.promotor_model import PromotorModel
import tkinter as tk

class LojaController:
    def __init__(self, tab_view, db):
        self.view = tab_view
        self.model = LojaModel(db)
        self.ind_model = IndustriaModel(db)
        self.prom_model = PromotorModel(db)

        self.id_em_edicao = None

        # Vincula as ações dos botões aos métodos do controlador
        self.view.btn_salvar.configure(command=self.salvar)
        self.view.btn_cancelar.configure(command=self.cancelar_edicao)

        # Carrega inicialmente as caixas de seleção e a lista de lojas
        self.recarregar_opcoes_checks()
        self.atualizar_tabela()

    def recarregar_opcoes_checks(self):
        """Atualiza a lista de promotores e indústrias nos checkboxes do formulário"""
        promotores = self.prom_model.buscar_todos()
        industrias = self.ind_model.buscar_todas()

        proms_selecionados = []
        inds_selecionadas = []

        if self.id_em_edicao:
            proms_selecionados = self.model.buscar_promotores_vinculados(self.id_em_edicao)
            inds_selecionadas = self.model.buscar_industrias_vinculadas(self.id_em_edicao)

        self.view.desenhar_checkboxes_promotores(promotores, proms_selecionados)
        self.view.desenhar_checkboxes_industrias(industrias, inds_selecionadas)

    def salvar(self):
        nome = self.view.entrada_nome.get().strip()
        cidade = self.view.entrada_cidade.get().strip()
        endereco = self.view.entrada_endereco.get().strip()
        intervalo_raw = self.view.entrada_intervalo.get().strip()

        # Validações dos campos obrigatórios conforme regras de negócio
        if not nome or not cidade:
            self.view.mostrar_mensagem("Erro", "Nome e Cidade são campos obrigatórios.", "erro")
            return

        try:
            intervalo_dias = int(intervalo_raw) if intervalo_raw else 7
            if intervalo_dias < 1:
                intervalo_dias = 1
        except ValueError:
            self.view.mostrar_mensagem("Erro", "O intervalo de visita deve ser um número inteiro válido.", "erro")
            return

        if self.model.nome_ja_existe(nome, cidade, self.id_em_edicao):
            self.view.mostrar_mensagem("Erro", f"Já existe uma loja chamada '{nome}' na cidade '{cidade}'.", "erro")
            return

        # Recupera os IDs selecionados nos checkboxes da View
        promotores_ids = self.view.obter_promotores_selecionados()
        industrias_ids = self.view.obter_industrias_selecionadas()

        if self.id_em_edicao:
            self.model.atualizar(
                self.id_em_edicao, nome, cidade, endereco, intervalo_dias, promotores_ids, industrias_ids
            )
            self.view.mostrar_mensagem("Sucesso", f"Loja '{nome}' atualizada com sucesso!")
        else:
            self.model.salvar(
                nome, cidade, endereco, intervalo_dias, promotores_ids, industrias_ids
            )
            self.view.mostrar_mensagem("Sucesso", f"Loja '{nome}' cadastrada com sucesso!")

        self.cancelar_edicao()
        self.atualizar_tabela()

    def preparar_edicao(self, loja_id, nome, cidade, endereco, intervalo_dias):
        self.id_em_edicao = loja_id

        # Preenche os campos do formulário
        self.view.entrada_nome.delete(0, 'end')
        self.view.entrada_nome.insert(0, nome)

        self.view.entrada_cidade.delete(0, 'end')
        self.view.entrada_cidade.insert(0, cidade)

        self.view.entrada_endereco.delete(0, 'end')
        self.view.entrada_endereco.insert(0, endereco or "")

        self.view.entrada_intervalo.delete(0, 'end')
        self.view.entrada_intervalo.insert(0, str(intervalo_dias))

        # Já usa self.model internamente porque self.id_em_edicao foi definido acima
        self.recarregar_opcoes_checks()

        # Atualiza o estado visual do formulário
        self.view.btn_salvar.configure(text="Salvar")
        self.view.btn_cancelar.pack(side=tk.LEFT, padx=10)

    def cancelar_edicao(self):
        self.id_em_edicao = None

        # Limpa os campos de texto
        self.view.entrada_nome.delete(0, 'end')
        self.view.entrada_cidade.delete(0, 'end')
        self.view.entrada_endereco.delete(0, 'end')
        self.view.entrada_intervalo.delete(0, 'end')
        self.view.entrada_intervalo.insert(0, "7")

        # Limpa as caixas de seleção
        self.recarregar_opcoes_checks()

        # Restaura os botões
        self.view.btn_salvar.configure(text="Salvar")
        self.view.btn_cancelar.pack_forget()

    def excluir(self, loja_id, nome_loja):
        if not tk.messagebox.askyesno("Confirmar", f"Deseja realmente excluir a loja '{nome_loja}'?"):
            return

        self.model.deletar(loja_id)

        if self.id_em_edicao == loja_id:
            self.cancelar_edicao()

        self.view.mostrar_mensagem("Sucesso", f"Loja '{nome_loja}' removida!")
        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.view.limpar_tabela()

        lojas = self.model.buscar_todas()
        for l in lojas:
            id_loja, nome, cidade, endereco, intervalo, promotores, industrias = l
            
            # Formata a exibição do intervalo com a palavra 'dias'
            intervalo_str = f"{intervalo} dias"

            self.view.adicionar_linha(
                id_loja=id_loja,
                nome=nome,
                cidade=cidade,
                endereco=endereco or "—",
                intervalo=intervalo_str,
                promotores_str=promotores,
                industrias_str=industrias,
                cmd_editar=lambda i=id_loja, n=nome, c=cidade, e=endereco, interv=intervalo: self.preparar_edicao(i, n, c, e, interv),
                cmd_excluir=lambda i=id_loja, n=nome: self.excluir(i, n)
            )