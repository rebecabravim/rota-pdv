import sqlite3

class LojaModel:
    def __init__(self, db):
        self.db = db

    def nome_ja_existe(self, nome, cidade, id_ignorar=None):
        cursor = self.db.conn.cursor()
        if id_ignorar:
            cursor.execute("SELECT id FROM lojas WHERE LOWER(nome) = LOWER(?) AND LOWER(cidade) = LOWER(?) AND id != ?", (nome, cidade, id_ignorar))
        else:
            cursor.execute("SELECT id FROM lojas WHERE LOWER(nome) = LOWER(?) AND LOWER(cidade) = LOWER(?)", (nome, cidade))
        return cursor.fetchone() is not None

    def salvar(self, nome, cidade, endereco, intervalo_dias, promotores_ids, industrias_ids):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            INSERT INTO lojas (nome, cidade, endereco, intervalo_dias)
            VALUES (?, ?, ?, ?)
        """, (nome, cidade, endereco, intervalo_dias))
        
        loja_id = cursor.lastrowid
        self._salvar_vinculos(cursor, loja_id, promotores_ids, industrias_ids)
        self.db.conn.commit()
        return loja_id

    def atualizar(self, loja_id, nome, cidade, endereco, intervalo_dias, promotores_ids, industrias_ids):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            UPDATE lojas
            SET nome = ?, cidade = ?, endereco = ?, intervalo_dias = ?
            WHERE id = ?
        """, (nome, cidade, endereco, intervalo_dias, loja_id))
        
        # Remove vínculos antigos e reinsere os novos
        cursor.execute("DELETE FROM loja_promotor WHERE loja_id = ?", (loja_id,))
        cursor.execute("DELETE FROM loja_industria WHERE loja_id = ?", (loja_id,))
        
        self._salvar_vinculos(cursor, loja_id, promotores_ids, industrias_ids)
        self.db.conn.commit()

    def _salvar_vinculos(self, cursor, loja_id, promotores_ids, industrias_ids):
        for p_id in promotores_ids:
            cursor.execute("INSERT INTO loja_promotor (loja_id, promotor_id) VALUES (?, ?)", (loja_id, p_id))
        for i_id in industrias_ids:
            cursor.execute("INSERT INTO loja_industria (loja_id, industria_id) VALUES (?, ?)", (loja_id, i_id))

    def buscar_todas(self):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT 
                l.id, l.nome, l.cidade, l.endereco, l.intervalo_dias,
                COALESCE(GROUP_CONCAT(DISTINCT p.nome), '—') AS promotores,
                COALESCE(GROUP_CONCAT(DISTINCT i.nome), '—') AS industrias
            FROM lojas l
            LEFT JOIN loja_promotor lp ON l.id = lp.loja_id
            LEFT JOIN promotores p ON lp.promotor_id = p.id
            LEFT JOIN loja_industria li ON l.id = li.loja_id
            LEFT JOIN industrias i ON li.industria_id = i.id
            GROUP BY l.id
            ORDER BY l.nome ASC
        """)
        return cursor.fetchall()

    def buscar_promotores_vinculados(self, loja_id):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT promotor_id FROM loja_promotor WHERE loja_id = ?", (loja_id,))
        return [row[0] for row in cursor.fetchall()]

    def buscar_industrias_vinculadas(self, loja_id):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT industria_id FROM loja_industria WHERE loja_id = ?", (loja_id,))
        return [row[0] for row in cursor.fetchall()]

    def deletar(self, loja_id):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM loja_promotor WHERE loja_id = ?", (loja_id,))
        cursor.execute("DELETE FROM loja_industria WHERE loja_id = ?", (loja_id,))
        cursor.execute("DELETE FROM lojas WHERE id = ?", (loja_id,))
        self.db.conn.commit()