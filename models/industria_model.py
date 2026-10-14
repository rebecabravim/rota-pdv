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

    def nome_ja_existe(self, nome, id_ignorar=None):
        cursor = self.db.conn.cursor()
        # Usamos LOWER() para ignorar diferenças de maiusculas/minusculas
        if id_ignorar:
            # Se esta editando, ignora o proprio ID
            cursor.execute("SELECT id FROM industrias WHERE LOWER(nome) = LOWER(?) AND id != ?", (nome, id_ignorar))
        else:
            # Se for cadastro novo, busca em toda a tabela
            cursor.execute("SELECT id FROM industrias WHERE LOWER(nome) = LOWER(?)", (nome,))
        
        return cursor.fetchone() is not None

    def tem_vinculos_promotores(self, ind_id):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT 1 FROM promotor_industria WHERE industria_id = ?", (ind_id,))
        return cursor.fetchone() is not None