#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - CRÉATION SALARIÉ DE TEST
Script pour créer un salarié de test avec chemin OneDrive

Auteur: ATARYS Team
Date: 2025
"""

import sqlite3
from pathlib import Path
from datetime import date

def create_test_salary():
    """Créer un salarié de test avec chemin OneDrive"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent.parent / 'data' / 'atarys_data.db'
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    print(f"📁 Base de données trouvée : {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si le salarié de test existe déjà
        cursor.execute("""
            SELECT id FROM salaries 
            WHERE nom = 'TEST' AND prenom = 'OneDrive'
        """)
        
        existing = cursor.fetchone()
        
        if existing:
            print("ℹ️ Salarié de test existe déjà")
            return
        
        # Créer le salarié de test
        test_salary = {
            'nom': 'TEST',
            'prenom': 'OneDrive',
            'salaire_brut_horaire': 15.00,
            'nbre_heure_hebdo': 35.00,
            'type_contrat': 'CDI',
            'date_entree': '2025-01-01',
            'date_sortie': None,
            'niveau_qualification_id': 1,
            'colonne_planning': '1',
            'email': 'test.onedrive@atarys.com',
            'num_telephone': '0123456789',
            'adresse': '123 Rue Test',
            'code_postal': '35000',
            'ville': 'Rennes',
            'date_naissance': '1990-01-01',
            'num_securite_social': '1234567890123',
            'ondrive_path': '\\OneDrive\\Administration\\Volet social\\0-Dc'
        }
        
        # Insérer le salarié de test
        cursor.execute("""
            INSERT INTO salaries (
                nom, prenom, salaire_brut_horaire, nbre_heure_hebdo,
                type_contrat, date_entree, date_sortie, niveau_qualification_id,
                colonne_planning, email, num_telephone, adresse, code_postal,
                ville, date_naissance, num_securite_social, ondrive_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_salary['nom'], test_salary['prenom'], test_salary['salaire_brut_horaire'],
            test_salary['nbre_heure_hebdo'], test_salary['type_contrat'], test_salary['date_entree'],
            test_salary['date_sortie'], test_salary['niveau_qualification_id'],
            test_salary['colonne_planning'], test_salary['email'], test_salary['num_telephone'],
            test_salary['adresse'], test_salary['code_postal'], test_salary['ville'],
            test_salary['date_naissance'], test_salary['num_securite_social'],
            test_salary['ondrive_path']
        ))
        
        conn.commit()
        print("✅ Salarié de test créé avec succès")
        print(f"   Nom: {test_salary['nom']} {test_salary['prenom']}")
        print(f"   Chemin OneDrive: {test_salary['ondrive_path']}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    print("🔧 ATARYS - CRÉATION SALARIÉ DE TEST")
    print("="*50)
    
    create_test_salary() 