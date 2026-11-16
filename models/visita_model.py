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
        """
        Retorna:
        - 'nao': se houve ruptura em alguma indústria na última visita
        - 'tem': se houve estoque e nenhuma ruptura na última visita
        - 'na' : se nunca foi visitada ou não há informação de estoque
        """
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