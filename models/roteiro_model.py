from datetime import datetime
from models.visita_model import VisitaModel


class RoteiroModel:
    def __init__(self, db):
        self.db = db
        self.visita_model = VisitaModel(db)

    def existe_roteiro_na_data(self, promotor_id, data_iso):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT id FROM roteiros WHERE promotor_id = ? AND data = ?",
            (promotor_id, data_iso)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def salvar(self, promotor_id, data_iso, lojas_ids):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "INSERT INTO roteiros (promotor_id, data) VALUES (?, ?)",
            (promotor_id, data_iso)
        )
        roteiro_id = cursor.lastrowid
        self._salvar_lojas(cursor, roteiro_id, lojas_ids)
        self.db.conn.commit()
        return roteiro_id

    def atualizar(self, roteiro_id, lojas_ids):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM roteiro_lojas WHERE roteiro_id = ?", (roteiro_id,))
        self._salvar_lojas(cursor, roteiro_id, lojas_ids)
        self.db.conn.commit()

    def _salvar_lojas(self, cursor, roteiro_id, lojas_ids):
        for loja_id in sorted(set(lojas_ids)):
            cursor.execute(
                "INSERT INTO roteiro_lojas (roteiro_id, loja_id) VALUES (?, ?)",
                (roteiro_id, loja_id)
            )

    def deletar(self, roteiro_id):
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM roteiro_lojas WHERE roteiro_id = ?", (roteiro_id,))
        cursor.execute("DELETE FROM roteiros WHERE id = ?", (roteiro_id,))
        self.db.conn.commit()

    def buscar_por_id(self, roteiro_id):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT r.id, r.promotor_id, p.nome, r.data
            FROM roteiros r
            INNER JOIN promotores p ON r.promotor_id = p.id
            WHERE r.id = ?
        """, (roteiro_id,))
        return cursor.fetchone()

    def buscar_lojas_vinculadas(self, roteiro_id):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT loja_id FROM roteiro_lojas WHERE roteiro_id = ?",
            (roteiro_id,)
        )
        return [row[0] for row in cursor.fetchall()]

    def buscar_todos(self, promotor_id=None, data_iso=None):
        cursor = self.db.conn.cursor()
        query = """
            SELECT
                r.id,
                r.promotor_id,
                p.nome AS promotor_nome,
                r.data,
                COUNT(DISTINCT rl.loja_id) AS total_lojas,
                COUNT(DISTINCT CASE WHEN v.status = 'feita' THEN v.loja_id END) AS feitas,
                COUNT(DISTINCT CASE WHEN v.status = 'nao_feita' THEN v.loja_id END) AS nao_feitas
            FROM roteiros r
            INNER JOIN promotores p ON r.promotor_id = p.id
            LEFT JOIN roteiro_lojas rl ON r.id = rl.roteiro_id
            LEFT JOIN visitas v ON r.id = v.roteiro_id AND rl.loja_id = v.loja_id
            WHERE 1 = 1
        """
        params = []
        if promotor_id:
            query += " AND r.promotor_id = ?"
            params.append(promotor_id)
        if data_iso:
            query += " AND r.data = ?"
            params.append(data_iso)

        query += """
            GROUP BY r.id, r.promotor_id, p.nome, r.data
            ORDER BY r.data DESC, p.nome ASC
        """
        cursor.execute(query, params)
        return cursor.fetchall()

    def buscar_lojas_valores_derivados_calculados(self, promotor_id, data_ref_iso):
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT l.id, l.nome, l.cidade, l.intervalo_dias
            FROM lojas l
            INNER JOIN loja_promotor lp ON l.id = lp.loja_id
            WHERE lp.promotor_id = ?
            ORDER BY l.nome ASC
        """, (promotor_id,))

        dt_ref = datetime.strptime(data_ref_iso, "%Y-%m-%d").date()
        lojas = []

        for row in cursor.fetchall():
            loja_id, nome, cidade, intervalo = row
            intervalo = intervalo or 7

            ultima_visita = self.visita_model.buscar_ultima_visita_loja(loja_id, data_ref_iso)
            if ultima_visita:
                dt_ultima = datetime.strptime(ultima_visita[1], "%Y-%m-%d").date()
                dias_sem_visita = max(0, (dt_ref - dt_ultima).days)
                critica = dias_sem_visita > intervalo
            else:
                dias_sem_visita = None
                critica = True

            resumo_estoque = self.visita_model.resumo_estoque_loja(loja_id, data_ref_iso)
            ja_registrada = self.visita_model.loja_ja_registrada_na_data(
                loja_id, promotor_id, data_ref_iso
            )

            lojas.append({
                "loja_id": loja_id,
                "nome": nome,
                "cidade": cidade or "",
                "intervalo_dias": intervalo,
                "dias_sem_visita": dias_sem_visita,
                "critica": critica,
                "resumo_estoque": resumo_estoque,
                "ja_registrada": ja_registrada,
            })

        # Ordena: não registradas primeiro, críticas no topo, maior tempo sem visita primeiro
        lojas.sort(
            key=lambda item: (
                item["ja_registrada"],
                not item["critica"],
                -(item["dias_sem_visita"] if item["dias_sem_visita"] is not None else 999999),
                item["nome"].lower(),
            )
        )
        return lojas