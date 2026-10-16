import customtkinter as ctk
import tkinter as tk

class WrappableLabel(tk.Label):
    def __init__(self, master=None, text="", fg_color="white", text_color="black", font=None, **kwargs):
        # A fonte do CustomTkinter precisa ser convertida para o Tkinter nativo entender
        fonte_padrao = ctk.CTkFont(size=12) if font is None else font
        tk_font = (fonte_padrao.cget("family"), fonte_padrao.cget("size"))
        
        # Inicializa a Label nativa do Tkinter (que ajusta a altura dinamicamente)
        super().__init__(
            master, 
            text=text, 
            fg=text_color, 
            bg=fg_color, 
            font=tk_font, 
            borderwidth=0, 
            highlightthickness=0, 
            **kwargs
        )
        # Escuta o redimensionamento apenas do seu frame "pai"
        self.master.bind("<Configure>", self._on_config, "+")

    def _on_config(self, event):
        # Quebra o texto respeitando estritamente a largura do frame em que está inserido
        wrappable = max(50, event.width - 10)
        self.configure(wraplength=wrappable)