from controllers.industria_controller import IndustriaController
from controllers.loja_controller import LojaController
from controllers.promotor_controller import PromotorController
from controllers.roteiro_controller import RoteiroController

class AppController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        
        self.industria_controller = IndustriaController(self.view.tab_industrias, self.db)
        self.promotor_controller = PromotorController(self.view.tab_promotores, self.db)
        self.loja_controller = LojaController(self.view.tab_lojas, self.db)
        self.roteiro_controller = RoteiroController(self.view.tab_roteiros, self.db)

        # A nossa nova Navbar possui um método para injetarmos o comando de troca
        self.view.set_tab_command(self.ao_trocar_aba)

    def ao_trocar_aba(self, texto_aba):
        if texto_aba == "Promotores":
            self.promotor_controller.recarregar_industrias()
            self.promotor_controller.atualizar_tabela()

        elif texto_aba == "Lojas":
            self.loja_controller.recarregar_opcoes_checks()
            self.loja_controller.atualizar_tabela()

        elif texto_aba == "Roteiros":
            self.roteiro_controller.recarregar_opcoes()
            self.roteiro_controller.atualizar_tabela()