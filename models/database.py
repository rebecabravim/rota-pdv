import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('rotapdv.db')
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()

        # Tabela de Indústrias
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
        
        # Tabela de Relacionamento N:N (Indústria x Promotor)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotor_industria (
                promotor_id INTEGER,
                industria_id INTEGER,
                FOREIGN KEY(promotor_id) REFERENCES promotores(id) ON DELETE CASCADE,
                FOREIGN KEY(industria_id) REFERENCES industrias(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de Lojas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lojas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cidade TEXT NOT NULL,
                endereco TEXT,
                intervalo_dias INTEGER DEFAULT 7
            )
        """)
        
        # Tabela de Relacionamento N:N (Loja x Promotor)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loja_promotor (
                loja_id INTEGER,
                promotor_id INTEGER,
                PRIMARY KEY (loja_id, promotor_id),
                FOREIGN KEY (loja_id) REFERENCES lojas (id) ON DELETE CASCADE,
                FOREIGN KEY (promotor_id) REFERENCES promotores (id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Relacionamento N:N (Loja x Indústria)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loja_industria (
                loja_id INTEGER,
                industria_id INTEGER,
                PRIMARY KEY (loja_id, industria_id),
                FOREIGN KEY (loja_id) REFERENCES lojas (id) ON DELETE CASCADE,
                FOREIGN KEY (industria_id) REFERENCES industrias (id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()