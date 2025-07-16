"""
Service pour la synchronisation des tables SQLite avec le backend
"""
import sqlite3
import os
from typing import List, Dict, Any


class TableSyncService:
    """Service pour gérer la synchronisation des tables SQLite"""
    
    def __init__(self):
        """Initialiser le service avec le chemin de la base de données"""
        # Chemin vers la base de données depuis le répertoire backend
        self.db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            '..', 'data', 'atarys_data.db'
        )
    
    def _get_all_tables(self) -> List[str]:
        """Récupérer toutes les tables de la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            print(f"Erreur lors de la récupération des tables: {e}")
            return []
    
    def _get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Récupérer les colonnes d'une table spécifique"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    'name': row[1],
                    'type': row[2],
                    'not_null': bool(row[3]),
                    'default_value': row[4],
                    'primary_key': bool(row[5])
                })
            conn.close()
            return columns
        except Exception as e:
            print(f"Erreur lors de la récupération des colonnes: {e}")
            return []
    
    def generate_relation_code(self, source_table: str, source_column: str,
                             target_table: str, target_column: str,
                             relation_name: str) -> str:
        """Générer le code Python pour une relation SQLAlchemy"""
        
        # Convertir les noms de tables en noms de classes Python
        source_class = self._table_to_class_name(source_table)
        target_class = self._table_to_class_name(target_table)
        
        # Générer le code de relation
        relation_code = f"""
# Relation {relation_name} dans {source_class}
{relation_name} = db.relationship(
    '{target_class}',
    foreign_keys=[{source_column}],
    backref=db.backref('{source_table}_list', lazy='dynamic')
)
"""
        return relation_code.strip()
    
    def validate_foreign_key(self, source_table: str, source_column: str,
                           target_table: str, target_column: str) -> bool:
        """Valider si une clé étrangère est possible"""
        try:
            # Vérifier que les tables existent
            tables = self._get_all_tables()
            if source_table not in tables or target_table not in tables:
                return False
            
            # Vérifier que les colonnes existent
            source_columns = [col['name'] for col in self._get_table_columns(source_table)]
            target_columns = [col['name'] for col in self._get_table_columns(target_table)]
            
            if source_column not in source_columns or target_column not in target_columns:
                return False
            
            # Vérifier que la colonne cible est une clé primaire ou unique
            target_cols = self._get_table_columns(target_table)
            target_col = next((col for col in target_cols if col['name'] == target_column), None)
            
            if not target_col:
                return False
            
            # La colonne cible doit être une clé primaire ou avoir un index unique
            return target_col['primary_key'] or self._has_unique_index(target_table, target_column)
            
        except Exception as e:
            print(f"Erreur lors de la validation de la clé étrangère: {e}")
            return False
    
    def _table_to_class_name(self, table_name: str) -> str:
        """Convertir un nom de table en nom de classe Python"""
        # Convertir snake_case en PascalCase
        words = table_name.split('_')
        return ''.join(word.capitalize() for word in words)
    
    def _has_unique_index(self, table_name: str, column_name: str) -> bool:
        """Vérifier si une colonne a un index unique"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA index_list({table_name})")
            indexes = cursor.fetchall()
            
            for index in indexes:
                index_name = index[1]
                cursor.execute(f"PRAGMA index_info({index_name})")
                index_info = cursor.fetchall()
                
                # Vérifier si l'index contient notre colonne et est unique
                if any(row[2] == column_name for row in index_info) and index[2] == 1:
                    conn.close()
                    return True
            
            conn.close()
            return False
        except Exception as e:
            print(f"Erreur lors de la vérification de l'index unique: {e}")
            return False


# Instance globale du service
table_sync = TableSyncService() 