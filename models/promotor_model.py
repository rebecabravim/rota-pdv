class PromotorModel:
    def __init__(self, db):
        self.db = db

    def salvar(self, nome, setor, industrias_ids):
        cursor = self.db.conn.cursor()
        cursor.execute("INSERT INTO promotores (nome, setor) VALUES (?, ?)", (nome, setor))
        promotor_id = cursor.lastrowid
        
        self._salvar_relacionamentos(cursor, promotor_id, industrias_ids)
        self.db.conn.commit()

    def atualizar(self, promotor_id, nome, setor, industrias_ids):
        cursor = self.db.conn.cursor()
        cursor.execute("UPDATE promotores SET nome = ?, setor = ? WHERE id = ?", (nome, setor, promotor_id))
        
        # Apaga os vínculos antigos e recria os novos
        cursor.execute("DELETE FROM promotor_industria WHERE promotor_id = ?", (promotor_id,))
        self._salvar_relacionamentos(cursor, promotor_id, industrias_ids)
        self.db.conn.commit()

    def _salvar_relacionamentos(self, cursor, promotor_id, industrias_ids):
        for ind_id in industrias_ids:
            cursor.execute("INSERT INTO promotor_industria (promotor_id, industria_id) VALUES (?, ?)", 
                           (promotor_id, ind_id))

    def buscar_todos(self):
        cursor = self.db.conn.cursor()
        # Busca promotores
        cursor.execute("SELECT id, nome, setor FROM promotores ORDER BY nome")
        promotores = cursor.fetchall()
        
        resultado = []
        for p in promotores:
            p_id, nome, setor = p
            # Busca as indústrias atreladas a este promotor
            cursor.execute('''
                SELECT i.id, i.nome 
                FROM industrias i
                INNER JOIN promotor_industria pi ON i.id = pi.industria_id
                WHERE pi.promotor_id = ?
            ''', (p_id,))
            inds = cursor.fetchall()
            resultado.append({"id": p_id, "nome": nome, "setor": setor, "industrias": inds})
            
        return resultado

    def deletar(self, promotor_id):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM promotores WHERE id = ?", (promotor_id,))
        cursor.execute("DELETE FROM promotor_industria WHERE promotor_id = ?", (promotor_id,))
        self.db.conn.commit()

    def nome_ja_existe(self, nome, id_ignorar=None):
        cursor = self.db.conn.cursor()
        if id_ignorar:
            cursor.execute("SELECT id FROM promotores WHERE LOWER(nome) = LOWER(?) AND id != ?", (nome, id_ignorar))
        else:
            cursor.execute("SELECT id FROM promotores WHERE LOWER(nome) = LOWER(?)", (nome,))
        
        return cursor.fetchone() is not None