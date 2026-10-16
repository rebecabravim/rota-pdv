import customtkinter as ctk
from PIL import Image
from views.tab_industria import TabIndustria
from views.tab_promotor import TabPromotor

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("RotaPDV - Gestão de Visitas")
        self.root.geometry("1000x700")

        ctk.set_appearance_mode("light")
        self.root.configure(fg_color="#f8f9fa")
        
        self.COR_AZUL_ESCURO = "#013f6f"
        self.COR_AZUL_MEDIO = "#2a6db8"

        # ==========================================
        # 1. NAVBAR (CABEÇALHO ESTILO WEB)
        # ==========================================
        self.navbar = ctk.CTkFrame(self.root, fg_color="white", height=60, corner_radius=0)
        self.navbar.pack(fill="x", side="top")
        self.navbar.pack_propagate(False) # Impede que a barra encolha

        # Logo e Título à esquerda
        try:
            # Tenta carregar a imagem da logo que enviou
            img_logo = Image.open("logo-listrada-3272b4.png")
            self.logo_ctk = ctk.CTkImage(light_image=img_logo, size=(50, 50))
            lbl_logo = ctk.CTkLabel(self.navbar, image=self.logo_ctk, text="")
            lbl_logo.pack(side="left", padx=(20, 10))
        except Exception:
            pass # Se não encontrar, segue sem quebrar o programa

        lbl_title = ctk.CTkLabel(
            self.navbar, text="RotaPDV", 
            font=ctk.CTkFont(size=18, weight="bold"), text_color=self.COR_AZUL_MEDIO
        )
        lbl_title.pack(side="left")

        # Menus de Navegação à direita
        frame_menus = ctk.CTkFrame(self.navbar, fg_color="transparent")
        frame_menus.pack(side="right", padx=20)

        # Botões do Menu (Sem fundo, parecem links HTML)
        self.btn_nav_ind = ctk.CTkButton(
            frame_menus, text="Indústrias", fg_color="transparent", hover_color="#f8f9fa",
            text_color=self.COR_AZUL_ESCURO, font=ctk.CTkFont(size=13, weight="normal"), width=80,
            command=lambda: self.selecionar_aba("Indústrias")
        )
        self.btn_nav_ind.pack(side="left", padx=10)

        self.btn_nav_prom = ctk.CTkButton(
            frame_menus, text="Promotores", fg_color="transparent", hover_color="#f8f9fa",
            text_color=self.COR_AZUL_ESCURO, font=ctk.CTkFont(size=13, weight="normal"), width=80,
            command=lambda: self.selecionar_aba("Promotores")
        )
        self.btn_nav_prom.pack(side="left", padx=10)

        # self.btn_nav_lojas = ctk.CTkButton(
        #     frame_menus, text="Lojas", fg_color="transparent", hover_color="#f8f9fa",
        #     text_color=self.COR_AZUL_ESCURO, font=ctk.CTkFont(size=13, weight="normal"), width=80,
        #     command=lambda: self.selecionar_aba("Lojas") # Descomente quando criar a TabLojas
        # )
        # self.btn_nav_lojas.pack(side="left", padx=10)


        # ==========================================
        # 2. ÁREA DE CONTEÚDO (Onde as abas aparecem)
        # ==========================================
        self.content_area = ctk.CTkFrame(self.root, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=5, pady=10)

        # Criamos os frames ocultos de cada tela
        self.frame_industrias = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frame_promotores = ctk.CTkFrame(self.content_area, fg_color="transparent")
        
        # Injetamos as views originais nestes frames
        self.tab_industrias = TabIndustria(self.frame_industrias)
        self.tab_promotores = TabPromotor(self.frame_promotores)

        # Inicia a aplicação exibindo a primeira aba
        self.selecionar_aba("Indústrias")

    def set_tab_command(self, command):
        """Permite que o AppController se ligue aos cliques do menu"""
        self.tab_command = command

    def selecionar_aba(self, nome_aba):
        # 1. Esconde todos os ecrãs
        self.frame_industrias.pack_forget()
        self.frame_promotores.pack_forget()

        # 2. Reseta a cor e fonte de todos os botões do menu
        fonte_normal = ctk.CTkFont(size=13, weight="normal")
        self.btn_nav_ind.configure(text_color=self.COR_AZUL_ESCURO, font=fonte_normal)
        self.btn_nav_prom.configure(text_color=self.COR_AZUL_ESCURO, font=fonte_normal)
        # self.btn_nav_lojas.configure(text_color=self.COR_AZUL_ESCURO, font=fonte_normal)

        # 3. Exibe a tela correta e pinta o botão de Azul Médio e Negrito
        fonte_negrito = ctk.CTkFont(size=13, weight="bold")
        
        if nome_aba == "Indústrias":
            self.frame_industrias.pack(fill="both", expand=True)
            self.btn_nav_ind.configure(text_color=self.COR_AZUL_MEDIO, font=fonte_negrito)
            
        elif nome_aba == "Promotores":
            self.frame_promotores.pack(fill="both", expand=True)
            self.btn_nav_prom.configure(text_color=self.COR_AZUL_MEDIO, font=fonte_negrito)

        # 4. Avisa o AppController (para recarregar banco de dados, se necessário)
        if hasattr(self, 'tab_command'):
            self.tab_command(nome_aba)