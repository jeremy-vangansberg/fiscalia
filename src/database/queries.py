"""
Documentation des requêtes SQL principales
"""

QUERIES = {
    "select_recent_data": """
        SELECT id, source, content, created_at
        FROM collected_data
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY)
        ORDER BY created_at DESC
        -- Cette requête est optimisée avec un index sur created_at
        -- Index: CREATE INDEX idx_created_at ON collected_data(created_at)
    """,
    
    "aggregate_by_source": """
        SELECT source, COUNT(*) as count, 
               MAX(created_at) as last_update
        FROM collected_data
        GROUP BY source
        HAVING count > 1
        -- Optimisée pour l'agrégation avec index composite
        -- Index: CREATE INDEX idx_source_created ON collected_data(source, created_at)
    """
}

class QueryBuilder:
    @staticmethod
    def build_select_query(table: str, conditions: dict) -> str:
        """
        Construit une requête SELECT dynamique et sécurisée
        """
        query = f"SELECT * FROM {table} WHERE "
        where_clauses = []
        for key, value in conditions.items():
            where_clauses.append(f"{key} = %s")
        query += " AND ".join(where_clauses)
        return query 