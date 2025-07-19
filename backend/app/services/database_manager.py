#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - SERVICE UNIFIÉ DE GESTION DE BASE DE DONNÉES
Service centralisé pour toutes les opérations sur les tables et relations

Auteur: ATARYS Team
Date: 2025
Version: 2.0 - Architecture unifiée
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import text, inspect
from app import db


class DatabaseManager:
    """Service unifié pour la gestion des tables et relations SQLAlchemy"""
    
    def __init__(self):
        """Initialiser le service avec configuration centralisée"""
        # Configuration centralisée de la base de données
        self.db_path = self._get_centralized_db_path()
        self.sqlalchemy_uri = f"sqlite:///{self.db_path}"
        
        # Modules ATARYS selon nomenclature officielle
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
        
        # Types SQLAlchemy supportés
        self.sqlalchemy_types = {
            'Integer': 'db.Integer',
            'String': 'db.String',
            'Text': 'db.Text',
            'Numeric': 'db.Numeric(10, 2)',
            'REAL': 'db.Float',
            'Boolean': 'db.Boolean',
            'Date': 'db.Date',
            'DateTime': 'db.DateTime',
            'Time': 'db.Time',
            'Timestamp': 'db.Timestamp',
            'JSON': 'db.JSON',
            'LargeBinary': 'db.LargeBinary',
            'Enum': 'db.Enum'
        }
    
    def _get_centralized_db_path(self) -> str:
        """Obtenir le chemin centralisé vers la base de données"""
        # Chemin absolu depuis la racine du projet
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data', 'atarys_data.db'
        )
    
    # ============================================================================
    # MÉTHODES POUR LES TABLES
    # ============================================================================
    
    def list_tables(self) -> Dict[str, Any]:
        """Lister toutes les tables de la base de données"""
        try:
            # Utiliser SQLAlchemy pour lister les tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            # Filtrer les tables système
            user_tables = [t for t in tables if not t.startswith('sqlite_') and t != 'alembic_version']
            
            return {
                'success': True,
                'data': user_tables,
                'message': f'{len(user_tables)} tables utilisateur trouvées'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors du listing des tables : {str(e)}'
            }
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Récupérer les informations détaillées d'une table"""
        try:
            inspector = inspect(db.engine)
            
            # Vérifier que la table existe
            if table_name not in inspector.get_table_names():
                return {
                    'success': False,
                    'message': f'Table {table_name} n\'existe pas'
                }
            
            # Récupérer les colonnes
            columns = inspector.get_columns(table_name)
            column_info = []
            
            for col in columns:
                column_info.append({
                    'name': col['name'],
                    'type': str(col['type']),
                    'nullable': col['nullable'],
                    'default': col['default'],
                    'primary_key': col.get('primary_key', False)
                })
            
            # Déterminer le module basé sur le nom de la table
            module_id = self._determine_module_id(table_name)
            
            return {
                'success': True,
                'data': {
                    'name': table_name,
                    'module_id': module_id,
                    'columns': column_info,
                    'column_count': len(column_info)
                },
                'message': f'Informations de {table_name} récupérées'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des infos : {str(e)}'
            }
    
    def create_table(self, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """Créer une nouvelle table avec modèle et routes"""
        try:
            # Validation du schéma
            validation_result = self._validate_table_schema(table_data)
            if not validation_result['success']:
                return validation_result
            
            # Génération des fichiers backend
            model_code = self._generate_model_code(table_data)
            route_code = self._generate_route_code(table_data)
            schema_code = self._generate_schema_code(table_data)
            
            # Écriture des fichiers
            self._write_model_file(table_data['module_id'], table_data['table_name'], model_code)
            self._write_route_file(table_data['module_id'], table_data['table_name'], route_code)
            self._write_schema_file(table_data['module_id'], table_data['table_name'], schema_code)
            
            # Enregistrement des métadonnées
            self._save_table_definition(table_data)
            
            return {
                'success': True,
                'message': f"✅ Code généré pour '{table_data['table_name']}'. Lancez maintenant les migrations :",
                'data': {
                    'table_name': table_data['table_name'],
                    'class_name': table_data['class_name'],
                    'module_id': table_data['module_id'],
                    'columns_count': len(table_data['columns']),
                    'next_steps': [
                        f"flask db migrate -m 'Add table {table_data['table_name']}'",
                        "flask db upgrade"
                    ],
                    'warning': "⚠️ N'oubliez pas de lancer les migrations pour créer la table dans la base de données",
                    'files_created': [
                        f"backend/app/models/module_{table_data['module_id']}.py",
                        f"backend/app/routes/module_{table_data['module_id']}.py", 
                        f"backend/app/schemas/module_{table_data['module_id']}.py"
                    ]
                }
            }
        except Exception as e:
            # Rollback automatique des fichiers générés
            self._cleanup_on_error(table_data)
            return {
                'success': False,
                'message': f"❌ Erreur lors de la génération : {str(e)}"
            }
    
    def delete_table(self, table_name: str) -> Dict[str, Any]:
        """Supprimer une table complètement (base + fichiers générés)"""
        try:
            # Vérifier que la table existe
            inspector = inspect(db.engine)
            if table_name not in inspector.get_table_names():
                return {
                    'success': False,
                    'message': f'Table {table_name} n\'existe pas'
                }
            
            # Supprimer la table SQLite
            db.session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            db.session.commit()
            
            # Supprimer les fichiers générés
            self._delete_generated_files_by_table_name(table_name)
            
            return {
                'success': True,
                'message': f'Table {table_name} supprimée avec succès'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Erreur lors de la suppression : {str(e)}'
            }
    
    def bulk_insert(self, table_name: str, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Insérer des données en masse dans une table"""
        try:
            # Vérifier que la table existe
            inspector = inspect(db.engine)
            if table_name not in inspector.get_table_names():
                return {
                    'success': False,
                    'message': f"Table '{table_name}' n'existe pas"
                }
            
            # Récupérer la structure de la table
            columns = inspector.get_columns(table_name)
            column_names = [col['name'] for col in columns]
            
            # Valider et nettoyer les données
            cleaned_data = []
            for row in data_list:
                if not isinstance(row, dict):
                    continue
                
                # Filtrer les lignes vides
                if not any(str(value).strip() for value in row.values()):
                    continue
                
                # Nettoyer les données
                cleaned_row = {}
                for col_name, value in row.items():
                    if col_name in column_names:
                        # Convertir les types selon la colonne
                        cleaned_value = self._convert_value_type(value, columns[column_names.index(col_name)])
                        cleaned_row[col_name] = cleaned_value
                
                if cleaned_row:  # Ne pas ajouter de lignes vides
                    cleaned_data.append(cleaned_row)
            
            if not cleaned_data:
                return {
                    'success': False,
                    'message': "Aucune donnée valide à insérer"
                }
            
            # Insérer les données via SQLAlchemy
            inserted_count = 0
            for row in cleaned_data:
                try:
                    # Construire la requête SQL dynamique
                    columns_str = ', '.join(row.keys())
                    placeholders = ', '.join(['?' for _ in row])
                    values = list(row.values())
                    
                    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                    db.session.execute(text(query), values)
                    inserted_count += 1
                        
                except Exception as e:
                    # Continuer avec les autres lignes en cas d'erreur
                    print(f"Erreur insertion ligne {row}: {str(e)}")
                    continue
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f"{inserted_count} lignes insérées sur {len(cleaned_data)} données valides",
                'data': {
                    'inserted_count': inserted_count,
                    'total_processed': len(data_list),
                    'valid_data_count': len(cleaned_data)
                }
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f"Erreur lors de l'insertion en masse : {str(e)}"
            }
    
    # ============================================================================
    # MÉTHODES POUR LES RELATIONS
    # ============================================================================
    
    def list_relations(self) -> Dict[str, Any]:
        """Lister toutes les relations existantes"""
        try:
            # Pour l'instant, retourner une liste vide
            # Cette fonctionnalité sera implémentée plus tard
            return {
                'success': True,
                'data': [],
                'message': 'Aucune relation configurée'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors du listing des relations : {str(e)}'
            }
    
    def create_relation(self, relation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Créer une nouvelle relation entre tables"""
        try:
            source_table = relation_data.get('source_table')
            target_table = relation_data.get('target_table')
            relation_type = relation_data.get('relation_type', 'many-to-one')
            
            if not source_table or not target_table:
                return {
                    'success': False,
                    'message': 'Tables source et cible requises'
                }
            
            if source_table == target_table:
                return {
                    'success': False,
                    'message': 'Les tables source et cible doivent être différentes'
                }
            
            # Générer le code de relation
            relation_code = self.generate_relation_code(relation_data)
            
            return {
                'success': True,
                'data': relation_code,
                'message': 'Relation créée avec succès'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la création de la relation : {str(e)}'
            }
    
    def validate_foreign_key(self, source_table: str, source_column: str,
                           target_table: str, target_column: str) -> Dict[str, Any]:
        """Valider si une clé étrangère est possible"""
        try:
            inspector = inspect(db.engine)
            
            # Vérifier que les tables existent
            tables = inspector.get_table_names()
            if source_table not in tables or target_table not in tables:
                return {
                    'success': True,
                    'data': {'is_valid': False},
                    'message': 'Une ou les deux tables n\'existent pas'
                }
            
            # Vérifier que les colonnes existent
            source_columns = [col['name'] for col in inspector.get_columns(source_table)]
            target_columns = [col['name'] for col in inspector.get_columns(target_table)]
            
            if source_column not in source_columns or target_column not in target_columns:
                return {
                    'success': True,
                    'data': {'is_valid': False},
                    'message': 'Une ou les deux colonnes n\'existent pas'
                }
            
            # Vérifier que la colonne cible est une clé primaire ou unique
            target_cols = inspector.get_columns(target_table)
            target_col = next((col for col in target_cols if col['name'] == target_column), None)
            
            if not target_col:
                return {
                    'success': True,
                    'data': {'is_valid': False},
                    'message': 'Colonne cible introuvable'
                }
            
            # La colonne cible doit être une clé primaire ou avoir un index unique
            is_valid = target_col.get('primary_key', False) or self._has_unique_index(target_table, target_column)
            
            return {
                'success': True,
                'data': {'is_valid': is_valid},
                'message': 'Clé étrangère valide' if is_valid else 'Clé étrangère invalide'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la validation : {str(e)}'
            }
    
    # ============================================================================
    # MÉTHODES POUR LA GÉNÉRATION DE CODE
    # ============================================================================
    
    def generate_table_code(self, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """Générer le code pour une table"""
        try:
            model_code = self._generate_model_code(table_data)
            route_code = self._generate_route_code(table_data)
            schema_code = self._generate_schema_code(table_data)
            
            return {
                'success': True,
                'data': {
                    'model_code': model_code,
                    'route_code': route_code,
                    'schema_code': schema_code,
                    'instructions': [
                        f"1. Ajouter le modèle dans backend/app/models/module_{table_data['module_id']}.py",
                        f"2. Ajouter les routes dans backend/app/routes/module_{table_data['module_id']}.py",
                        f"3. Ajouter le schéma dans backend/app/schemas/module_{table_data['module_id']}.py",
                        "4. Lancer les migrations : flask db migrate && flask db upgrade"
                    ]
                },
                'message': 'Code généré avec succès'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération : {str(e)}'
            }
    
    def generate_relation_code(self, relation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Générer le code pour une relation"""
        try:
            source_table = relation_data.get('source_table')
            target_table = relation_data.get('target_table')
            relation_type = relation_data.get('relation_type', 'many-to-one')
            
            # Récupérer les informations des tables
            source_info = self.get_table_info(source_table)
            target_info = self.get_table_info(target_table)
            
            if not source_info['success'] or not target_info['success']:
                return {
                    'success': False,
                    'message': 'Impossible de récupérer les informations des tables'
                }
            
            # Générer les noms automatiquement
            names = self._generate_relation_names(source_table, target_table)
            
            # Générer le code pour chaque étape
            relation_code = {
                'step_1_model_source': self._generate_relation_model_source(source_info['data'], target_info['data'], names, relation_type),
                'step_2_model_target': self._generate_relation_model_target(source_info['data'], target_info['data'], names, relation_type),
                'step_3_schema_source': self._generate_relation_schema_source(source_info['data'], target_info['data'], names),
                'step_4_schema_target': self._generate_relation_schema_target(source_info['data'], target_info['data'], names),
                'step_5_migration': self._generate_relation_migration(source_info['data'], target_info['data'], names),
                'metadata': {
                    'source_table': source_table,
                    'target_table': target_table,
                    'source_module': source_info['data']['module_id'],
                    'target_module': target_info['data']['module_id'],
                    'relation_type': relation_type,
                    'names': names
                }
            }
            
            return {
                'success': True,
                'data': relation_code,
                'message': 'Code de relation généré avec succès'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération : {str(e)}'
            }
    
    # ============================================================================
    # MÉTHODES UTILITAIRES
    # ============================================================================
    
    def _determine_module_id(self, table_name: str) -> int:
        """Déterminer le module ID basé sur le nom de la table"""
        # Logique simple pour déterminer le module
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
    
    def _validate_table_schema(self, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valider le schéma de données pour une table"""
        required_fields = ['table_name', 'class_name', 'module_id', 'columns']
        for field in required_fields:
            if field not in table_data:
                return {
                    'success': False,
                    'message': f'Champ requis manquant : {field}'
                }
        
        if not table_data['columns'] or not isinstance(table_data['columns'], list):
            return {
                'success': False,
                'message': 'Au moins une colonne est requise'
            }
        
        return {'success': True}
    
    def _generate_model_code(self, table_data: Dict[str, Any]) -> str:
        """Générer le code du modèle SQLAlchemy"""
        class_name = table_data['class_name']
        table_name = table_data['table_name']
        options = table_data.get('options', {})
        
        imports = [
            "from app.models.base import BaseModel",
            "from app import db",
            "from datetime import datetime"
        ]
        
        class_def = f"""
class {class_name}(BaseModel):
    __tablename__ = '{table_name}'
"""
        
        columns_code = []
        column_names = [col['name'] for col in table_data['columns']]
        
        if options.get('id', True) and 'id' not in column_names:
            columns_code.append("    id = db.Column(db.Integer, primary_key=True, autoincrement=True)")
        
        for col in table_data['columns']:
            if col['name'] in ['id', 'created_at', 'updated_at']:
                continue
            
            col_type = self.sqlalchemy_types.get(col['type'], 'db.String')
            nullable = "nullable=False" if col.get('not_null', True) else "nullable=True"
            
            if col.get('primary_key', False):
                columns_code.append(f"    {col['name']} = db.Column({col_type}, primary_key=True)")
            else:
                columns_code.append(f"    {col['name']} = db.Column({col_type}, {nullable})")
        
        if options.get('created_at', True) and 'created_at' not in column_names:
            columns_code.append("    created_at = db.Column(db.DateTime, default=datetime.utcnow)")
        
        if options.get('updated_at', True) and 'updated_at' not in column_names:
            columns_code.append("    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)")
        
        # Méthode __repr__
        repr_code = f"""
    def __repr__(self):
        return f"<{class_name} {{self.id}}>"
"""
        
        return '\n'.join(imports) + class_def + '\n'.join(columns_code) + repr_code
    
    def _generate_route_code(self, table_data: Dict[str, Any]) -> str:
        """Générer le code des routes API"""
        class_name = table_data['class_name']
        table_name = table_data['table_name']
        main_module = str(table_data['module_id']).split('_')[0]
        
        route_code = (
            f"\n# Routes CRUD pour {class_name}\n"
            f"from app.schemas.module_{main_module} import {class_name}Schema\n"
            f"{table_name}_schema = {class_name}Schema()\n"
            f"{table_name}_schemas = {class_name}Schema(many=True)\n\n"
        )
        
        # GET
        route_code += (
            f"@module_{main_module}_bp.route('/api/{table_name}/', methods=['GET'])\n"
            f"def list_{table_name}():\n"
            f"    try:\n"
            f"        items = {class_name}.query.all()\n"
            f"        return jsonify({{\n"
            f"            'success': True,\n"
            f"            'data': {table_name}_schemas.dump(items),\n"
            f"            'message': f'{{len(items)}} {table_name} trouvés'\n"
            f"        }})\n"
            f"    except Exception as e:\n"
            f"        return jsonify({{'success': False, 'message': str(e)}}), 400\n\n"
        )
        
        # POST
        route_code += (
            f"@module_{main_module}_bp.route('/api/{table_name}/', methods=['POST'])\n"
            f"def create_{table_name}():\n"
            f"    try:\n"
            f"        data = request.get_json()\n"
            f"        errors = {table_name}_schema.validate(data)\n"
            f"        if errors:\n"
            f"            return jsonify({{'success': False, 'message': errors}}), 400\n"
            f"        new_item = {class_name}(**data)\n"
            f"        db.session.add(new_item)\n"
            f"        db.session.commit()\n"
            f"        return jsonify({{\n"
            f"            'success': True,\n"
            f"            'data': {table_name}_schema.dump(new_item),\n"
            f"            'message': '{class_name} créé avec succès'\n"
            f"        }})\n"
            f"    except Exception as e:\n"
            f"        db.session.rollback()\n"
            f"        return jsonify({{'success': False, 'message': str(e)}}), 400\n\n"
        )
        
        return route_code
    
    def _generate_schema_code(self, table_data: Dict[str, Any]) -> str:
        """Générer le code du schéma Marshmallow"""
        class_name = table_data['class_name']
        
        schema_code = f"""
from marshmallow import Schema, fields

class {class_name}Schema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
"""
        
        for col in table_data['columns']:
            if col['name'] in ['id', 'created_at', 'updated_at']:
                continue
            
            if col['type'] == 'Integer':
                schema_code += f"    {col['name']} = fields.Integer()\n"
            elif col['type'] == 'String':
                schema_code += f"    {col['name']} = fields.String()\n"
            elif col['type'] == 'Text':
                schema_code += f"    {col['name']} = fields.String()\n"
            elif col['type'] == 'Numeric':
                schema_code += f"    {col['name']} = fields.Decimal()\n"
            elif col['type'] == 'Boolean':
                schema_code += f"    {col['name']} = fields.Boolean()\n"
            elif col['type'] == 'Date':
                schema_code += f"    {col['name']} = fields.Date()\n"
            elif col['type'] == 'DateTime':
                schema_code += f"    {col['name']} = fields.DateTime()\n"
            else:
                schema_code += f"    {col['name']} = fields.String()\n"
        
        return schema_code
    
    def _write_model_file(self, module_id: str, table_name: str, model_code: str) -> bool:
        """Écrire le code du modèle dans le fichier du module"""
        try:
            models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
            os.makedirs(models_dir, exist_ok=True)
            
            main_module = str(module_id).split('_')[0]
            model_file = os.path.join(models_dir, f'module_{main_module}.py')
            
            if not os.path.exists(model_file):
                with open(model_file, 'w', encoding='utf-8') as f:
                    f.write(f'"""Module {main_module} - Modèles SQLAlchemy"""\n')
                    f.write('from app.models.base import BaseModel\n')
                    f.write('from app import db\n')
                    f.write('from datetime import datetime\n\n')
                    f.write(model_code)
            else:
                with open(model_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(model_code)
            
            return True
        except Exception as e:
            print(f"❌ Erreur écriture modèle: {e}")
            return False
    
    def _write_route_file(self, module_id: str, table_name: str, route_code: str) -> bool:
        """Écrire le code des routes dans le fichier du module"""
        try:
            routes_dir = os.path.join(os.path.dirname(__file__), '..', 'routes')
            os.makedirs(routes_dir, exist_ok=True)
            
            main_module = str(module_id).split('_')[0]
            route_file = os.path.join(routes_dir, f'module_{main_module}.py')
            
            if not os.path.exists(route_file):
                with open(route_file, 'w', encoding='utf-8') as f:
                    f.write(f'"""Module {main_module} - Routes Flask"""\n')
                    f.write('from flask import Blueprint, request, jsonify\n')
                    f.write('from app import db\n\n')
                    f.write(f'module_{main_module}_bp = Blueprint(\'module_{main_module}\', __name__)\n\n')
                    f.write(route_code)
            else:
                with open(route_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(route_code)
            
            return True
        except Exception as e:
            print(f"❌ Erreur écriture routes: {e}")
            return False
    
    def _write_schema_file(self, module_id: str, table_name: str, schema_code: str) -> bool:
        """Écrire le code du schéma dans le fichier du module"""
        try:
            schemas_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')
            os.makedirs(schemas_dir, exist_ok=True)
            
            main_module = str(module_id).split('_')[0]
            schema_file = os.path.join(schemas_dir, f'module_{main_module}.py')
            
            if not os.path.exists(schema_file):
                with open(schema_file, 'w', encoding='utf-8') as f:
                    f.write(f'"""Module {main_module} - Schémas Marshmallow"""\n')
                    f.write('from marshmallow import Schema, fields\n\n')
                    f.write(schema_code)
            else:
                with open(schema_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(schema_code)
            
            return True
        except Exception as e:
            print(f"❌ Erreur écriture schéma: {e}")
            return False
    
    def _save_table_definition(self, table_data: Dict[str, Any]) -> None:
        """Sauvegarder la définition de la table pour référence future"""
        # Cette méthode peut être étendue pour sauvegarder les métadonnées
        pass
    
    def _cleanup_on_error(self, table_data: Dict[str, Any]) -> None:
        """Nettoyer les fichiers générés en cas d'erreur"""
        # Cette méthode peut être étendue pour nettoyer les fichiers en cas d'erreur
        pass
    
    def _delete_generated_files_by_table_name(self, table_name: str) -> None:
        """Supprimer les fichiers générés pour une table spécifique"""
        # Cette méthode peut être étendue pour supprimer les fichiers générés
        pass
    
    def _convert_value_type(self, value: Any, column_info: Dict[str, Any]) -> Any:
        """Convertir une valeur selon le type de colonne"""
        if value is None:
            return None
        
        col_type = str(column_info['type']).lower()
        
        if 'integer' in col_type:
            return int(value) if value else 0
        elif 'real' in col_type or 'float' in col_type or 'numeric' in col_type:
            return float(value) if value else 0.0
        elif 'boolean' in col_type:
            return bool(value) if value else False
        else:
            return str(value) if value else ''
    
    def _has_unique_index(self, table_name: str, column_name: str) -> bool:
        """Vérifier si une colonne a un index unique"""
        try:
            # Utiliser SQLAlchemy pour vérifier les index
            inspector = inspect(db.engine)
            indexes = inspector.get_indexes(table_name)
            
            for index in indexes:
                if column_name in index['column_names'] and index.get('unique', False):
                    return True
            
            return False
        except Exception as e:
            print(f"Erreur lors de la vérification de l'index unique: {e}")
            return False
    
    def _generate_relation_names(self, source_table: str, target_table: str) -> Dict[str, str]:
        """Générer les noms automatiquement pour une relation"""
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
    
    def _generate_relation_model_source(self, source_info: Dict[str, Any], target_info: Dict[str, Any], 
                                      names: Dict[str, str], relation_type: str) -> Dict[str, Any]:
        """Générer le code pour le modèle source dans une relation"""
        foreign_key_code = f"    {names['foreign_key_name']} = db.Column(db.Integer, db.ForeignKey('{target_info['name']}.id'), nullable=False)"
        relationship_code = f"    {names['relation_name']} = db.relationship('{names['target_class']}', backref='{names['backref_name']}', lazy='select')"
        
        return {
            'code': f"{foreign_key_code}\n{relationship_code}",
            'file': f"backend/app/models/module_{source_info['module_id']}.py",
            'insert_position': f"Dans la classe {names['source_class']}, après les autres colonnes, avant la méthode __repr__",
            'instructions': [
                f"1. Ouvrir le fichier : backend/app/models/module_{source_info['module_id']}.py",
                f"2. Trouver la classe {names['source_class']}",
                f"3. Insérer le code après les autres colonnes, avant la méthode __repr__",
                f"4. Ajouter l'import si nécessaire : from app.models.module_{target_info['module_id']} import {names['target_class']}"
            ]
        }
    
    def _generate_relation_model_target(self, source_info: Dict[str, Any], target_info: Dict[str, Any], 
                                      names: Dict[str, str], relation_type: str) -> Dict[str, Any]:
        """Générer le code pour le modèle cible dans une relation"""
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
    
    def _generate_relation_schema_source(self, source_info: Dict[str, Any], target_info: Dict[str, Any], 
                                       names: Dict[str, str]) -> Dict[str, Any]:
        """Générer le code pour le schéma source dans une relation"""
        foreign_key_field = f"    {names['foreign_key_name']} = fields.Integer(required=True)"
        relation_field = f"    {names['relation_name']} = fields.Nested('{names['target_class']}Schema', dump_only=True)"
        
        return {
            'code': f"{foreign_key_field}\n{relation_field}",
            'file': f"backend/app/schemas/module_{source_info['module_id']}.py",
            'insert_position': f"Dans la classe {names['source_class']}Schema, après les autres champs",
            'instructions': [
                f"1. Ouvrir le fichier : backend/app/schemas/module_{source_info['module_id']}.py",
                f"2. Trouver la classe {names['source_class']}Schema",
                f"3. Insérer le code après les autres champs",
                f"4. Ajouter l'import si nécessaire : from app.schemas.module_{target_info['module_id']} import {names['target_class']}Schema"
            ]
        }
    
    def _generate_relation_schema_target(self, source_info: Dict[str, Any], target_info: Dict[str, Any], 
                                       names: Dict[str, str]) -> Dict[str, Any]:
        """Générer le code pour le schéma cible dans une relation"""
        backref_field = f"    {names['backref_name']} = fields.Nested('{names['source_class']}Schema', many=True, dump_only=True)"
        
        return {
            'code': backref_field,
            'file': f"backend/app/schemas/module_{target_info['module_id']}.py",
            'insert_position': f"Dans la classe {names['target_class']}Schema, après les autres champs",
            'instructions': [
                f"1. Ouvrir le fichier : backend/app/schemas/module_{target_info['module_id']}.py",
                f"2. Trouver la classe {names['target_class']}Schema",
                f"3. Insérer le code après les autres champs",
                f"4. Ajouter l'import si nécessaire : from app.schemas.module_{source_info['module_id']} import {names['source_class']}Schema"
            ]
        }
    
    def _generate_relation_migration(self, source_info: Dict[str, Any], target_info: Dict[str, Any], 
                                   names: Dict[str, str]) -> Dict[str, Any]:
        """Générer le code de migration pour une relation"""
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


# Instance globale du service
database_manager = DatabaseManager() 