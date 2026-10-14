from controllers.industria_controller import IndustriaController
from controllers.promotor_controller import PromotorController

class AppController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        
        # Inicia o controle especifico da aba de Industrias
        self.industria_controller = IndustriaController(self.view.tab_industrias, self.db)
        self.promotor_controller = PromotorController(self.view.tab_promotores, self.db)

        # Associa o evento de troca de aba do Notebook
        self.view.notebook.bind("<<NotebookTabChanged>>", self.ao_trocar_aba)

    def ao_trocar_aba(self, event):
        # Descobre qual é a aba atual
        aba_selecionada = event.widget.select()
        texto_aba = event.widget.tab(aba_selecionada, "text")
        
        # Se o utilizador entrou na aba Promotores, atualiza as checkboxes de Indústrias
        if texto_aba == "Promotores":
            self.promotor_controller.recarregar_industrias()
            self.promotor_controller.atualizar_tabela()