"""
Service pour la génération de relations étape par étape
"""
import os
from datetime import datetime

class RelationGenerator:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'atarys_data.db')
    
    def get_all_tables(self):
        """Récupérer toutes les tables disponibles"""
        import sqlite3
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'alembic_version'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            print(f"Erreur récupération tables: {e}")
            return []
    
    def get_table_info(self, table_name):
        """Récupérer les informations d'une table"""
        import sqlite3
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            conn.close()
            
            # Déterminer le module basé sur le nom de la table
            module_id = self._determine_module_id(table_name)
            
            return {
                'name': table_name,
                'module_id': module_id,
                'columns': [{'name': col[1], 'type': col[2], 'notnull': col[3], 'pk': col[5]} for col in columns]
            }
        except Exception as e:
            print(f"Erreur récupération info table {table_name}: {e}")
            return None
    
    def _determine_module_id(self, table_name):
        """Déterminer le module ID basé sur le nom de la table"""
        # Logique simple pour déterminer le module
        # En production, cela pourrait être plus sophistiqué
        if 'chantier' in table_name:
            return 3
        elif 'client' in table_name:
            return 2
        elif 'article' in table_name:
            return 5
        elif 'salarie' in table_name:
            return 9
        else:
            return 12  # Module par défaut
    
    def generate_relation_code(self, source_table, target_table, relation_type='many-to-one', cascade='', lazy='select'):
        """Générer le code de relation étape par étape"""
        
        # Récupérer les informations des tables
        source_info = self.get_table_info(source_table)
        target_info = self.get_table_info(target_table)
        
        if not source_info or not target_info:
            return None
        
        # Générer les noms automatiquement
        names = self._generate_names(source_table, target_table)
        
        # Générer le code pour chaque étape
        return {
            'step_1_model_source': self._generate_model_source_code(source_info, target_info, names, relation_type, cascade, lazy),
            'step_2_model_target': self._generate_model_target_code(source_info, target_info, names, relation_type),
            'step_3_schema_source': self._generate_schema_source_code(source_info, target_info, names),
            'step_4_schema_target': self._generate_schema_target_code(source_info, target_info, names),
            'step_5_migration': self._generate_migration_code(source_info, target_info, names),
            'step_6_routes': self._generate_routes_code(source_info, target_info, names),
            'metadata': {
                'source_table': source_table,
                'target_table': target_table,
                'source_module': source_info['module_id'],
                'target_module': target_info['module_id'],
                'relation_type': relation_type,
                'names': names
            }
        }
    
    def _generate_names(self, source_table, target_table):
        """Générer les noms automatiquement"""
        source_class = ''.join(word.capitalize() for word in source_table.split('_'))
        target_class = ''.join(word.capitalize() for word in target_table.split('_'))
        
        foreign_key_name = f"{target_table}_id"
        relation_name = target_table
        backref_name = source_table
        
        return {
            'source_class': source_class,
            'target_class': target_class,
            'foreign_key_name': foreign_key_name,
            'relation_name': relation_name,
            'backref_name': backref_name
        }
    
    def _generate_model_source_code(self, source_info, target_info, names, relation_type, cascade, lazy):
        """Générer le code pour le modèle source"""
        cascade_code = f", cascade='{cascade}'" if cascade else ""
        
        foreign_key_code = f"    {names['foreign_key_name']} = db.Column(db.Integer, db.ForeignKey('{target_info['name']}.id'), nullable=False)"
        relationship_code = f"    {names['relation_name']} = db.relationship('{names['target_class']}', backref='{names['backref_name']}', lazy='{lazy}'{cascade_code})"
        
        return {
            'code': f"{foreign_key_code}\n{relationship_code}",
            'file': f"backend/app/models/module_{source_info['module_id']}.py",
            'insert_position': f"Dans la classe {names['source_class']}, après les autres colonnes, avant la méthode __repr__",
            'instructions': [
                f"1. Ouvrir le fichier : {self._get_file_path(f'backend/app/models/module_{source_info['module_id']}.py')}",
                f"2. Trouver la classe {names['source_class']}",
                f"3. Insérer le code après les autres colonnes, avant la méthode __repr__",
                f"4. Ajouter l'import si nécessaire : from app.models.module_{target_info['module_id']} import {names['target_class']}"
            ]
        }
    
    def _generate_model_target_code(self, source_info, target_info, names, relation_type):
        """Générer le code pour le modèle cible (si nécessaire)"""
        if relation_type in ['one-to-many', 'many-to-many']:
            return {
                'code': f"    # Relation bidirectionnelle automatiquement créée par le backref dans {names['source_class']}",
                'file': f"backend/app/models/module_{target_info['module_id']}.py",
                'insert_position': f"Dans la classe {names['target_class']}, le backref est automatiquement créé",
                'instructions': [
                    f"1. Aucun code à ajouter dans le modèle cible",
                    f"2. Le backref '{names['backref_name']}' est automatiquement créé par la relation dans {names['source_class']}",
                    f"3. Vous pouvez accéder aux {names['backref_name']} via : {names['target_class']}.{names['backref_name']}"
                ]
            }
        else:
            return {
                'code': "    # Aucun code nécessaire pour ce type de relation",
                'file': f"backend/app/models/module_{target_info['module_id']}.py",
                'insert_position': "Aucune insertion nécessaire",
                'instructions': [
                    "1. Aucun code à ajouter dans le modèle cible",
                    "2. La relation est unidirectionnelle"
                ]
            }
    
    def _generate_schema_source_code(self, source_info, target_info, names):
        """Générer le code pour le schéma source"""
        foreign_key_field = f"    {names['foreign_key_name']} = fields.Integer(required=True, validate=validate.Range(min=1))"
        relation_field = f"    {names['relation_name']} = fields.Nested('{names['target_class']}Schema', dump_only=True)"
        
        return {
            'code': f"{foreign_key_field}\n{relation_field}",
            'file': f"backend/app/schemas/module_{source_info['module_id']}.py",
            'insert_position': f"Dans la classe {names['source_class']}Schema, après les autres champs",
            'instructions': [
                f"1. Ouvrir le fichier : {self._get_file_path(f'backend/app/schemas/module_{source_info['module_id']}.py')}",
                f"2. Trouver la classe {names['source_class']}Schema",
                f"3. Insérer le code après les autres champs",
                f"4. Ajouter l'import si nécessaire : from app.schemas.module_{target_info['module_id']} import {names['target_class']}Schema"
            ]
        }
    
    def _generate_schema_target_code(self, source_info, target_info, names):
        """Générer le code pour le schéma cible"""
        backref_field = f"    {names['backref_name']} = fields.Nested('{names['source_class']}Schema', many=True, dump_only=True)"
        
        return {
            'code': backref_field,
            'file': f"backend/app/schemas/module_{target_info['module_id']}.py",
            'insert_position': f"Dans la classe {names['target_class']}Schema, après les autres champs",
            'instructions': [
                f"1. Ouvrir le fichier : {self._get_file_path(f'backend/app/schemas/module_{target_info['module_id']}.py')}",
                f"2. Trouver la classe {names['target_class']}Schema",
                f"3. Insérer le code après les autres champs",
                f"4. Ajouter l'import si nécessaire : from app.schemas.module_{source_info['module_id']} import {names['source_class']}Schema"
            ]
        }
    
    def _generate_migration_code(self, source_info, target_info, names):
        """Générer le code de migration"""
        migration_name = f"add_{names['foreign_key_name']}_to_{source_info['name']}"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        upgrade_code = f"""def upgrade():
    # Ajouter la colonne clé étrangère
    op.add_column('{source_info['name']}', sa.Column('{names['foreign_key_name']}', sa.Integer(), nullable=False))
    
    # Créer la contrainte de clé étrangère
    op.create_foreign_key(
        'fk_{source_info['name']}_{names['relation_name']}',
        '{source_info['name']}',
        '{target_info['name']}',
        ['{names['foreign_key_name']}'],
        ['id']
    )"""

        downgrade_code = f"""def downgrade():
    # Supprimer la contrainte de clé étrangère
    op.drop_constraint('fk_{source_info['name']}_{names['relation_name']}', '{source_info['name']}', type_='foreignkey')
    
    # Supprimer la colonne
    op.drop_column('{source_info['name']}', '{names['foreign_key_name']}')"""
        
        return {
            'code': f"{upgrade_code}\n\n{downgrade_code}",
            'migration_name': migration_name,
            'command': f"flask db migrate -m \"{migration_name}\"",
            'instructions': [
                "1. Exécuter la commande de migration :",
                f"   {migration_name}",
                "2. Vérifier le fichier de migration généré",
                "3. Appliquer la migration : flask db upgrade"
            ]
        }
    
    def _generate_routes_code(self, source_info, target_info, names):
        """Générer le code pour les routes API"""
        import_code = f"from app.models.module_{target_info['module_id']} import {names['target_class']}"
        
        return {
            'imports': [import_code],
            'file': f"backend/app/routes/module_{source_info['module_id']}.py",
            'insert_position': "En haut du fichier, avec les autres imports",
            'instructions': [
                f"1. Ouvrir le fichier : {self._get_file_path(f'backend/app/routes/module_{source_info['module_id']}.py')}",
                f"2. Ajouter l'import en haut du fichier : {import_code}",
                f"3. Les endpoints existants utiliseront automatiquement la relation"
            ]
        }
    
    def _get_file_path(self, relative_path):
        """Obtenir le chemin absolu d'un fichier"""
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), relative_path.replace('backend/', ''))

# Instance globale
relation_generator = RelationGenerator() 