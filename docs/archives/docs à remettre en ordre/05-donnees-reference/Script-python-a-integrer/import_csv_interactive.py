#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - IMPORT CSV INTERACTIF
Script d'import de données CSV vers la base de données ATARYS

Auteur: ATARYS Team
Date: 2025
"""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd


class ATARYSCSVImporter:
    """Classe principale pour l'import CSV interactif ATARYS"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent
        self.csv_dir = self.data_dir / "DB_CSV"
        self.config_dir = self.data_dir / "import_configs"
        self.logs_dir = self.data_dir / "import_logs"
        
        # Créer les dossiers nécessaires
        self.csv_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Configuration des modules ATARYS - Nomenclature officielle
        # Les tables seront créées dynamiquement selon les fichiers CSV disponibles
        self.modules_atarys = {
            1: {"name": "📅 1. PLANNING", "description": "Planning salariés et chantiers"},
            2: {"name": "📋 2. LISTE DES TÂCHES", "description": "Tâches Yann et Julien"},
            3: {"name": "🏗️ 3. LISTE CHANTIERS", "description": "Gestion des chantiers clients"},
            4: {"name": "🔧 4. CHANTIERS", "description": "Suivi détaillé des chantiers"},
            5: {"name": "💰 5. DEVIS-FACTURATION", "description": "Devis et facturation"},
            6: {"name": "🏭 6. ATELIER", "description": "Gestion de l'atelier"},
            7: {"name": "📊 7. GESTION", "description": "Gestion prévisionnelle"},
            8: {"name": "🏦 8. COMPTABILITE", "description": "Comptabilité et TVA"},
            9: {"name": "👥 9. SOCIAL", "description": "Gestion des salariés"},
            10: {"name": "🛠️ 10. OUTILS", "description": "Outils de calcul"},
            11: {"name": "📚 11. ARCHIVES", "description": "Archivage"},
            12: {"name": "⚙️ 12. PARAMETRES", "description": "Paramètres système"},
            13: {"name": "❓ 13. AIDE", "description": "Aide et documentation"}
        }
        
        # Types de données disponibles
        self.data_types = {
            1: {"name": "INTEGER", "description": "Nombre entier (ex: 1, 42, 1000)", 
                "python_type": int},
            2: {"name": "TEXT", "description": "Texte libre (ex: nom, adresse, description)", 
                "python_type": str},
            3: {"name": "NUMERIC", "description": "Nombre décimal (ex: 15.50, 1000.00)", 
                "python_type": float},
            4: {"name": "DATE", "description": "Date (format: YYYY-MM-DD)", 
                "python_type": "date"},
            5: {"name": "DATETIME", 
                "description": "Date et heure (format: YYYY-MM-DD HH:MM:SS)", 
                "python_type": "datetime"},
            6: {"name": "BOOLEAN", 
                "description": "Vrai/Faux (ex: 1/0, true/false, oui/non)", 
                "python_type": bool},
            7: {"name": "ENUM", 
                "description": "Liste de valeurs prédéfinies (ex: statuts, types)", 
                "python_type": "enum"},
            8: {"name": "EMAIL", "description": "Adresse email avec validation", 
                "python_type": "email"},
            9: {"name": "PHONE", "description": "Numéro de téléphone formaté", 
                "python_type": "phone"},
            10: {"name": "POSTAL_CODE", "description": "Code postal français (5 chiffres)", 
                 "python_type": "postal_code"},
            11: {"name": "CURRENCY", "description": "Montant monétaire (ex: 1500.00 €)", 
                 "python_type": "currency"},
            12: {"name": "PERCENTAGE", "description": "Pourcentage (ex: 15.5 pour 15.5%)", 
                 "python_type": "percentage"},
            13: {"name": "JSON", "description": "Données structurées JSON", 
                 "python_type": "json"},
            14: {"name": "URL", "description": "Lien web avec validation", 
                 "python_type": "url"},
            15: {"name": "FOREIGN_KEY", 
                 "description": "Clé étrangère vers une autre table", 
                 "python_type": "foreign_key"},
            16: {"name": "PRIMARY_KEY", 
                 "description": "Clé primaire (généralement id, auto-incrémenté)", 
                 "python_type": "primary_key"}
        }
        
        # Contraintes disponibles
        self.constraints = {
            1: {"name": "NOT NULL", "description": "La colonne ne peut pas être vide", 
                "sql": "NOT NULL"},
            2: {"name": "UNIQUE", "description": "Valeurs uniques dans la colonne", 
                "sql": "UNIQUE"},
            3: {"name": "DEFAULT", "description": "Valeur par défaut si non spécifiée", 
                "sql": "DEFAULT"},
            4: {"name": "CHECK", "description": "Condition personnalisée", 
                "sql": "CHECK"},
            5: {"name": "AUTO_INCREMENT", 
                "description": "Auto-incrémentation (INTEGER PRIMARY KEY)", 
                "sql": "AUTOINCREMENT"}
        }
        
        # Initialiser la base de données
        self.init_database()
    
    def init_database(self):
        """Initialiser la connexion à la base de données"""
        try:
            # Créer le dossier data s'il n'existe pas
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            
            self.db_path = data_dir / "atarys_data.db"
            self.conn = sqlite3.connect(str(self.db_path))
            self.cursor = self.conn.cursor()
            print(f"✅ Base de données connectée: {self.db_path}")
        except Exception as e:
            print(f"❌ Erreur de connexion à la base: {e}")
            sys.exit(1)
    
    def show_header(self):
        """Afficher l'en-tête du script"""
        print("=" * 50)
        print("  ATARYS - IMPORT CSV INTERACTIF")
        print("=" * 50)
        print("📁 Dossier CSV:", self.csv_dir)
        print("⚙️  Configurations:", self.config_dir)
        print("📋 Logs:", self.logs_dir)
        print("🗄️  Base de données:", self.db_path)
        print()
    
    def list_csv_files(self):
        """Lister les fichiers CSV disponibles"""
        csv_files = list(self.csv_dir.glob("*.csv"))
        if not csv_files:
            print("❌ Aucun fichier CSV trouvé dans", self.csv_dir)
            print("📝 Placez vos fichiers CSV dans ce dossier et relancez le script")
            return None
        
        print("📊 Fichiers CSV disponibles:")
        for i, file in enumerate(csv_files, 1):
            print(f"  {i}. {file.name}")
        
        while True:
            try:
                choice = int(input(f"\nChoisissez un fichier (1-{len(csv_files)}): "))
                if 1 <= choice <= len(csv_files):
                    return csv_files[choice - 1]
                else:
                    print("❌ Choix invalide")
            except ValueError:
                print("❌ Veuillez entrer un nombre")
    
    def select_module(self):
        """Sélectionner le module ATARYS"""
        print("\n🏗️  Modules ATARYS disponibles:")
        for module_id, module_info in self.modules_atarys.items():
            print(f"  {module_id}. {module_info['name']}")
        
        while True:
            try:
                choice = int(input(f"\nQuel module traitez-vous ? ({', '.join(map(str, self.modules_atarys.keys()))}): "))
                if choice in self.modules_atarys:
                    return choice
                else:
                    print("❌ Module invalide")
            except ValueError:
                print("❌ Veuillez entrer un nombre")
    
    def analyze_csv(self, csv_file):
        """Analyser le contenu du fichier CSV"""
        # Essayer différents encodages et séparateurs
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252', 'iso-8859-1']
        separators = [';', ',', '\t', '|']
        
        for encoding in encodings:
            for sep in separators:
                try:
                    df = pd.read_csv(csv_file, nrows=5, encoding=encoding, sep=sep)
                    columns = list(df.columns)
                    
                    # Vérifier qu'on a bien plusieurs colonnes (pas une seule colonne avec tout le contenu)
                    if len(columns) > 1:
                        print(f"\n📊 Analyse du fichier: {csv_file.name}")
                        print(f"🔤 Encodage détecté: {encoding}")
                        print(f"🔗 Séparateur détecté: '{sep}'")
                        print(f"📋 Colonnes détectées: {len(columns)}")
                        print("📝 Aperçu des données:")
                        print(df.head())
                        
                        # Sauvegarder l'encodage et le séparateur pour l'import
                        self.detected_encoding = encoding
                        self.detected_separator = sep
                        
                        return columns, df
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    continue
        
        print(f"❌ Impossible de lire le fichier avec les encodages et séparateurs testés")
        print("💡 Vérifiez que votre fichier CSV a bien des en-têtes en première ligne")
        return None, None
    
    def select_column_type(self, column_name, sample_data):
        """Sélectionner le type pour une colonne"""
        print(f"\n🔧 Configuration de la colonne: {column_name}")
        print(f"📝 Exemple de données: {sample_data}")
        
        # Détection automatique pour les colonnes id
        if column_name.lower() in ['id', 'id_', '_id']:
            print("💡 Suggestion: Cette colonne ressemble à une clé primaire")
            auto_suggestion = 16  # PRIMARY_KEY
        else:
            auto_suggestion = None
        
        print("\nTypes disponibles:")
        for type_id, type_info in self.data_types.items():
            marker = " ⭐" if auto_suggestion and type_id == auto_suggestion else ""
            print(f"  {type_id}. {type_info['name']} - {type_info['description']}{marker}")
        
        while True:
            try:
                choice = int(input(f"\nChoisissez le type (1-{len(self.data_types)}): "))
                if choice in self.data_types:
                    selected_type = self.data_types[choice].copy()
                    
                    # Configuration spéciale selon le type
                    if choice == 15:  # FOREIGN_KEY
                        selected_type.update(self.configure_foreign_key(column_name))
                    elif choice == 7:  # ENUM
                        selected_type.update(self.configure_enum(column_name, sample_data))
                    elif choice in [8, 9, 10, 11, 12, 13, 14]:  # Types avec validation
                        selected_type.update(self.configure_validation(choice, column_name))
                    
                    # Configuration des contraintes
                    selected_type.update(self.configure_constraints(column_name, choice))
                    
                    return selected_type
                else:
                    print("❌ Type invalide")
            except ValueError:
                print("❌ Veuillez entrer un nombre")
    
    def configure_constraints(self, column_name, type_id):
        """Configurer les contraintes pour une colonne"""
        print(f"\n🔒 Configuration des contraintes pour: {column_name}")
        
        constraints_config = {}
        
        print("\nContraintes disponibles:")
        for constraint_id, constraint_info in self.constraints.items():
            print(f"  {constraint_id}. {constraint_info['name']} - {constraint_info['description']}")
        
        print("\nSélectionnez les contraintes (séparées par des virgules, ou 0 pour aucune):")
        try:
            choices = input("Choix: ").strip()
            if choices == "0" or not choices:
                return constraints_config
            
            selected_constraints = [int(x.strip()) for x in choices.split(",")]
            
            for constraint_id in selected_constraints:
                if constraint_id in self.constraints:
                    constraint_name = self.constraints[constraint_id]["name"]
                    
                    if constraint_name == "DEFAULT":
                        default_value = input(f"Valeur par défaut pour {column_name}: ")
                        constraints_config["default_value"] = default_value
                        constraints_config["constraints"] = constraints_config.get("constraints", []) + [f"DEFAULT '{default_value}'"]
                    
                    elif constraint_name == "CHECK":
                        check_condition = input(f"Condition CHECK pour {column_name} (ex: > 0, IN ('A','B','C')): ")
                        constraints_config["check_condition"] = check_condition
                        constraints_config["constraints"] = constraints_config.get("constraints", []) + [f"CHECK ({check_condition})"]
                    
                    else:
                        constraints_config["constraints"] = constraints_config.get("constraints", []) + [self.constraints[constraint_id]["sql"]]
                    
                    print(f"✅ Contrainte {constraint_name} ajoutée")
                else:
                    print(f"❌ Contrainte {constraint_id} invalide")
        
        except ValueError:
            print("❌ Format invalide")
        
        return constraints_config
    
    def configure_foreign_key(self, column_name):
        """Configurer une clé étrangère"""
        print(f"\n🔗 Configuration clé étrangère pour: {column_name}")
        
        # Lister les tables existantes
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in self.cursor.fetchall()]
        
        if existing_tables:
            print("Tables existantes:")
            for i, table in enumerate(existing_tables, 1):
                print(f"  {i}. {table}")
            
            while True:
                try:
                    choice = int(input(f"\nTable référencée (1-{len(existing_tables)}): "))
                    if 1 <= choice <= len(existing_tables):
                        referenced_table = existing_tables[choice - 1]
                        break
                    else:
                        print("❌ Choix invalide")
                except ValueError:
                    print("❌ Veuillez entrer un nombre")
        else:
            referenced_table = input("Nom de la table référencée: ")
        
        # Lister les colonnes de la table référencée
        try:
            self.cursor.execute(f"PRAGMA table_info({referenced_table})")
            columns = [row[1] for row in self.cursor.fetchall()]
            
            print(f"Colonnes de {referenced_table}:")
            for i, col in enumerate(columns, 1):
                print(f"  {i}. {col}")
            
            while True:
                try:
                    choice = int(input(f"\nColonne référencée (1-{len(columns)}): "))
                    if 1 <= choice <= len(columns):
                        referenced_column = columns[choice - 1]
                        break
                    else:
                        print("❌ Choix invalide")
                except ValueError:
                    print("❌ Veuillez entrer un nombre")
        except:
            referenced_column = input("Nom de la colonne référencée: ")
        
        return {
            "foreign_key": True,
            "referenced_table": referenced_table,
            "referenced_column": referenced_column
        }
    
    def configure_enum(self, column_name, sample_data):
        """Configurer un type ENUM"""
        print(f"\n📋 Configuration ENUM pour: {column_name}")
        print(f"📝 Exemple de données: {sample_data}")
        
        enum_values = []
        print("Entrez les valeurs ENUM (une par ligne, ligne vide pour terminer):")
        
        while True:
            value = input("Valeur: ").strip()
            if not value:
                break
            enum_values.append(value)
        
        if not enum_values:
            print("⚠️  Aucune valeur ENUM définie, utilisation de TEXT")
            return {"name": "TEXT"}
        
        return {
            "enum_type": True,
            "enum_values": enum_values
        }
    
    def configure_validation(self, type_id, column_name):
        """Configurer la validation pour les types spécialisés"""
        print(f"\n🔧 Configuration validation pour: {column_name}")
        
        validations = {
            8: {"name": "EMAIL", "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"},
            9: {"name": "PHONE", "pattern": r"^(\+33|0)[1-9](\d{8})$"},
            10: {"name": "POSTAL_CODE", "pattern": r"^[0-9]{5}$"},
            11: {"name": "CURRENCY", "pattern": r"^[0-9]+(\.[0-9]{2})?$"},
            12: {"name": "PERCENTAGE", "pattern": r"^[0-9]+(\.[0-9]+)?$"},
            13: {"name": "JSON", "pattern": None},  # Validation JSON spéciale
            14: {"name": "URL", "pattern": r"^https?://[^\s/$.?#].[^\s]*$"}
        }
        
        validation = validations.get(type_id, {})
        print(f"✅ Validation {validation['name']} configurée")
        
        return {
            "validation_type": validation["name"],
            "validation_pattern": validation.get("pattern")
        }
    
    def configure_columns(self, columns, df):
        """Configurer tous les types de colonnes"""
        column_configs = {}
        
        print(f"\n🔧 Configuration des {len(columns)} colonnes:")
        
        for column in columns:
            sample_data = str(df[column].iloc[0]) if not df[column].empty else "vide"
            column_type = self.select_column_type(column, sample_data)
            column_configs[column] = column_type
        
        return column_configs
    
    def create_table_sql(self, table_name, column_configs):
        """Générer le SQL de création de table"""
        columns_sql = []
        
        for column_name, config in column_configs.items():
            # Type SQL de base
            if config['name'] == 'INTEGER':
                sql_type = 'INTEGER'
            elif config['name'] == 'NUMERIC':
                sql_type = 'NUMERIC(10,2)'
            elif config['name'] == 'DATE':
                sql_type = 'DATE'
            elif config['name'] == 'DATETIME':
                sql_type = 'DATETIME'
            elif config['name'] == 'BOOLEAN':
                sql_type = 'BOOLEAN'
            elif config['name'] == 'JSON':
                sql_type = 'TEXT'
            else:
                sql_type = 'TEXT'
            
            # Clé primaire
            if config.get('primary_key'):
                sql_type = 'INTEGER PRIMARY KEY AUTOINCREMENT'
            
            # Construire la définition de colonne
            column_def = f"{column_name} {sql_type}"
            
            # Ajouter les contraintes
            if config.get('constraints'):
                column_def += " " + " ".join(config['constraints'])
            
            # Clé étrangère (doit être ajoutée après la définition de colonne)
            if config.get('foreign_key'):
                fk_constraint = f"FOREIGN KEY ({column_name}) REFERENCES {config['referenced_table']}({config['referenced_column']})"
                columns_sql.append(fk_constraint)
            
            columns_sql.append(column_def)
        
        # Créer le SQL final
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        sql += ",\n".join(columns_sql)
        sql += "\n)"
        
        return sql
    
    def create_table(self, table_name, column_configs):
        """Créer la table dans la base de données"""
        print(f"\n🏗️  Création de la table: {table_name}")
        
        # Vérifier si la table existe déjà
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if self.cursor.fetchone():
            print(f"⚠️  La table {table_name} existe déjà")
            choice = input("Voulez-vous la supprimer et la recréer ? (o/n): ").lower()
            if choice.startswith('o'):
                self.cursor.execute(f"DROP TABLE {table_name}")
                print(f"🗑️  Table {table_name} supprimée")
            else:
                print(f"✅ Utilisation de la table existante {table_name}")
                return True
        
        # Générer le SQL de création
        create_sql = self.create_table_sql(table_name, column_configs)
        
        print("📝 SQL de création:")
        print(create_sql)
        
        try:
            self.cursor.execute(create_sql)
            self.conn.commit()
            print(f"✅ Table {table_name} créée avec succès")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la création de la table: {e}")
            return False
    
    def save_configuration(self, csv_file, module_id, column_configs):
        """Sauvegarder la configuration"""
        # Nettoyer les configurations pour la sérialisation JSON
        clean_configs = {}
        for column, config in column_configs.items():
            clean_config = {
                "name": config["name"],
                "description": config["description"]
            }
            # Ajouter les configurations spéciales si elles existent
            if config.get("foreign_key"):
                clean_config.update({
                    "foreign_key": True,
                    "referenced_table": config["referenced_table"],
                    "referenced_column": config["referenced_column"]
                })
            if config.get("primary_key"):
                clean_config.update({
                    "primary_key": True
                })
            if config.get("enum_type"):
                clean_config.update({
                    "enum_type": True,
                    "enum_values": config["enum_values"]
                })
            if config.get("validation_type"):
                clean_config.update({
                    "validation_type": config["validation_type"],
                    "validation_pattern": config.get("validation_pattern")
                })
            if config.get("constraints"):
                clean_config.update({
                    "constraints": config["constraints"]
                })
            if config.get("default_value"):
                clean_config.update({
                    "default_value": config["default_value"]
                })
            if config.get("check_condition"):
                clean_config.update({
                    "check_condition": config["check_condition"]
                })
            clean_configs[column] = clean_config
        
        config = {
            "csv_file": csv_file.name,
            "module_id": module_id,
            "module_name": self.modules_atarys[module_id]["name"],
            "column_configs": clean_configs,
            "created_at": datetime.now().isoformat(),
            "atarys_version": "1.0"
        }
        
        config_file = self.config_dir / f"{csv_file.stem}_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuration sauvegardée: {config_file}")
        return config_file
    
    def preview_import(self, csv_file, column_configs):
        """Aperçu de l'import"""
        print(f"\n👀 APERÇU DE L'IMPORT")
        print("=" * 40)
        
        # Utiliser l'encodage et le séparateur détectés
        df = pd.read_csv(csv_file, nrows=3, encoding=getattr(self, 'detected_encoding', 'utf-8'), sep=getattr(self, 'detected_separator', ','))
        
        for column, config in column_configs.items():
            print(f"\n📋 {column}:")
            print(f"   Type: {config['name']}")
            if config.get('foreign_key'):
                print(f"   Référence: {config['referenced_table']}.{config['referenced_column']}")
            if config.get('primary_key'):
                print(f"   🔑 Clé primaire (auto-incrémentée)")
            if config.get('enum_type'):
                print(f"   📋 ENUM: {config['enum_values']}")
            if config.get('validation_type'):
                print(f"   ✅ Validation: {config['validation_type']}")
            if config.get('constraints'):
                print(f"   🔒 Contraintes: {', '.join(config['constraints'])}")
            if config.get('default_value'):
                print(f"   📝 Valeur par défaut: {config['default_value']}")
            if config.get('check_condition'):
                print(f"   ✅ Condition CHECK: {config['check_condition']}")
            
            # Afficher quelques exemples
            examples = df[column].head(3).tolist()
            print(f"   Exemples: {examples}")
        
        print(f"\n📊 Total: {len(df)} lignes à importer")
        
        return input("\nContinuer l'import ? (o/n): ").lower().startswith('o')
    
    def import_data(self, csv_file, column_configs):
        """Importer les données dans la base"""
        print(f"\n🚀 IMPORT DES DONNÉES")
        print("=" * 30)
        
        try:
            # Utiliser l'encodage et le séparateur détectés
            df = pd.read_csv(csv_file, encoding=getattr(self, 'detected_encoding', 'utf-8'), sep=getattr(self, 'detected_separator', ','))
            total_rows = len(df)
            imported_rows = 0
            errors = []
            
            # Déterminer la table cible (basé sur le nom du fichier ou la config)
            table_name = csv_file.stem
            
            print(f"📊 Import vers la table: {table_name}")
            print(f"📈 {total_rows} lignes à traiter")
            
            for index, row in df.iterrows():
                try:
                    # Convertir les données selon les types configurés
                    converted_data = {}
                    
                    for column, config in column_configs.items():
                        value = row[column]
                        
                        if pd.isna(value):
                            # Appliquer la valeur par défaut si configurée
                            if config.get('default_value'):
                                converted_data[column] = config['default_value']
                            else:
                                converted_data[column] = None
                        elif config['name'] == 'INTEGER':
                            converted_data[column] = int(value) if value else None
                        elif config['name'] == 'NUMERIC':
                            converted_data[column] = float(value) if value else None
                        elif config['name'] == 'BOOLEAN':
                            converted_data[column] = bool(value) if value else False
                        elif config['name'] == 'DATE':
                            if value:
                                converted_data[column] = pd.to_datetime(value).date()
                            else:
                                converted_data[column] = None
                        elif config['name'] == 'DATETIME':
                            if value:
                                converted_data[column] = pd.to_datetime(value)
                            else:
                                converted_data[column] = None
                        elif config['name'] == 'ENUM':
                            # Validation ENUM
                            if value in config.get('enum_values', []):
                                converted_data[column] = value
                            else:
                                errors.append(f"Ligne {index+1}: Valeur '{value}' non autorisée pour ENUM {column}")
                                continue
                        elif config['name'] == 'EMAIL':
                            # Validation email basique
                            if value and '@' in str(value) and '.' in str(value):
                                converted_data[column] = str(value)
                            else:
                                errors.append(f"Ligne {index+1}: Email invalide '{value}'")
                                continue
                        elif config['name'] == 'PHONE':
                            # Validation téléphone français
                            phone = str(value).replace(' ', '').replace('-', '')
                            if phone.startswith('0') and len(phone) == 10:
                                converted_data[column] = phone
                            else:
                                errors.append(f"Ligne {index+1}: Téléphone invalide '{value}'")
                                continue
                        elif config['name'] == 'POSTAL_CODE':
                            # Validation code postal français
                            if str(value).isdigit() and len(str(value)) == 5:
                                converted_data[column] = str(value)
                            else:
                                errors.append(f"Ligne {index+1}: Code postal invalide '{value}'")
                                continue
                        elif config['name'] == 'CURRENCY':
                            # Validation montant
                            try:
                                amount = float(value)
                                converted_data[column] = round(amount, 2)
                            except:
                                errors.append(f"Ligne {index+1}: Montant invalide '{value}'")
                                continue
                        elif config['name'] == 'PERCENTAGE':
                            # Validation pourcentage
                            try:
                                pct = float(value)
                                if 0 <= pct <= 100:
                                    converted_data[column] = pct
                                else:
                                    errors.append(f"Ligne {index+1}: Pourcentage invalide '{value}'")
                                    continue
                            except:
                                errors.append(f"Ligne {index+1}: Pourcentage invalide '{value}'")
                                continue
                        elif config['name'] == 'JSON':
                            # Validation JSON
                            try:
                                import json
                                if value:
                                    json.loads(str(value))
                                converted_data[column] = str(value) if value else None
                            except:
                                errors.append(f"Ligne {index+1}: JSON invalide '{value}'")
                                continue
                        elif config['name'] == 'URL':
                            # Validation URL basique
                            if value and ('http://' in str(value) or 'https://' in str(value)):
                                converted_data[column] = str(value)
                            else:
                                errors.append(f"Ligne {index+1}: URL invalide '{value}'")
                                continue
                        elif config['name'] == 'FOREIGN_KEY':
                            # Vérifier que la clé étrangère existe
                            ref_table = config['referenced_table']
                            ref_col = config['referenced_column']
                            
                            self.cursor.execute(f"SELECT COUNT(*) FROM {ref_table} WHERE {ref_col} = ?", (value,))
                            if self.cursor.fetchone()[0] > 0:
                                converted_data[column] = value
                            else:
                                errors.append(f"Ligne {index+1}: Clé étrangère {value} non trouvée dans {ref_table}")
                                continue
                        else:  # TEXT
                            converted_data[column] = str(value) if value else None
                    
                    # Insérer dans la base
                    columns = list(converted_data.keys())
                    placeholders = ', '.join(['?' for _ in columns])
                    values = list(converted_data.values())
                    
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    self.cursor.execute(query, values)
                    
                    imported_rows += 1
                    
                    if (index + 1) % 10 == 0:
                        print(f"   ✅ {index + 1}/{total_rows} lignes importées")
                
                except Exception as e:
                    errors.append(f"Ligne {index+1}: {str(e)}")
                    continue
            
            # Valider les changements
            self.conn.commit()
            
            print(f"\n✅ IMPORT TERMINÉ")
            print(f"📊 Lignes importées: {imported_rows}/{total_rows}")
            
            if errors:
                print(f"❌ Erreurs: {len(errors)}")
                error_log = self.logs_dir / f"{csv_file.stem}_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(error_log, 'w', encoding='utf-8') as f:
                    for error in errors:
                        f.write(f"{error}\n")
                print(f"📋 Détails des erreurs: {error_log}")
            
            return imported_rows, errors
            
        except Exception as e:
            print(f"❌ Erreur lors de l'import: {e}")
            return 0, [str(e)]
    
    def run(self):
        """Exécuter le script d'import"""
        self.show_header()
        
        # Sélectionner le fichier CSV
        csv_file = self.list_csv_files()
        if not csv_file:
            return
        
        # Sélectionner le module
        module_id = self.select_module()
        
        # Analyser le CSV
        columns, df = self.analyze_csv(csv_file)
        if not columns:
            return
        
        # Configurer les colonnes
        column_configs = self.configure_columns(columns, df)
        
        # Sauvegarder la configuration
        config_file = self.save_configuration(csv_file, module_id, column_configs)
        
        # Créer la table
        table_name = csv_file.stem
        if not self.create_table(table_name, column_configs):
            print("❌ Impossible de créer la table")
            return
        
        # Aperçu et confirmation
        if not self.preview_import(csv_file, column_configs):
            print("❌ Import annulé")
            return
        
        # Importer les données
        imported, errors = self.import_data(csv_file, column_configs)
        
        print(f"\n🎉 PROCESSUS TERMINÉ")
        print(f"📁 Fichier traité: {csv_file.name}")
        print(f"⚙️  Configuration: {config_file.name}")
        print(f"🗄️  Table créée: {table_name}")
        print(f"📊 Données importées: {imported} lignes")
        
        if errors:
            print(f"⚠️  {len(errors)} erreurs détectées (voir les logs)")

def main():
    """Point d'entrée principal"""
    try:
        importer = ATARYSCSVImporter()
        importer.run()
    except KeyboardInterrupt:
        print("\n\n❌ Opération annulée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 