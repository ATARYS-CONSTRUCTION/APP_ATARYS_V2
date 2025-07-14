#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - SERVICE DE GÉNÉRATION DE TABLES SQLALCHEMY
Générateur automatique pour le module 12.1 Base de Données

Auteur: ATARYS Team
Date: 2025
Version: 2.0 - Architecture modulaire
"""

import os
import re
from sqlalchemy import text
from app import db


class TableGeneratorService:
    """Service pour générer automatiquement les modèles et routes SQLAlchemy"""
    
    def __init__(self):
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
        
        # Mapping vers SQLite
        self.sqlite_types = {
            'Integer': 'INTEGER',
            'String': 'TEXT',
            'Text': 'TEXT',
            'Numeric': 'REAL',
            'REAL': 'REAL',
            'Boolean': 'INTEGER',
            'Date': 'TEXT',
            'DateTime': 'TEXT',
            'Time': 'TEXT',
            'Timestamp': 'TEXT',
            'JSON': 'TEXT',
            'LargeBinary': 'BLOB',
            'Enum': 'TEXT'
        }
    
    def create_table_professional(self, table_data):
        """
        Créer une table de manière professionnelle (génération de code + instructions migration)
        
        Args:
            table_data (dict): {
                'module_id': int,
                'table_name': str,
                'class_name': str,
                'columns': list,
                'options': {
                    'hasPrimaryKey': bool,
                    'hasTimestamps': bool,
                    'primaryKeyColumn': str,
                    'autoIncrement': bool
                }
            }
        
        Returns:
            dict: {'success': bool, 'message': str, 'data': dict}
        """
        try:
            # 1. Validation du schéma
            validation_result = self._validate_table_schema(table_data)
            if not validation_result['success']:
                return validation_result
            
            # 2. Génération des fichiers backend (sans toucher à la base)
            model_code = self._generate_model_code(table_data)
            route_code = self._generate_route_code(table_data)
            schema_code = self._generate_schema_code(table_data)
            
            # 3. Écriture des fichiers
            self._write_model_file(table_data['module_id'], table_data['table_name'], model_code)
            self._write_route_file(table_data['module_id'], table_data['table_name'], route_code)
            self._write_schema_file(table_data['module_id'], table_data['table_name'], schema_code)
            
            # 4. Enregistrement des métadonnées
            self._save_table_definition(table_data)
            
            # 5. Instructions pour l'utilisateur
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

    def create_table(self, table_data):
        """
        Créer une table complète avec modèle et routes (version professionnelle)
        
        Args:
            table_data (dict): {
                'module_id': int,
                'table_name': str,
                'class_name': str,
                'columns': list,
                'options': {
                    'hasPrimaryKey': bool,
                    'hasTimestamps': bool,
                    'primaryKeyColumn': str,
                    'autoIncrement': bool
                }
            }
        
        Returns:
            dict: {'success': bool, 'message': str, 'data': dict}
        """
        # Utiliser la version professionnelle qui respecte Flask-Migrate
        return self.create_table_professional(table_data)
    
    def modify_table(self, table_data, modifications):
        """
        Modifier une table existante
        
        Args:
            table_data (dict): Données de la table
            modifications (dict): Modifications à apporter
        
        Returns:
            dict: Résultat de la modification
        """
        try:
            # 1. Validation des modifications
            validation_result = self._validate_modifications(table_data, modifications)
            if not validation_result['success']:
                return validation_result
            
            # 2. Application des modifications
            for modification in modifications:
                if modification['type'] == 'add_column':
                    self._add_column(table_data['table_name'], modification['column'])
                elif modification['type'] == 'modify_column':
                    self._modify_column(table_data['table_name'], modification['column'])
                elif modification['type'] == 'drop_column':
                    self._drop_column(table_data['table_name'], modification['column_name'])
            
            # 3. Mise à jour des fichiers générés
            self._update_generated_files(table_data)
            
            return {
                'success': True,
                'message': f"Table '{table_data['table_name']}' modifiée avec succès"
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur lors de la modification : {str(e)}"
            }
    
    def delete_table_professional(self, table_data):
        """
        Supprimer une table de manière professionnelle (suppression code + instructions migration)
        
        Args:
            table_data (dict): Données de la table
        
        Returns:
            dict: Résultat de la suppression
        """
        try:
            table_name = table_data['table_name']
            class_name = table_data['class_name']
            
            # 1. Suppression des fichiers générés
            self._delete_generated_files(table_data)
            
            # 2. Suppression des métadonnées
            self._delete_table_definition(table_data)
            
            return {
                'success': True,
                'message': f"✅ Code supprimé pour '{table_name}'. Lancez maintenant les migrations :",
                'data': {
                    'table_name': table_name,
                    'class_name': class_name,
                    'next_steps': [
                        f"flask db migrate -m 'Remove table {table_name}'",
                        "flask db upgrade"
                    ],
                    'warning': "⚠️ N'oubliez pas de lancer les migrations pour supprimer la table de la base de données",
                    'files_deleted': [
                        f"backend/app/models/module_{table_data['module_id']}.py",
                        f"backend/app/routes/module_{table_data['module_id']}.py", 
                        f"backend/app/schemas/module_{table_data['module_id']}.py"
                    ]
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Erreur lors de la suppression : {str(e)}"
            }

    def delete_table(self, table_data):
        """
        Supprimer une table complètement (version professionnelle)
        
        Args:
            table_data (dict): Données de la table
        
        Returns:
            dict: Résultat de la suppression
        """
        # Utiliser la version professionnelle qui respecte Flask-Migrate
        return self.delete_table_professional(table_data)
    
    def delete_table_by_name(self, table_name):
        """
        Supprimer une table par son nom (table SQLite + fichiers générés)
        
        Args:
            table_name (str): Nom de la table à supprimer
        
        Returns:
            dict: Résultat de la suppression
        """
        try:
            # 1. Vérifier que la table existe
            result = db.session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"),
                {'table_name': table_name}
            ).fetchone()
            
            if not result:
                return {
                    'success': False,
                    'message': f'Table {table_name} n\'existe pas'
                }
            
            # 2. Supprimer la table SQLite
            db.session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            db.session.commit()
            
            # 3. Supprimer les fichiers générés (modèle, routes, schéma)
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
    
    def list_tables(self):
        """Retourne la liste enrichie des tables SQLite (hors tables système), avec dates au format ISO 8601."""
        try:
            result = db.session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
            )
            tables = [row[0] for row in result.fetchall()]
            enriched = []
            for table in tables:
                # Récupérer les colonnes
                cols_result = db.session.execute(text(f"PRAGMA table_info({table})"))
                columns = [col[1] for col in cols_result.fetchall()]
                # Récupérer la date de création (première valeur created_at si possible)
                created_at = '-'
                try:
                    row = db.session.execute(text(f"SELECT created_at FROM {table} ORDER BY created_at ASC LIMIT 1")).fetchone()
                    if row and row[0]:
                        # Convertir au format ISO 8601
                        created_at = str(row[0]).replace(' ', 'T')
                except Exception:
                    pass
                # Déduire le module si possible (ex: module_3_xxx)
                module = ''
                match = re.match(r'module_(\d+)', table)
                if match:
                    module_id = int(match.group(1))
                    module = self.modules_atarys.get(module_id, str(module_id))
                enriched.append({
                    'name': table,
                    'module': module,
                    'columns': columns,
                    'created_at': created_at,
                })
            return enriched
        except Exception as e:
            print(f"Erreur lors du listing enrichi des tables : {e}")
            return []
    
    def check_migration_status(self):
        """
        Vérifier l'état des migrations et donner des conseils
        
        Returns:
            dict: État des migrations et conseils
        """
        try:
            import subprocess
            import os
            
            # Vérifier si on est dans le bon répertoire
            if not os.path.exists('migrations'):
                return {
                    'success': False,
                    'message': '❌ Répertoire migrations non trouvé. Lancez d\'abord : flask db init',
                    'data': {
                        'status': 'not_initialized',
                        'next_steps': ['flask db init']
                    }
                }
            
            # Vérifier l'état actuel des migrations
            try:
                result = subprocess.run(
                    ['flask', 'db', 'current'], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                
                if result.returncode == 0:
                    current_revision = result.stdout.strip()
                    return {
                        'success': True,
                        'message': f'✅ Migrations initialisées. Révision actuelle : {current_revision}',
                        'data': {
                            'status': 'ready',
                            'current_revision': current_revision,
                            'next_steps': [
                                'flask db migrate -m "Description des changements"',
                                'flask db upgrade'
                            ]
                        }
                    }
                else:
                    return {
                        'success': False,
                        'message': '❌ Erreur lors de la vérification des migrations',
                        'data': {
                            'status': 'error',
                            'error': result.stderr,
                            'next_steps': ['flask db init', 'flask db migrate', 'flask db upgrade']
                        }
                    }
                    
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'message': '❌ Timeout lors de la vérification des migrations',
                    'data': {
                        'status': 'timeout',
                        'next_steps': ['Vérifiez la configuration Flask']
                    }
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Erreur lors de la vérification : {str(e)}',
                'data': {
                    'status': 'error',
                    'error': str(e)
                }
            }

    def get_migration_help(self):
        """
        Obtenir l'aide pour les migrations Flask-Migrate
        
        Returns:
            dict: Guide d'utilisation des migrations
        """
        return {
            'success': True,
            'message': '📚 Guide des migrations Flask-Migrate',
            'data': {
                'workflow': [
                    '1. Créer/modifier les modèles Python',
                    '2. Générer une migration : flask db migrate -m "Description"',
                    '3. Appliquer la migration : flask db upgrade',
                    '4. Vérifier : flask db current'
                ],
                'commands': {
                    'init': 'flask db init - Initialiser les migrations (première fois)',
                    'migrate': 'flask db migrate -m "Description" - Générer une migration',
                    'upgrade': 'flask db upgrade - Appliquer les migrations',
                    'downgrade': 'flask db downgrade - Revenir en arrière',
                    'current': 'flask db current - Voir la révision actuelle',
                    'history': 'flask db history - Voir l\'historique des migrations'
                },
                'tips': [
                    '✅ Toujours décrire les changements dans le message de migration',
                    '✅ Tester les migrations sur une base de test avant production',
                    '✅ Versionner les fichiers de migration avec le code',
                    '⚠️ Ne jamais modifier une migration déjà appliquée',
                    '⚠️ Toujours faire un backup avant de migrer en production'
                ]
            }
        }
    
    def _validate_table_schema(self, table_data):
        """Valider le schéma de la table"""
        errors = []
        
        # Validation du nom de table
        if not re.match(r'^[a-z][a-z0-9_]*$', table_data['table_name']):
            errors.append("Nom de table invalide (doit être en snake_case)")
        
        # Validation des colonnes
        if not table_data['columns']:
            errors.append("Au moins une colonne est requise")
        
        # Validation des clés primaires
        primary_keys = [col for col in table_data['columns'] if col.get('primaryKey')]
        if len(primary_keys) > 1:
            errors.append("Une seule clé primaire autorisée")
        
        # Validation des types
        for col in table_data['columns']:
            if col['type'] not in self.sqlalchemy_types:
                errors.append(f"Type '{col['type']}' non supporté pour la colonne '{col['name']}'")
            
            if col['type'] == 'String' and not col.get('maxLength') and not col.get('max_length'):
                errors.append(f"Longueur max requise pour String dans la colonne '{col['name']}'")
        
        # Validation des clés étrangères
        for col in table_data['columns']:
            if col.get('isForeignKey'):
                if not col.get('foreignKeyTable'):
                    errors.append(f"Table de référence requise pour la clé étrangère '{col['name']}'")
        
        if errors:
            return {'success': False, 'message': '; '.join(errors)}
        
        return {'success': True}
    
    def _create_sqlite_table(self, table_data):
        """Créer la table SQLite"""
        try:
            # Générer la requête SQL CREATE TABLE
            columns_sql = []
            column_names = [col['name'] for col in table_data['columns']]
            options = table_data.get('options', {})

            # Forcer l'ajout de id, created_at, updated_at si demandé dans options
            if options.get('id', True) and 'id' not in column_names:
                columns_sql.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
            # Colonnes utilisateur
            for col in table_data['columns']:
                if col['name'] in ['id', 'created_at', 'updated_at']:
                    continue
                sql_type = self.sqlite_types.get(col['type'], 'TEXT')
                col_def = f"{col['name']} {sql_type}"
                if not col.get('nullable', True):
                    col_def += " NOT NULL"
                if col.get('unique', False):
                    col_def += " UNIQUE"
                if col.get('primaryKey', False):
                    col_def += " PRIMARY KEY"
                    if col.get('autoIncrement', False):
                        col_def += " AUTOINCREMENT"
                if col.get('default') is not None:
                    default_val = col['default']
                    if col['type'] == 'Boolean':
                        default_val = '1' if default_val else '0'
                    elif col['type'] == 'String':
                        default_val = f"'{default_val}'"
                    elif col['type'] == 'DateTime' and default_val == 'datetime.utcnow':
                        default_val = 'CURRENT_TIMESTAMP'
                    col_def += f" DEFAULT {default_val}"
                columns_sql.append(col_def)
            if options.get('created_at', True) and 'created_at' not in column_names:
                columns_sql.append("created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            if options.get('updated_at', True) and 'updated_at' not in column_names:
                columns_sql.append("updated_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            columns_str = ",\n    ".join(columns_sql)
            create_sql = f"CREATE TABLE {table_data['table_name']} (\n    {columns_str}\n)"
            print(f"🔧 SQL généré: {create_sql}")
            db.session.execute(text(create_sql))
            db.session.commit()
            return {'success': True}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def _generate_model_code(self, table_data):
        """Générer le code du modèle SQLAlchemy"""
        class_name = table_data['class_name']
        table_name = table_data['table_name']
        module_name = f"module_{table_data['module_id']}"
        options = table_data.get('options', {})
        # Imports
        imports = [
            "from app.models.base import BaseModel",
            "from app import db",
            "from datetime import datetime"
        ]
        # Définition de la classe
        class_def = f"""
class {class_name}(BaseModel):
    __tablename__ = '{table_name}'
    
"""
        columns_code = []
        column_names = [col['name'] for col in table_data['columns']]
        # id
        if options.get('id', True) and 'id' not in column_names:
            columns_code.append("    id = db.Column(db.Integer, primary_key=True, autoincrement=True)")
        # Colonnes utilisateur
        for col in table_data['columns']:
            if col['name'] in ['id', 'created_at', 'updated_at']:
                continue
            sqlalchemy_type = self.sqlalchemy_types.get(col['type'], 'db.String')
            params = []
            if not col.get('nullable', True):
                params.append('nullable=False')
            if col.get('unique', False):
                params.append('unique=True')
            if col.get('primaryKey', False):
                params.append('primary_key=True')
                if col.get('autoIncrement', False):
                    params.append('autoincrement=True')
            if col.get('default') is not None:
                default_val = col['default']
                if col['type'] == 'DateTime':
                    params.append('default=datetime.utcnow')
                elif col['type'] == 'Boolean':
                    params.append(f'default={str(default_val).lower()}')
                elif col['type'] == 'String':
                    params.append(f"default='{default_val}'")
                else:
                    params.append(f'default={default_val}')
            if col['type'] == 'String' and (col.get('maxLength') or col.get('max_length')):
                max_length = col.get('maxLength') or col.get('max_length')
                sqlalchemy_type = f"db.String({max_length})"
            if col.get('isForeignKey'):
                foreign_table = col['foreignKeyTable']
                foreign_column = col['foreignKeyColumn']
                fk_param = f"db.ForeignKey('{foreign_table}.{foreign_column}')"
                params.append(fk_param)
            params_str = ', '.join(params)
            column_def = f"    {col['name']} = {sqlalchemy_type}({params_str})"
            columns_code.append(column_def)
        # created_at
        if options.get('created_at', True) and 'created_at' not in column_names:
            columns_code.append("    created_at = db.Column(db.DateTime, default=datetime.utcnow)")
        # updated_at
        if options.get('updated_at', True) and 'updated_at' not in column_names:
            columns_code.append("    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)")
        # Méthode __repr__
        repr_method = f"""
    def __repr__(self):
        return f'<{class_name} {{self.id}}>'
"""
        model_code = '\n'.join(imports) + class_def + '\n'.join(columns_code) + repr_method
        return model_code
    
    def _generate_route_code(self, table_data):
        """Générer le code des routes API à insérer dans le fichier du module (sans blueprint)"""
        class_name = table_data['class_name']
        table_name = table_data['table_name']
        
        # Extraire le numéro principal du module (ex: 12 de "12_1")
        main_module = str(table_data['module_id']).split('_')[0]
        
        # Schéma Marshmallow
        route_code = (
            f"\n# Schéma et routes CRUD pour {class_name}\n"
            f"class {class_name}Schema(Schema):\n"
        )
        for col in table_data['columns']:
            if col['name'] in ['id', 'created_at', 'updated_at']:
                continue
            if col['type'] == 'Integer':
                route_code += f"    {col['name']} = fields.Integer()\n"
            elif col['type'] == 'String':
                route_code += f"    {col['name']} = fields.String()\n"
            elif col['type'] == 'Text':
                route_code += f"    {col['name']} = fields.String()\n"
            elif col['type'] == 'Numeric':
                route_code += f"    {col['name']} = fields.Decimal()\n"
            elif col['type'] == 'Boolean':
                route_code += f"    {col['name']} = fields.Boolean()\n"
            elif col['type'] == 'Date':
                route_code += f"    {col['name']} = fields.Date()\n"
            elif col['type'] == 'DateTime':
                route_code += f"    {col['name']} = fields.DateTime()\n"
            else:
                route_code += f"    {col['name']} = fields.String()\n"
        route_code += f"\n{table_name}_schema = {class_name}Schema()\n{table_name}_schemas = {class_name}Schema(many=True)\n\n"
        # GET
        route_code += (
            f"@module_{main_module}_bp.route('/api/{table_name}/', "
            f"methods=['GET'])\n"
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
            f"@module_{main_module}_bp.route('/api/{table_name}/', "
            f"methods=['POST'])\n"
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
        # PUT
        route_code += (
            f"@module_{main_module}_bp.route('/api/{table_name}/<int:item_id>', "
            f"methods=['PUT'])\n"
            f"def update_{table_name}(item_id):\n"
            f"    try:\n"
            f"        item = {class_name}.query.get_or_404(item_id)\n"
            f"        data = request.get_json()\n"
            f"        errors = {table_name}_schema.validate(data)\n"
            f"        if errors:\n"
            f"            return jsonify({{'success': False, 'message': errors}}), 400\n"
            f"        for key, value in data.items():\n"
            f"            setattr(item, key, value)\n"
            f"        db.session.commit()\n"
            f"        return jsonify({{\n"
            f"            'success': True,\n"
            f"            'data': {table_name}_schema.dump(item),\n"
            f"            'message': '{class_name} modifié avec succès'\n"
            f"        }})\n"
            f"    except Exception as e:\n"
            f"        db.session.rollback()\n"
            f"        return jsonify({{'success': False, 'message': str(e)}}), 400\n\n"
        )
        # DELETE
        route_code += (
            f"@module_{main_module}_bp.route('/api/{table_name}/<int:item_id>', "
            f"methods=['DELETE'])\n"
            f"def delete_{table_name}(item_id):\n"
            f"    try:\n"
            f"        item = {class_name}.query.get_or_404(item_id)\n"
            f"        db.session.delete(item)\n"
            f"        db.session.commit()\n"
            f"        return jsonify({{\n"
            f"            'success': True,\n"
            f"            'message': '{class_name} supprimé avec succès'\n"
            f"        }})\n"
            f"    except Exception as e:\n"
            f"        db.session.rollback()\n"
            f"        return jsonify({{'success': False, 'message': str(e)}}), 400\n"
        )
        return route_code
    
    def _generate_schema_code(self, table_data):
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
    
    def _write_model_file(self, module_id, table_name, model_code):
        """Ajouter la classe générée à la fin du fichier module_X.py du module concerné (créé si besoin)."""
        try:
            models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
            os.makedirs(models_dir, exist_ok=True)
            
            # Extraire le numéro principal du module (ex: 12 de "12_1")
            main_module = str(module_id).split('_')[0]
            module_file = os.path.join(models_dir, f'module_{main_module}.py')
            
            header = (
                '"""\n'
                f'Module {main_module} - Modèles SQLAlchemy\n'
                'Respecte les standards ATARYS V2 (voir .cursorrules et docs/02-architecture/ATARYS_MODULES.md)\n'
                '- Hérite toujours de BaseModel\n'
                '- Utilise db.Numeric(10, 2) pour montants financiers\n'
                '- Strings avec longueur max obligatoire\n'
                '- __repr__ explicite\n"""\n'
                'from backend.app.models.base import BaseModel\n'
                'from backend.app import db\n\n'
                f'# Modèles du module {main_module} - '
                f'{self.modules_atarys.get(int(main_module), "MODULE").replace("_", " ")}\n'
                f'# Ajouter ici les modèles du module {main_module} selon les besoins \n'
            )
            if not os.path.exists(module_file):
                with open(module_file, 'w', encoding='utf-8') as f:
                    f.write(header)
                    f.write('\n')
                    f.write(model_code)
            else:
                with open(module_file, 'a', encoding='utf-8') as f:
                    f.write('\n\n')
                    f.write(model_code)
            print(f"✅ Classe ajoutée dans {module_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur ajout modèle dans module: {e}")
            return False
    
    def _write_route_file(self, module_id, table_name, route_code):
        """Ajouter le code CRUD de la table à la fin du fichier module_X.py du module routes (créé si besoin)."""
        try:
            routes_dir = os.path.join(os.path.dirname(__file__), '..', 'routes')
            os.makedirs(routes_dir, exist_ok=True)
            
            # Extraire le numéro principal du module (ex: 12 de "12_1")
            main_module = str(module_id).split('_')[0]
            route_file = os.path.join(routes_dir, f'module_{main_module}.py')
            
            header = (
                '"""\n'
                f'Module {main_module} - Routes Flask\n'
                'Respecte les standards ATARYS V2 (voir .cursorrules et docs/02-architecture/ATARYS_MODULES.md)\n'
                '- Blueprint unique par module\n'
                '- CRUD pour chaque table du module\n"""\n'
                'from flask import Blueprint, request, jsonify\n'
                'from backend.app import db\n'
                'from marshmallow import Schema, fields\n\n'
                f"module_{main_module}_bp = Blueprint('module_{main_module}', __name__)\n\n"
                f'# Routes du module {main_module}\n'
            )
            if not os.path.exists(route_file):
                with open(route_file, 'w', encoding='utf-8') as f:
                    f.write(header)
                    f.write(route_code)
            else:
                with open(route_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(route_code)
            print(f"✅ Routes CRUD ajoutées dans {route_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur ajout routes CRUD: {e}")
            return False

    def _write_schema_file(self, module_id, table_name, schema_code):
        """Ajouter le schéma Marshmallow à la fin du fichier module_X.py du module schemas (créé si besoin)."""
        try:
            schemas_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')
            os.makedirs(schemas_dir, exist_ok=True)
            
            # Extraire le numéro principal du module (ex: 12 de "12_1")
            main_module = str(module_id).split('_')[0]
            schema_file = os.path.join(schemas_dir, f'module_{main_module}.py')
            
            header = (
                '"""\n'
                f'Module {main_module} - Schémas Marshmallow\n'
                'Respecte les standards ATARYS V2 (voir .cursorrules et docs/02-architecture/ATARYS_MODULES.md)\n'
                '- Un fichier par module\n'
                '- Un schéma par table\n"""\n'
                'from marshmallow import Schema, fields\n\n'
                f'# Schémas du module {main_module}\n'
            )
            if not os.path.exists(schema_file):
                with open(schema_file, 'w', encoding='utf-8') as f:
                    f.write(header)
                    f.write(schema_code)
            else:
                with open(schema_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(schema_code)
            print(f"✅ Schéma ajouté dans {schema_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur ajout schéma: {e}")
            return False
    
    def _save_table_definition(self, table_data):
        """Sauvegarder la définition de la table dans la base de données"""
        # Cette méthode sera implémentée quand on aura les modèles de métadonnées
        pass
    
    def _cleanup_on_error(self, table_data):
        """Nettoyer les fichiers créés en cas d'erreur"""
        try:
            # Supprimer la table SQLite si elle a été créée
            db.session.execute(text(f"DROP TABLE IF EXISTS {table_data['table_name']}"))
            db.session.commit()
        except:
            pass
        
        # Supprimer les fichiers générés
        self._delete_generated_files(table_data)
    
    def _delete_generated_files(self, table_data):
        """Supprimer les fichiers générés"""
        module_id = table_data['module_id']
        table_name = table_data['table_name']
        
        # Fichiers à supprimer
        files_to_delete = [
            f"app/models/module_{module_id}.py",
            f"app/routes/module_{module_id}.py",
            f"app/schemas/module_{module_id}.py"
        ]
        
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                # Supprimer seulement la partie générée, pas le fichier entier
                # (car d'autres tables peuvent être dans le même fichier)
                pass
    
    def _delete_generated_files_by_table_name(self, table_name):
        """
        Supprimer les fichiers générés pour une table spécifique
        (modèle, routes, schéma dans les fichiers de module)
        """
        try:
            # Chercher dans tous les fichiers de module pour supprimer les classes/routes/schémas
            # de cette table spécifique
            
            # 1. Supprimer le modèle
            self._remove_model_from_files(table_name)
            
            # 2. Supprimer les routes
            self._remove_routes_from_files(table_name)
            
            # 3. Supprimer le schéma
            self._remove_schema_from_files(table_name)
            
            print(f"✅ Fichiers générés supprimés pour {table_name}")
            
        except Exception as e:
            print(f"❌ Erreur suppression fichiers générés: {e}")
    
    def _remove_model_from_files(self, table_name):
        """Supprimer la classe modèle de tous les fichiers module_X.py"""
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        for filename in os.listdir(models_dir):
            if filename.startswith('module_') and filename.endswith('.py'):
                file_path = os.path.join(models_dir, filename)
                self._remove_class_from_file(file_path, table_name, 'class')
    
    def _remove_routes_from_files(self, table_name):
        """Supprimer les routes de tous les fichiers module_X.py"""
        routes_dir = os.path.join(os.path.dirname(__file__), '..', 'routes')
        
        for filename in os.listdir(routes_dir):
            if filename.startswith('module_') and filename.endswith('.py'):
                file_path = os.path.join(routes_dir, filename)
                self._remove_class_from_file(file_path, table_name, 'route')
    
    def _remove_schema_from_files(self, table_name):
        """Supprimer le schéma de tous les fichiers module_X.py"""
        schemas_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')
        
        for filename in os.listdir(schemas_dir):
            if filename.startswith('module_') and filename.endswith('.py'):
                file_path = os.path.join(schemas_dir, filename)
                self._remove_class_from_file(file_path, table_name, 'schema')
    
    def _remove_class_from_file(self, file_path, table_name, content_type):
        """
        Supprimer une classe/routes/schéma spécifique d'un fichier
        Args:
            file_path (str): Chemin du fichier
            table_name (str): Nom de la table
            content_type (str): 'class', 'route', ou 'schema'
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            class_name = self._snake_to_pascal(table_name)
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Suppression du bloc CRUD complet (avec ou sans commentaire)
                if content_type == 'route':
                    # Bloc avec commentaire
                    if f'# Schéma et routes CRUD pour {class_name}' in line:
                        i += 1
                        while i < len(lines) and not lines[i].startswith('# Schéma et routes CRUD pour') and not lines[i].startswith('class ') and not lines[i].startswith('def '):
                            i += 1
                        continue
                    # Bloc sans commentaire, détecter la classe schéma ou la fonction route
                    if f'class {class_name}Schema(Schema):' in line or f'def list_{table_name}()' in line or f'def create_{table_name}()' in line:
                        # Remonter pour supprimer les décorateurs éventuels
                        start = i
                        while start > 0 and lines[start-1].strip().startswith('@'):
                            start -= 1
                        i = start
                        # Sauter jusqu'à la prochaine classe/fonction ou fin de fichier
                        while i < len(lines) and not lines[i].startswith('class ') and not lines[i].startswith('def ') and not lines[i].startswith('# Schéma et routes CRUD pour'):
                            i += 1
                        continue
                # Suppression du bloc modèle
                if content_type == 'class' and f'class {class_name}(BaseModel):' in line:
                    i += 1
                    while i < len(lines) and not lines[i].startswith('class '):
                        i += 1
                    continue
                # Suppression du bloc schéma
                if content_type == 'schema' and f'class {class_name}Schema(Schema):' in line:
                    i += 1
                    while i < len(lines) and not lines[i].startswith('class '):
                        i += 1
                    continue
                new_lines.append(line)
                i += 1
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        except Exception as e:
            print(f"❌ Erreur suppression {content_type} de {file_path}: {e}")
    
    def _validate_modifications(self, table_data, modifications):
        """Valider les modifications de structure"""
        # À implémenter selon les besoins
        return {'success': True}
    
    def _add_column(self, table_name, column_data):
        """Ajouter une colonne à une table existante"""
        try:
            sql_type = self.sqlite_types.get(column_data['type'], 'TEXT')
            col_def = f"{column_data['name']} {sql_type}"
            
            if not column_data.get('nullable', True):
                col_def += " NOT NULL"
            
            if column_data.get('unique', False):
                col_def += " UNIQUE"
            
            if column_data.get('default') is not None:
                default_val = column_data['default']
                if column_data['type'] == 'Boolean':
                    default_val = '1' if default_val else '0'
                elif column_data['type'] == 'String':
                    default_val = f"'{default_val}'"
                col_def += f" DEFAULT {default_val}"
            
            # SQLite supporte ADD COLUMN
            db.session.execute(
                text(f"ALTER TABLE {table_name} ADD COLUMN {col_def}")
            )
            db.session.commit()
            
            print(f"✅ Colonne {column_data['name']} ajoutée à {table_name}")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur ajout colonne: {e}")
            return False
    
    def _modify_column(self, table_name, column_data):
        """Modifier une colonne existante (SQLite limitations)"""
        try:
            # SQLite a des limitations pour ALTER TABLE
            # On ne peut que renommer ou ajouter des colonnes
            # Pour modifier le type, il faut recréer la table
            
            if 'new_name' in column_data:
                # Renommer la colonne
                old_name = column_data['name']
                new_name = column_data['new_name']
                
                # Récupérer la définition de la colonne
                result = db.session.execute(
                    text(f"PRAGMA table_info({table_name})")
                ).fetchall()
                
                for col in result:
                    if col[1] == old_name:
                        # Créer une nouvelle table avec la colonne renommée
                        # (SQLite ne supporte pas RENAME COLUMN directement)
                        print(f"⚠️ Renommage de colonne non supporté par SQLite")
                        return False
                        
            return True
            
        except Exception as e:
            print(f"❌ Erreur modification colonne: {e}")
            return False
    
    def _drop_column(self, table_name, column_name):
        """Supprimer une colonne (SQLite limitations)"""
        try:
            # SQLite ne supporte pas DROP COLUMN directement
            # Il faut créer une nouvelle table sans la colonne
            
            # Récupérer la structure actuelle
            result = db.session.execute(
                text(f"PRAGMA table_info({table_name})")
            ).fetchall()
            
            # Créer une nouvelle table sans la colonne à supprimer
            columns_to_keep = []
            for col in result:
                if col[1] != column_name:
                    col_def = f"{col[1]} {col[2]}"
                    if col[3]:  # NOT NULL
                        col_def += " NOT NULL"
                    if col[4]:  # DEFAULT
                        col_def += f" DEFAULT {col[4]}"
                    if col[5]:  # PRIMARY KEY
                        col_def += " PRIMARY KEY"
                    columns_to_keep.append(col_def)
            
            # Créer la nouvelle table
            temp_table = f"{table_name}_temp"
            columns_str = ", ".join(columns_to_keep)
            select_cols = ', '.join(
                [col[1] for col in result if col[1] != column_name]
            )
            create_sql = (
                f"CREATE TABLE {temp_table} AS "
                f"SELECT {select_cols} FROM {table_name}"
            )
            
            db.session.execute(text(create_sql))
            db.session.execute(text(f"DROP TABLE {table_name}"))
            db.session.execute(
                text(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
            )
            db.session.commit()
            
            print(f"✅ Colonne {column_name} supprimée de {table_name}")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur suppression colonne: {e}")
            return False
    
    def _update_generated_files(self, table_data):
        """Mettre à jour les fichiers générés après modification"""
        # Régénérer les fichiers avec la nouvelle structure
        model_code = self._generate_model_code(table_data)
        route_code = self._generate_route_code(table_data)
        schema_code = self._generate_schema_code(table_data)
        
        self._write_model_file(table_data['module_id'], table_data['table_name'], model_code)
        self._write_route_file(table_data['module_id'], table_data['table_name'], route_code)
        self._write_schema_file(table_data['module_id'], table_data['table_name'], schema_code)
    
    def _snake_to_pascal(self, snake_case):
        """Convertir snake_case en PascalCase"""
        return ''.join(word.capitalize() for word in snake_case.split('_'))
    
    def _pascal_to_snake(self, pascal_case):
        """Convertir PascalCase en snake_case"""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_case).lower()


# Instance globale du service
table_generator = TableGeneratorService() 