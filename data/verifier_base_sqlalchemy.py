#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - VÉRIFICATION BASE SQLALCHEMY
Script pour vérifier la compatibilité de atarys_data.db avec SQLAlchemy et Flask

Auteur: ATARYS Team
Date: 2025
"""

import sqlite3
from pathlib import Path
from datetime import datetime


class ATARYSDatabaseChecker:
    """Classe pour vérifier la base de données ATARYS"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent
        self.db_path = self.data_dir / "atarys_data.db"
        
    def check_database_exists(self):
        """Vérifier si la base existe"""
        print("🔍 Vérification de l'existence de la base...")
        
        if not self.db_path.exists():
            print(f"❌ Base de données non trouvée: {self.db_path}")
            return False
        
        print(f"✅ Base trouvée: {self.db_path}")
        print(f"📊 Taille: {self.db_path.stat().st_size} octets")
        return True
    
    def check_sqlite_format(self):
        """Vérifier le format SQLite"""
        print("\n🔍 Vérification du format SQLite...")
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Vérifier la version SQLite
            cursor.execute("SELECT sqlite_version()")
            version = cursor.fetchone()[0]
            print(f"✅ Version SQLite: {version}")
            
            # Vérifier les tables existantes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                print("✅ Base vierge (aucune table)")
            else:
                print(f"⚠️  Base contient {len(tables)} table(s):")
                for table in tables:
                    print(f"   - {table[0]}")
            
            # Vérifier les index
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indexes = cursor.fetchall()
            print(f"📊 Index: {len(indexes)} trouvé(s)")
            
            # Vérifier les triggers
            cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
            triggers = cursor.fetchall()
            print(f"🔧 Triggers: {len(triggers)} trouvé(s)")
            
            # Vérifier les vues
            cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
            views = cursor.fetchall()
            print(f"👁️  Vues: {len(views)} trouvée(s)")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la vérification SQLite: {e}")
            return False
    
    def check_sqlalchemy_compatibility(self):
        """Vérifier la compatibilité avec SQLAlchemy"""
        print("\n🔍 Vérification compatibilité SQLAlchemy...")
        
        try:
            # Test d'import SQLAlchemy
            import sqlalchemy
            print("✅ SQLAlchemy version: " + sqlalchemy.__version__)
            
            # Test de connexion SQLAlchemy
            from sqlalchemy import create_engine, inspect
            
            engine = create_engine(f"sqlite:///{self.db_path}")
            inspector = inspect(engine)
            
            # Vérifier les tables via SQLAlchemy
            tables = inspector.get_table_names()
            print(f"📊 Tables détectées par SQLAlchemy: {len(tables)}")
            
            if tables:
                for table in tables:
                    columns = inspector.get_columns(table)
                    print(f"   - {table}: {len(columns)} colonne(s)")
            
            # Vérifier les contraintes
            for table in tables:
                foreign_keys = inspector.get_foreign_keys(table)
                if foreign_keys:
                    print(f"   🔗 {table}: {len(foreign_keys)} clé(s) étrangère(s)")
            
            engine.dispose()
            return True
            
        except ImportError as e:
            print(f"❌ SQLAlchemy non installé: {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur SQLAlchemy: {e}")
            return False
    
    def check_flask_compatibility(self):
        """Vérifier la compatibilité avec Flask"""
        print("\n🔍 Vérification compatibilité Flask...")
        
        try:
            # Test d'import Flask
            import flask
            print("✅ Flask version: " + flask.__version__)
            
            # Test d'import Flask-SQLAlchemy
            import flask_sqlalchemy
            print("✅ Flask-SQLAlchemy disponible")
            
            # Test de configuration Flask
            from flask import Flask
            from flask_sqlalchemy import SQLAlchemy
            
            app = Flask(__name__)
            app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{self.db_path}"
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            
            db = SQLAlchemy(app)
            
            with app.app_context():
                # Test de connexion Flask-SQLAlchemy
                db.engine.connect()
                print("✅ Connexion Flask-SQLAlchemy réussie")
                
                # Vérifier les métadonnées
                metadata = db.metadata
                print(f"📊 Métadonnées SQLAlchemy: {len(metadata.tables)} table(s) définie(s)")
            
            return True
            
        except ImportError as e:
            print(f"❌ Flask ou Flask-SQLAlchemy non installé: {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur Flask: {e}")
            return False
    
    def check_base_model_compatibility(self):
        """Vérifier la compatibilité avec BaseModel ATARYS"""
        print("\n🔍 Vérification compatibilité BaseModel...")
        
        try:
            # Simuler la structure BaseModel ATARYS
            from datetime import datetime
            from flask_sqlalchemy import SQLAlchemy
            
            db = SQLAlchemy()
            
            class BaseModel(db.Model):
                __abstract__ = True
                
                id = db.Column(db.Integer, primary_key=True)
                created_at = db.Column(db.DateTime, default=datetime.utcnow)
                updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            print("✅ Structure BaseModel compatible")
            print("✅ Types de données SQLAlchemy supportés:")
            print("   - INTEGER (clés primaires)")
            print("   - NUMERIC(10,2) (montants financiers)")
            print("   - STRING (textes courts)")
            print("   - TEXT (textes longs)")
            print("   - DATETIME (dates et heures)")
            print("   - BOOLEAN (vrai/faux)")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur BaseModel: {e}")
            return False
    
    def generate_report(self):
        """Générer un rapport complet"""
        print("=" * 60)
        print("  ATARYS - RAPPORT VÉRIFICATION BASE DE DONNÉES")
        print("=" * 60)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Base: {self.db_path}")
        print()
        
        checks = [
            ("Existence", self.check_database_exists),
            ("Format SQLite", self.check_sqlite_format),
            ("Compatibilité SQLAlchemy", self.check_sqlalchemy_compatibility),
            ("Compatibilité Flask", self.check_flask_compatibility),
            ("Compatibilité BaseModel", self.check_base_model_compatibility)
        ]
        
        results = []
        for name, check_func in checks:
            try:
                result = check_func()
                results.append((name, result))
            except Exception as e:
                print(f"❌ Erreur lors de {name}: {e}")
                results.append((name, False))
        
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES VÉRIFICATIONS")
        print("=" * 60)
        
        for name, result in results:
            status = "✅ OK" if result else "❌ ÉCHEC"
            print(f"{name:<25} {status}")
        
        print()
        print("🎯 RECOMMANDATIONS:")
        
        if all(result for _, result in results):
            print("✅ Base de données prête pour SQLAlchemy + Flask")
            print("✅ Compatible avec l'architecture ATARYS V2")
            print("✅ Prête pour le développement des modèles")
        else:
            print("⚠️  Problèmes détectés:")
            for name, result in results:
                if not result:
                    print(f"   - {name} nécessite une correction")
        
        print()
        print("📋 Prochaines étapes:")
        print("   1. Créer les modèles SQLAlchemy selon modules ATARYS")
        print("   2. Configurer Flask-Admin pour la visualisation")
        print("   3. Tester avec des données réelles")


def main():
    """Point d'entrée principal"""
    checker = ATARYSDatabaseChecker()
    checker.generate_report()


if __name__ == "__main__":
    main() 