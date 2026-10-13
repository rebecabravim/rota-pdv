import tkinter as tk
from tkinter import ttk
from views.tab_industria import TabIndustria

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("RotaPDV - Gestão de Visitas")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Cria os frames para cada aba
        self.frame_dash = ttk.Frame(self.notebook)
        self.frame_industrias = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_dash, text="Dashboard")
        self.notebook.add(self.frame_industrias, text="Indústrias")

        # Injeta o frame limpo na classe que vai desenhar a aba de industrias
        self.tab_industrias = TabIndustria(self.frame_industrias)