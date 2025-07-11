#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - INITIALISATION BASE DE DONNÉES
Script pour créer les tables dans la base SQLite

Auteur: ATARYS Team
Date: 2025
"""

from app import create_app, db
from app.models.module_5_1 import articlesatarys

def init_database():
    """Initialiser la base de données avec les tables"""
    app = create_app('development')
    
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        
        print("✅ Base de données initialisée avec succès")
        print("📊 Tables créées :")
        
        # Lister les tables créées
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        for table in tables:
            print(f"  - {table}")
        
        print(f"\n🎉 {len(tables)} table(s) créée(s)")

if __name__ == '__main__':
    init_database() 