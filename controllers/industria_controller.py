from models.industria_model import IndustriaModel
import tkinter as tk

class IndustriaController:
    def __init__(self, tab_view, db):
        self.view = tab_view
        self.model = IndustriaModel(db)
        
        self.id_em_edicao = None

        self.view.btn_salvar.config(command=self.salvar)
        self.view.btn_cancelar.config(command=self.cancelar_edicao)

        self.atualizar_tabela()

    def salvar(self):
        nome = self.view.entrada_nome.get().strip()
        
        if not nome:
            self.view.mostrar_mensagem("Erro", "O nome da indústria é obrigatório.", "erro")
            return
        
        if self.model.nome_ja_existe(nome, self.id_em_edicao):
            self.view.mostrar_mensagem("Erro", f"Já existe uma indústria com o nome '{nome}'.", "erro")
            return
        
        if self.id_em_edicao:
            self.model.atualizar(self.id_em_edicao, nome)
            self.view.mostrar_mensagem("Sucesso", f"Indústria atualizada para '{nome}'!")
        else:
            self.model.salvar(nome)
            self.view.mostrar_mensagem("Sucesso", f"Indústria '{nome}' cadastrada!")

        self.cancelar_edicao()
        self.atualizar_tabela()

    def preparar_edicao(self, ind_id, nome):
        self.id_em_edicao = ind_id
        
        self.view.entrada_nome.delete(0, 'end')
        self.view.entrada_nome.insert(0, nome)
        self.view.btn_salvar.config(text="Salvar Alteração")
        self.view.btn_cancelar.pack(side=tk.LEFT)

    def cancelar_edicao(self):
        self.id_em_edicao = None
        self.view.entrada_nome.delete(0, 'end')
        self.view.btn_salvar.config(text="Salvar")
        self.view.btn_cancelar.pack_forget()

    def excluir(self, ind_id, nome_ind):

        # Bloqueia exclusão se estiver em uso por promotores
        if self.model.tem_vinculos_promotores(ind_id):
            self.view.mostrar_mensagem(
                "Operação Bloqueada", 
                f"A indústria '{nome_ind}' não pode ser excluída porque possui promotores associados a ela.", 
                "erro"
            )
            return
        
        if not tk.messagebox.askyesno("Confirmar", f"Deseja excluir a indústria '{nome_ind}'?"):
            return

        self.model.deletar(ind_id)
        
        if self.id_em_edicao == ind_id:
            self.cancelar_edicao()
            
        self.view.mostrar_mensagem("Sucesso", f"Indústria '{nome_ind}' removida!")
        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.view.limpar_tabela()
            
        industrias = self.model.buscar_todas()
        for ind in industrias:
            ind_id = ind[0]
            nome = ind[1]
            
            # Passa lambdas para que o botão da linha saiba com quem interagir
            self.view.adicionar_industria(
                id_ind=ind_id,
                nome=nome,
                cmd_editar=lambda i=ind_id, n=nome: self.preparar_edicao(i, n),
                cmd_excluir=lambda i=ind_id, n=nome: self.excluir(i, n)
            )