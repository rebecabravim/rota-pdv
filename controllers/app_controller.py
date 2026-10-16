from controllers.industria_controller import IndustriaController
from controllers.promotor_controller import PromotorController

class AppController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        
        self.industria_controller = IndustriaController(self.view.tab_industrias, self.db)
        self.promotor_controller = PromotorController(self.view.tab_promotores, self.db)

        # A nossa nova Navbar possui um método para injetarmos o comando de troca
        self.view.set_tab_command(self.ao_trocar_aba)

    def ao_trocar_aba(self, texto_aba):
        if texto_aba == "Promotores":
            self.promotor_controller.recarregar_industrias()
            self.promotor_controller.atualizar_tabela()