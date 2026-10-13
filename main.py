import tkinter as tk
from models.database import Database
from views.main_view import MainView
from controllers.app_controller import AppController

def main():
    db = Database()
    root = tk.Tk()
    view = MainView(root)
    app = AppController(view, db)
    root.mainloop()

if __name__ == "__main__":
    main()