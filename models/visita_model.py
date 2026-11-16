class VisitaModel:
    def __init__(self, db):
        self.db = db

    def buscar_ultima_visita_loja(self, loja_id, data_ref_iso):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT id, data, status
            FROM visitas
            WHERE loja_id = ? AND data <= ?
            ORDER BY data DESC, criado_em DESC, id DESC
            LIMIT 1
        """, (loja_id, data_ref_iso))
        return cursor.fetchone()

    def resumo_estoque_loja(self, loja_id, data_ref_iso):
            ultima = self.buscar_ultima_visita_loja(loja_id, data_ref_iso)
            if not ultima:
                return "na"
    
            visita_id = ultima[0]
            cursor = self.db.conn.cursor()
            cursor.execute(
                "SELECT estoque FROM visita_industrias WHERE visita_id = ?",
                (visita_id,)
            )
            estoques = [row[0] for row in cursor.fetchall()]
    
            if "nao" in estoques:
                return "nao"
            if "tem" in estoques:
                return "tem"
            return "na"

    def loja_ja_registrada_na_data(self, loja_id, promotor_id, data_iso):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT 1
            FROM visitas
            WHERE loja_id = ? AND promotor_id = ? AND data = ?
            LIMIT 1
        """, (loja_id, promotor_id, data_iso))
        return cursor.fetchone() is not None

    # --- Consultas de Domínio para Registro de Visita ---
    def buscar_roteiro_e_lojas_pendentes(self, promotor_id, data_iso):
        """
        Busca o roteiro do promotor na data e retorna (roteiro_id, lojas_pendentes).
        Se não houver roteiro cadastrado na data, retorna (None, []).
        """
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT id FROM roteiros WHERE promotor_id = ? AND data = ?",
            (promotor_id, data_iso)
        )
        row = cursor.fetchone()
        if not row:
            return None, []

        roteiro_id = row[0]

        cursor.execute("""
            SELECT l.id, l.nome, l.cidade
            FROM roteiro_lojas rl
            INNER JOIN lojas l ON l.id = rl.loja_id
            WHERE rl.roteiro_id = ?
                AND l.id NOT IN (
                    SELECT v.loja_id
                    FROM visitas v
                    WHERE v.roteiro_id = ?
                )
            ORDER BY l.nome ASC
        """, (roteiro_id, roteiro_id))

        return roteiro_id, cursor.fetchall()

    def buscar_industrias_auditaveis(self, loja_id, promotor_id):
        """Retorna apenas as indústrias atendidas pela loja E representadas pelo promotor."""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT i.id, i.nome
            FROM industrias i
            INNER JOIN loja_industria li ON i.id = li.industria_id
            INNER JOIN promotor_industria pi ON i.id = pi.industria_id
            WHERE li.loja_id = ? AND pi.promotor_id = ?
            ORDER BY i.nome ASC
        """, (loja_id, promotor_id))
        return cursor.fetchall()

    # --- CRUD de Visitas ---
    def salvar(self, roteiro_id, promotor_id, loja_id, data_iso, status, obs_geral, itens_industrias):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            INSERT INTO visitas (roteiro_id, promotor_id, loja_id, data, status, obs_geral)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roteiro_id, promotor_id, loja_id, data_iso, status, obs_geral))

        visita_id = cursor.lastrowid
        if status == "feita":
            self._salvar_itens(cursor, visita_id, itens_industrias)

        self.db.conn.commit()
        return visita_id

    def atualizar(self, visita_id, status, obs_geral, itens_industrias):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            UPDATE visitas
            SET status = ?, obs_geral = ?
            WHERE id = ?
        """, (status, obs_geral, visita_id))

        cursor.execute("DELETE FROM visita_industrias WHERE visita_id = ?", (visita_id,))
        if status == "feita":
            self._salvar_itens(cursor, visita_id, itens_industrias)

        self.db.conn.commit()

    @staticmethod
    def _salvar_itens(cursor, visita_id, itens_industrias):
        for item in itens_industrias:
            cursor.execute("""
                INSERT INTO visita_industrias (visita_id, industria_id, estoque, obs)
                VALUES (?, ?, ?, ?)
            """, (visita_id, item["industria_id"], item["estoque"], item["obs"]))

    def deletar(self, visita_id):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM visita_industrias WHERE visita_id = ?", (visita_id,))
        cursor.execute("DELETE FROM visitas WHERE id = ?", (visita_id,))
        self.db.conn.commit()

    def buscar_por_id(self, visita_id):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT
                v.id,
                v.roteiro_id,
                v.promotor_id,
                p.nome AS promotor_nome,
                v.loja_id,
                l.nome AS loja_nome,
                l.cidade AS loja_cidade,
                v.data,
                v.status,
                v.obs_geral
            FROM visitas v
            INNER JOIN promotores p ON v.promotor_id = p.id
            INNER JOIN lojas l ON v.loja_id = l.id
            WHERE v.id = ?
        """, (visita_id,))
        return cursor.fetchone()

    def buscar_itens_visita(self, visita_id):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT vi.industria_id, i.nome, vi.estoque, vi.obs
            FROM visita_industrias vi
            INNER JOIN industrias i ON vi.industria_id = i.id
            WHERE vi.visita_id = ?
            ORDER BY i.nome ASC
        """, (visita_id,))
        return cursor.fetchall()

    def buscar_todas(self, promotor_id=None, data_iso=None):
        cursor = self.db.conn.cursor()
        query = """
            SELECT
                v.id,
                p.nome AS promotor_nome,
                v.data,
                l.nome AS loja_nome,
                l.cidade AS loja_cidade,
                v.status,
                v.obs_geral,
                COALESCE(
                    GROUP_CONCAT(
                        i.nome || ': ' ||
                        CASE vi.estoque
                            WHEN 'tem' THEN 'Com estoque'
                            WHEN 'nao' THEN 'Sem estoque'
                            ELSE 'N/A'
                        END,
                        ' | '
                    ),
                    '—'
                ) AS resumo_industrias
            FROM visitas v
            INNER JOIN promotores p ON v.promotor_id = p.id
            INNER JOIN lojas l ON v.loja_id = l.id
            LEFT JOIN visita_industrias vi ON v.id = vi.visita_id
            LEFT JOIN industrias i ON vi.industria_id = i.id
            WHERE 1 = 1
        """
        params = []
        if promotor_id:
            query += " AND v.promotor_id = ?"
            params.append(promotor_id)
        if data_iso:
            query += " AND v.data = ?"
            params.append(data_iso)

        query += """
            GROUP BY v.id, p.nome, v.data, l.nome, l.cidade, v.status, v.obs_geral
            ORDER BY v.data DESC, v.id DESC
        """
        cursor.execute(query, params)
        return cursor.fetchall()