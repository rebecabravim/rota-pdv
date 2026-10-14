import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('rotapdv.db')
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS industrias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')
    # Tabela de Promotores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                setor TEXT
            )
        ''')
        
        # Tabela de Relacionamento (N:N)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotor_industria (
                promotor_id INTEGER,
                industria_id INTEGER,
                FOREIGN KEY(promotor_id) REFERENCES promotores(id) ON DELETE CASCADE,
                FOREIGN KEY(industria_id) REFERENCES industrias(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()