from controllers.industria_controller import IndustriaController

class AppController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        
        # Inicia o controle especifico da aba de Industrias
        self.industria_controller = IndustriaController(self.view.tab_industrias, self.db)