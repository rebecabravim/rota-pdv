class IndustriaModel:
    def __init__(self, db):
        self.db = db

    def salvar(self, nome):
        cursor = self.db.conn.cursor()
        cursor.execute("INSERT INTO industrias (nome) VALUES (?)", (nome,))
        self.db.conn.commit()

    def atualizar(self, ind_id, nome):
        cursor = self.db.conn.cursor()
        cursor.execute("UPDATE industrias SET nome = ? WHERE id = ?", (nome, ind_id))
        self.db.conn.commit()

    def buscar_todas(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nome FROM industrias ORDER BY nome")
        return cursor.fetchall()
    
    def deletar(self, ind_id):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM industrias WHERE id = ?", (ind_id,))
        self.db.conn.commit()