#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la structure des tables
"""

import sqlite3
import os

def check_all_tables():
    """Vérifier la structure de toutes les tables"""
    
    # Chemin vers la base de données
    db_path = os.path.join('data', 'atarys_data.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        print(f"📋 Tables trouvées ({len(tables)}):")
        print("-" * 50)
        
        for table_row in tables:
            table_name = table_row[0]
            print(f"\n🔍 Table: {table_name}")
            
            # Récupérer la structure
            cursor.execute(f'PRAGMA table_info({table_name})')
            columns = cursor.fetchall()
            
            column_names = []
            for col in columns:
                cid, name, type_name, not_null, default_value, pk = col
                column_names.append(name)
                print(f"  - {name} ({type_name})")
                if pk:
                    print(f"    → PRIMARY KEY")
                if not_null:
                    print(f"    → NOT NULL")
                if default_value:
                    print(f"    → DEFAULT: {default_value}")
            
            # Vérifier les colonnes standard
            print(f"  📊 Colonnes standard:")
            print(f"    - 'id' présent: {'id' in column_names}")
            print(f"    - 'created_at' présent: {'created_at' in column_names}")
            print(f"    - 'updated_at' présent: {'updated_at' in column_names}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_all_tables() 