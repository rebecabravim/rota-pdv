from models.promotor_model import PromotorModel
from models.industria_model import IndustriaModel
import tkinter as tk

class PromotorController:
    def __init__(self, tab_view, db):
        self.view = tab_view
        self.model = PromotorModel(db)
        self.industria_model = IndustriaModel(db)
        
        self.id_em_edicao = None

        self.view.btn_salvar.configure(command=self.salvar)
        self.view.btn_cancelar.configure(command=self.cancelar_edicao)

        self.atualizar_tabela()
        self.carregar_checkboxes()

    def carregar_checkboxes(self, selecionadas=None):
        industrias = self.industria_model.buscar_todas()
        self.view.desenhar_checkboxes_industrias(industrias, selecionadas)

    def salvar(self):
        nome = self.view.entrada_nome.get().strip()
        setor = self.view.entrada_setor.get().strip()
        
        # Lê quais IDs de indústrias foram marcados
        inds_selecionadas = [ind_id for ind_id, var in self.view.check_vars.items() if var.get()]
        
        if not nome:
            self.view.mostrar_mensagem("Erro", "O nome do promotor é obrigatório.", "erro")
            return

        if self.model.nome_ja_existe(nome, self.id_em_edicao):
            self.view.mostrar_mensagem("Erro", f"Já existe um promotor com o nome '{nome}'.", "erro")
            return
        
        if self.id_em_edicao:
            self.model.atualizar(self.id_em_edicao, nome, setor, inds_selecionadas)
            self.view.mostrar_mensagem("Sucesso", f"Promotor atualizado!")
        else:
            self.model.salvar(nome, setor, inds_selecionadas)
            self.view.mostrar_mensagem("Sucesso", f"Promotor cadastrado!")

        self.cancelar_edicao()
        self.atualizar_tabela()

    def preparar_edicao(self, prom_id, nome, setor, industrias_obj):
        self.id_em_edicao = prom_id
        
        self.view.entrada_nome.delete(0, 'end')
        self.view.entrada_nome.insert(0, nome)
        
        self.view.entrada_setor.delete(0, 'end')
        self.view.entrada_setor.insert(0, setor)
        
        # Marca os checkboxes que esse promotor já possui
        ids_selecionados = [ind[0] for ind in industrias_obj]
        self.carregar_checkboxes(ids_selecionados)

        self.view.btn_salvar.configure(text="Salvar")
        self.view.btn_cancelar.pack(side=tk.LEFT)

    def cancelar_edicao(self):
        self.id_em_edicao = None
        self.view.entrada_nome.delete(0, 'end')
        self.view.entrada_setor.delete(0, 'end')
        self.carregar_checkboxes()
        
        self.view.btn_salvar.configure(text="Salvar")
        self.view.btn_cancelar.pack_forget()

    def excluir(self, prom_id, nome):
        if not tk.messagebox.askyesno("Confirmar", f"Deseja excluir o promotor '{nome}'?"):
            return

        self.model.deletar(prom_id)
        if self.id_em_edicao == prom_id:
            self.cancelar_edicao()
            
        self.view.mostrar_mensagem("Sucesso", f"Promotor removido!")
        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.view.limpar_tabela()
        promotores = self.model.buscar_todos()
        
        for p in promotores:
            nomes_inds = [ind[1] for ind in p['industrias']]
            inds_str = ", ".join(nomes_inds) if nomes_inds else "—"
            setor = p['setor'] if p['setor'] else "—"
            
            self.view.adicionar_linha(
                id_prom=p['id'],
                nome=p['nome'],
                setor=setor,
                inds_str=inds_str,
                cmd_editar=lambda idp=p['id'], n=p['nome'], s=p['setor'], inds=p['industrias']: self.preparar_edicao(idp, n, s, inds),
                cmd_excluir=lambda idp=p['id'], n=p['nome']: self.excluir(idp, n)
            )

    def recarregar_industrias(self):
        # 1. Guarda os IDs que já estavam selecionados na tela
        selecionadas = [ind_id for ind_id, var in self.view.check_vars.items() if var.get()]
        
        # 2. Redesenha os checkboxes trazendo as novidades do banco de dados
        self.carregar_checkboxes(selecionadas)