#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - SERVICE DE SYNCHRONISATION BACKEND
Synchronise la structure SQLite avec le backend Flask

Auteur: ATARYS Team
Date: 2025
Version: 2.0 - Synchronisation automatique
"""

import os
import re
from sqlalchemy import text
from app import db
from app.services.table_generator import TableGeneratorService


class TableSyncService:
    """Service pour synchroniser la structure SQLite avec le backend"""
    
    def __init__(self):
        # Types SQLAlchemy supportés
        self.sqlalchemy_types = {
            'INTEGER': 'db.Integer',
            'TEXT': 'db.String',
            'REAL': 'db.Numeric(10, 2)',
            'BLOB': 'db.LargeBinary',
            'BOOLEAN': 'db.Boolean',
            'DATETIME': 'db.DateTime',
            'DATE': 'db.Date'
        }
        
        # Modules ATARYS
        self.modules_atarys = {
            1: "PLANNING",
            2: "LISTE_DES_TACHES", 
            3: "LISTE_CHANTIERS",
            4: "CHANTIERS",
            5: "DEVIS_FACTURATION",
            6: "ATELIER",
            7: "GESTION",
            8: "COMPTABILITE",
            9: "SOCIAL",
            10: "OUTILS",
            11: "ARCHIVES",
            12: "PARAMETRES",
            13: "AIDE"
        }
    
    def sync_all_tables(self):
        """
        Synchroniser toutes les tables SQLite avec le backend
        
        Returns:
            dict: Résultat de la synchronisation
        """
        try:
            # 1. Récupérer toutes les tables SQLite
            tables_in_db = set(self._get_all_tables())

            # 2. Lister toutes les tables connues dans le code backend (par parsing des fichiers models/routes/schemas)
            # On parse les fichiers module_X.py pour trouver toutes les classes de modèle générées
            models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
            all_backend_tables = set()
            for filename in os.listdir(models_dir):
                if filename.startswith('module_') and filename.endswith('.py'):
                    file_path = os.path.join(models_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Cherche toutes les classes de modèle générées
                        matches = re.findall(r'class ([A-Za-z0-9_]+)\(BaseModel\):', content)
                        for class_name in matches:
                            # Convertit en snake_case pour comparer avec SQLite
                            table_name = TableGeneratorService()._pascal_to_snake(class_name)
                            all_backend_tables.add(table_name)

            # 3. Pour chaque table qui n'existe plus dans la base, supprimer le code backend
            for table_name in all_backend_tables:
                if table_name not in tables_in_db:
                    print(f"[SYNC] Suppression du code backend pour la table disparue : {table_name}")
                    TableGeneratorService()._delete_generated_files_by_table_name(table_name)

            # 4. Synchroniser les tables existantes normalement
            results = []
            for table_name in tables_in_db:
                if not table_name.startswith('sqlite_'):
                    result = self._sync_table(table_name)
                    results.append(result)
            
            return {
                'success': True,
                'message': f'Synchronisation terminée : {len(results)} tables traitées',
                'data': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur synchronisation : {str(e)}'
            }
    
    def sync_single_table(self, table_name):
        """
        Synchroniser une table spécifique
        
        Args:
            table_name (str): Nom de la table à synchroniser
        
        Returns:
            dict: Résultat de la synchronisation
        """
        try:
            result = self._sync_table(table_name)
            return {
                'success': True,
                'message': f'Table {table_name} synchronisée',
                'data': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur synchronisation {table_name} : {str(e)}'
            }
    
    def _get_all_tables(self):
        """Récupérer toutes les tables SQLite"""
        result = db.session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        )
        return [row[0] for row in result.fetchall()]
    
    def _sync_table(self, table_name):
        """
        Synchroniser une table spécifique
        
        Args:
            table_name (str): Nom de la table
        
        Returns:
            dict: Informations de synchronisation
        """
        # 1. Analyser la structure de la table
        columns = self._get_table_structure(table_name)
        
        # 2. Déterminer le module
        module_id = self._determine_module(table_name)
        
        # 3. Générer le code backend
        model_code = self._generate_model_code(table_name, columns, module_id)
        route_code = self._generate_route_code(table_name, columns, module_id)
        schema_code = self._generate_schema_code(table_name, columns)
        
        # 4. Écrire les fichiers
        self._write_model_file(module_id, table_name, model_code)
        self._write_route_file(module_id, table_name, route_code)
        self._write_schema_file(module_id, table_name, schema_code)
        
        return {
            'table_name': table_name,
            'module_id': module_id,
            'columns_count': len(columns),
            'columns': columns
        }
    
    def _get_table_structure(self, table_name):
        """Récupérer la structure d'une table"""
        result = db.session.execute(
            text(f"PRAGMA table_info({table_name})")
        )
        
        columns = []
        for row in result.fetchall():
            column = {
                'name': row[1],
                'type': row[2],
                'not_null': bool(row[3]),
                'default': row[4],
                'primary_key': bool(row[5])
            }
            columns.append(column)
        
        return columns
    
    def _determine_module(self, table_name):
        """Déterminer le module d'une table"""
        # Logique de détermination du module
        # Par défaut : module 12 (PARAMETRES)
        return 12
    
    def _generate_model_code(self, table_name, columns, module_id):
        """Générer le code du modèle SQLAlchemy"""
        class_name = self._snake_to_pascal(table_name)
        
        model_code = f"""
class {class_name}(BaseModel):
    __tablename__ = '{table_name}'
    
"""
        
        for col in columns:
            if col['name'] in ['id', 'created_at', 'updated_at']:
                continue
                
            sqlalchemy_type = self._get_sqlalchemy_type(col['type'])
            params = []
            
            if not col['not_null']:
                params.append('nullable=True')
            else:
                params.append('nullable=False')
            
            if col['primary_key']:
                params.append('primary_key=True')
            
            if col['default'] is not None:
                params.append(f"default='{col['default']}'")
            
            params_str = ', '.join(params)
            model_code += f"    {col['name']} = {sqlalchemy_type}({params_str})\n"
        
        model_code += f"""
    def __repr__(self):
        return f'<{class_name} {{self.id}}>'
"""
        return model_code
    
    def _generate_route_code(self, table_name, columns, module_id):
        """Générer le code des routes API"""
        class_name = self._snake_to_pascal(table_name)
        main_module = str(module_id).split('_')[0]
        
        route_code = f"""
# Schéma et routes CRUD pour {class_name}
class {class_name}Schema(Schema):
"""
        
        for col in columns:
            if col['name'] in ['id', 'created_at', 'updated_at']:
                continue
            route_code += f"    {col['name']} = fields.String()\n"
        
        route_code += f"""
{table_name}_schema = {class_name}Schema()
{table_name}_schemas = {class_name}Schema(many=True)

@module_{main_module}_bp.route('/api/{table_name}/', methods=['GET'])
def list_{table_name}():
    try:
        items = {class_name}.query.all()
        return jsonify({{
            'success': True,
            'data': {table_name}_schemas.dump(items),
            'message': f'{{len(items)}} {table_name} trouvés'
        }})
    except Exception as e:
        return jsonify({{'success': False, 'message': str(e)}}), 400

@module_{main_module}_bp.route('/api/{table_name}/', methods=['POST'])
def create_{table_name}():
    try:
        data = request.get_json()
        errors = {table_name}_schema.validate(data)
        if errors:
            return jsonify({{'success': False, 'message': errors}}), 400
        new_item = {class_name}(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({{
            'success': True,
            'data': {table_name}_schema.dump(new_item),
            'message': '{class_name} créé avec succès'
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({{'success': False, 'message': str(e)}}), 400
"""
        return route_code
    
    def _generate_schema_code(self, table_name, columns):
        """Générer le code du schéma Marshmallow"""
        class_name = self._snake_to_pascal(table_name)
        
        schema_code = f"""
class {class_name}Schema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
"""
        
        for col in columns:
            if col['name'] in ['id', 'created_at', 'updated_at']:
                continue
            schema_code += f"    {col['name']} = fields.String()\n"
        
        return schema_code
    
    def _get_sqlalchemy_type(self, sqlite_type):
        """Convertir type SQLite vers SQLAlchemy"""
        return self.sqlalchemy_types.get(sqlite_type.upper(), 'db.String')
    
    def _write_model_file(self, module_id, table_name, model_code):
        """Écrire le modèle dans le fichier du module"""
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        main_module = str(module_id).split('_')[0]
        module_file = os.path.join(models_dir, f'module_{main_module}.py')
        
        # Ajouter le code à la fin du fichier
        with open(module_file, 'a', encoding='utf-8') as f:
            f.write('\n\n')
            f.write(model_code)
        
        print(f"✅ Modèle synchronisé dans {module_file}")
    
    def _clean_table_code_from_file(self, file_path, class_name):
        """Supprime le code existant lié à une table (modèle, routes, schéma) dans le fichier cible."""
        if not os.path.exists(file_path):
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Regex pour supprimer la classe, le schéma et les routes CRUD de la table
        # On supprime tout bloc commençant par 'class {class_name}' jusqu'à la prochaine classe ou fin de fichier
        pattern = re.compile(rf'(\n# Schéma et routes CRUD pour {class_name}.*?)(?=\n# Schéma et routes CRUD pour |\Z)', re.DOTALL)
        content_cleaned = re.sub(pattern, '\n', content)
        # On supprime aussi la définition du schéma Marshmallow si présent
        pattern_schema = re.compile(rf'(\nclass {class_name}Schema\(Schema\):.*?)(?=\nclass |\Z)', re.DOTALL)
        content_cleaned = re.sub(pattern_schema, '\n', content_cleaned)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_cleaned)
    
    def _write_route_file(self, module_id, table_name, route_code):
        """Écrire les routes dans le fichier du module"""
        routes_dir = os.path.join(os.path.dirname(__file__), '..', 'routes')
        main_module = str(module_id).split('_')[0]
        route_file = os.path.join(routes_dir, f'module_{main_module}.py')
        class_name = self._snake_to_pascal(table_name)
        # Nettoyer le code existant lié à la table
        self._clean_table_code_from_file(route_file, class_name)
        # Ajouter le code à la fin du fichier
        with open(route_file, 'a', encoding='utf-8') as f:
            f.write('\n')
            f.write(route_code)
        print(f"✅ Routes synchronisées dans {route_file}")
    
    def _write_schema_file(self, module_id, table_name, schema_code):
        """Écrire le schéma dans le fichier du module"""
        schemas_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')
        main_module = str(module_id).split('_')[0]
        schema_file = os.path.join(schemas_dir, f'module_{main_module}.py')
        
        # Ajouter le code à la fin du fichier
        with open(schema_file, 'a', encoding='utf-8') as f:
            f.write('\n')
            f.write(schema_code)
        
        print(f"✅ Schéma synchronisé dans {schema_file}")
    
    def _snake_to_pascal(self, snake_case):
        """Convertir snake_case en PascalCase"""
        return ''.join(word.capitalize() for word in snake_case.split('_'))


# Instance globale du service
table_sync = TableSyncService() 