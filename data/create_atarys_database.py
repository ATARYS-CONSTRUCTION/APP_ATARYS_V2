#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - CRÉATION BASE DE DONNÉES VIERGE
Script pour créer une base de données SQLite vierge pour ATARYS V2

Auteur: ATARYS Team
Date: 2025
"""

import sqlite3
from pathlib import Path
import os


def create_virgin_database():
    """Créer une base de données SQLite vierge pour ATARYS"""
    
    # Chemin vers le dossier data
    data_dir = Path(__file__).parent
    db_path = data_dir / "atarys_data.db"
    
    # Supprimer la base existante si elle existe
    if db_path.exists():
        os.remove(db_path)
        print(f"🗑️  Base existante supprimée: {db_path}")
    
    # Créer une nouvelle base SQLite vierge
    try:
        conn = sqlite3.connect(str(db_path))
        conn.close()
        
        print("✅ Base de données ATARYS créée avec succès!")
        print(f"📁 Emplacement: {db_path}")
        print(f"📊 Taille: {db_path.stat().st_size} octets")
        print()
        print("📋 Base de données vierge prête pour:")
        print("   - Création des tables selon modules ATARYS")
        print("   - Import de données depuis Excel")
        print("   - Développement des modèles SQLAlchemy")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False


def verify_database():
    """Vérifier que la base est bien créée et vierge"""
    
    db_path = Path(__file__).parent / "atarys_data.db"
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Vérifier qu'il n'y a aucune table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if not tables:
            print("✅ Base de données vierge confirmée")
            print("📊 Aucune table trouvée")
        else:
            print("⚠️  Base de données contient des tables:")
            for table in tables:
                print(f"   - {table[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False


def main():
    """Point d'entrée principal"""
    print("=" * 50)
    print("  ATARYS - CRÉATION BASE DE DONNÉES VIERGE")
    print("=" * 50)
    print()
    
    # Créer la base
    if create_virgin_database():
        print()
        print("🔍 Vérification de la base...")
        verify_database()
    
    print()
    print("🎯 Prochaines étapes:")
    print("   1. Créer les modèles SQLAlchemy selon modules ATARYS")
    print("   2. Développer les tables prioritaires (3.1, 9.1, 10.1)")
    print("   3. Configurer Flask-Admin pour la gestion")
    print("   4. Importer les données depuis Excel")


if __name__ == "__main__":
    main() 