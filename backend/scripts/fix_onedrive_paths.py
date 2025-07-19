#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - CORRECTION AUTOMATIQUE CHEMINS ONEDRIVE
Script pour corriger automatiquement les chemins OneDrive dans la base de données

Auteur: ATARYS Team
Date: 2025
"""

import sqlite3
import os
from pathlib import Path

def fix_onedrive_paths():
    """Corriger automatiquement les chemins OneDrive dans la base de données"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent.parent / 'data' / 'atarys_data.db'
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    print(f"📁 Base de données trouvée : {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer tous les salariés avec leurs chemins OneDrive
        cursor.execute("""
            SELECT id, nom, prenom, ondrive_path 
            FROM salaries 
            WHERE ondrive_path IS NOT NULL AND ondrive_path != ''
        """)
        
        salaries = cursor.fetchall()
        
        if not salaries:
            print("ℹ️ Aucun salarié avec chemin OneDrive trouvé")
            return
        
        print(f"📋 {len(salaries)} salarié(s) avec chemin OneDrive trouvé(s)")
        print("\n" + "="*80)
        
        corrections_made = 0
        
        for salary_id, nom, prenom, ondrive_path in salaries:
            print(f"\n👤 {nom} {prenom} (ID: {salary_id})")
            print(f"   Chemin actuel: {ondrive_path}")
            
            # Analyser et corriger le chemin
            corrected_path = analyze_and_correct_path(ondrive_path)
            
            if corrected_path != ondrive_path:
                print(f"   🔧 Chemin corrigé: {corrected_path}")
                
                # Corriger automatiquement
                cursor.execute("""
                    UPDATE salaries 
                    SET ondrive_path = ? 
                    WHERE id = ?
                """, (corrected_path, salary_id))
                
                corrections_made += 1
                print("   ✅ Chemin corrigé en base")
            else:
                print("   ✅ Chemin correct")
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*80)
        print(f"✅ Correction terminée - {corrections_made} chemin(s) corrigé(s)")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

def analyze_and_correct_path(path):
    """Analyser et corriger un chemin OneDrive"""
    
    if not path:
        return path
    
    path = path.strip()
    
    # Si le chemin commence par \ (sans lettre de lecteur)
    if path.startswith('\\') and not path.startswith('\\\\'):
        return 'C:' + path
    
    # Si le chemin commence par OneDrive sans lettre de lecteur
    if path.startswith('OneDrive\\') or path.startswith('OneDrive/'):
        return 'C:\\' + path.replace('/', '\\')
    
    # Si le chemin est relatif mais sans ./
    if not path.startswith('./') and not path.startswith('../') and not path.startswith('C:') and not path.startswith('\\\\'):
        # Ajouter ./ pour le rendre relatif
        return './' + path
    
    return path

def test_paths_after_fix():
    """Tester les chemins après correction"""
    
    db_path = Path(__file__).parent.parent.parent / 'data' / 'atarys_data.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nom, prenom, ondrive_path 
            FROM salaries 
            WHERE ondrive_path IS NOT NULL AND ondrive_path != ''
        """)
        
        salaries = cursor.fetchall()
        
        print("\n🧪 TEST DES CHEMINS APRÈS CORRECTION")
        print("="*50)
        
        for salary_id, nom, prenom, ondrive_path in salaries:
            print(f"\n👤 {nom} {prenom}")
            print(f"   Chemin: {ondrive_path}")
            
            # Tester l'existence du chemin
            if os.path.exists(ondrive_path):
                print(f"   ✅ Existe: {ondrive_path}")
            else:
                print(f"   ❌ N'existe pas: {ondrive_path}")
                
                # Tester des variantes
                test_variants = [
                    ondrive_path.replace('\\', '/'),
                    ondrive_path.replace('/', '\\'),
                    'C:' + ondrive_path if not ondrive_path.startswith('C:') else None,
                    './' + ondrive_path if not ondrive_path.startswith('./') else None
                ]
                
                for variant in test_variants:
                    if variant and os.path.exists(variant):
                        print(f"   ✅ Variante existe: {variant}")
                        break
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    print("🔧 ATARYS - CORRECTION AUTOMATIQUE CHEMINS ONEDRIVE")
    print("="*60)
    
    # Étape 1: Corriger les chemins
    fix_onedrive_paths()
    
    # Étape 2: Tester les chemins après correction
    test_paths_after_fix()
    
    print("\n🎯 Instructions pour tester:")
    print("1. Ouvrir l'application sur http://localhost:3001")
    print("2. Aller dans Module 9.1 - Salariés")
    print("3. Cliquer sur un bouton OneDrive")
    print("4. Vérifier la console du navigateur (F12) pour les logs") 